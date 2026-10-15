#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Gate, search, and read a batch of GitHub repos in one call.

Needs only Python's standard library and git, and calls no rate-limited API.
Each stage tries its sources in order and moves to the next when one fails
or returns data that fails validation.

  gate:   ecosystems (repos.ecosyste.ms), page (the github.com repo page and
          commit feed), depsdev (api.deps.dev, stars only)
  search: clone (shallow clone and git grep), sourcegraph (sourcegraph.com
          search), tarball (codeload.github.com, searched in memory)
  show:   githubusercontent (raw.githubusercontent.com), sourcegraph (raw
          files), with the last commit that touched the file, from its commit feed

Patterns must be valid in both RE2 and PCRE, such as '\\bmedia_?type\\b'.
Searching may clone into a temp folder, which the script deletes before it exits;
read the files you need with --show.

    survey.py owner/repo ... -p media='\\bmedia_?type\\b' -p mime='\\bmime_?type\\b' \\
        [--path '\\.py$'] [--exclude 'test'] [--ignore-case] [--top 5] [--skip SOURCE]
    survey.py --show owner/repo@sha:path [--show ...]
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple, Optional

GATE_SOURCES = ("ecosystems", "page", "depsdev")
SEARCH_SOURCES = ("clone", "sourcegraph", "tarball")
TIMEOUT_SECONDS = 60
CLONE_TIMEOUT_SECONDS = 180
ECOSYSTEMS_MAX_STALENESS = timedelta(days=14)


class SourceError(Exception):
    """A source failed, or returned data that does not pass validation."""


class Gate(NamedTuple):
    source: str
    stars: int
    archived: Optional[bool]  # None when the source cannot tell
    activity: Optional[datetime]  # latest push or commit to the default branch


class Search(NamedTuple):
    sha: str
    counts: dict  # pattern label → {path: matching lines}


class Patterns(NamedTuple):
    items: list  # [(label, regex)]
    path: str
    exclude: str
    ignore_case: bool

    def keeps(self, path: str) -> bool:
        if self.path and not re.search(self.path, path):
            return False
        return not (self.exclude and re.search(self.exclude, path))


# a python.org install on macOS ships without CA certificates until its installer step runs
SYSTEM_CA_BUNDLES = (
    "/etc/ssl/cert.pem",
    "/etc/ssl/certs/ca-certificates.crt",
    "/etc/pki/tls/certs/ca-bundle.crt",
    "/etc/ssl/ca-bundle.pem",
)


def tls_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    if not context.cert_store_stats()["x509_ca"]:
        for bundle in SYSTEM_CA_BUNDLES:
            if os.path.exists(bundle):
                context.load_verify_locations(cafile=bundle)
                break
    return context


TLS_CONTEXT = tls_context()


def fetch(url: str) -> Optional[bytes]:
    """GET a URL; None on 404, SourceError on any other failure."""
    request = urllib.request.Request(url, headers={"User-Agent": "pq-ask-top-repos"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS, context=TLS_CONTEXT) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise SourceError(f"HTTP {error.code} from {url}") from error
    except OSError as error:
        raise SourceError(f"{error} from {url}") from error


def parse_time(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def git(args: list, timeout: float = TIMEOUT_SECONDS, no_match_ok: bool = False) -> str:
    try:
        result = subprocess.run(
            ["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout
        )
    except subprocess.TimeoutExpired as error:
        raise SourceError(f"git timed out after {timeout}s") from error
    # git grep exits 1 when nothing matches, which is an answer, not a failure
    if result.returncode and not (no_match_ok and result.returncode == 1):
        raise SourceError(f"git {args[-1]}: {result.stderr.strip()[:200]}")
    return result.stdout


# Gate sources: each returns a Gate, None when it does not know the repo, or raises SourceError.


def gate_ecosystems(repo: str) -> Optional[Gate]:
    body = fetch(f"https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/{urllib.parse.quote(repo, safe='')}")
    if body is None:
        return None
    data = json.loads(body)
    stars, archived, pushed, synced = (data.get(key) for key in ("stargazers_count", "archived", "pushed_at", "last_synced_at"))
    if not isinstance(stars, int) or not isinstance(archived, bool) or not pushed or not synced:
        raise SourceError("ecosystems: response lacks stars, archived, pushed_at, or last_synced_at")
    if datetime.now(timezone.utc) - parse_time(synced) > ECOSYSTEMS_MAX_STALENESS:
        raise SourceError(f"ecosystems: {repo} last synced {synced[:10]}")
    return Gate("ecosystems", stars, archived, parse_time(pushed))


def feed_updated(url: str) -> Optional[datetime]:
    """Read the newest entry's date from a github.com Atom feed."""
    body = fetch(url)
    entry = re.search(r"<entry>.*?<updated>([^<]+)</updated>", (body or b"").decode("utf-8", "replace"), re.S)
    return parse_time(entry.group(1)) if entry else None


def gate_page(repo: str) -> Optional[Gate]:
    body = fetch(f"https://github.com/{repo}")
    if body is None:
        return None
    page = body.decode("utf-8", errors="replace")
    # the page embeds its repository data as JSON
    stars = re.search(r'"stargazerCount":(\d+)', page)
    archived = re.search(r'"isArchived":(true|false)', page)
    if not stars or not archived:
        raise SourceError("page: no stargazerCount or isArchived")
    activity = feed_updated(f"https://github.com/{repo}/commits.atom")
    return Gate("page", int(stars.group(1)), archived.group(1) == "true", activity)


def gate_depsdev(repo: str) -> Optional[Gate]:
    body = fetch(f"https://api.deps.dev/v3/projects/{urllib.parse.quote('github.com/' + repo, safe='')}")
    if body is None:
        return None
    stars = json.loads(body).get("starsCount")
    if not isinstance(stars, int):
        raise SourceError("depsdev: no starsCount")
    return Gate("depsdev", stars, None, feed_updated(f"https://github.com/{repo}/commits.atom"))


GATES = {"ecosystems": gate_ecosystems, "page": gate_page, "depsdev": gate_depsdev}


def gate_repo(repo: str, sources: list) -> tuple:
    """Return the first Gate a working source gives, and why earlier sources gave none."""
    misses = []
    for source in sources:
        try:
            gate = GATES[source](repo)
        except SourceError as error:
            misses.append(str(error))
            continue
        if gate is not None:
            return gate, misses
        misses.append(f"{source}: not found")
    return None, misses


def verdict(repo: str, gate: Gate, min_stars: int, window: timedelta) -> tuple:
    summary = f"via {gate.source}, stars={gate.stars}, activity={gate.activity.date() if gate.activity else 'unknown'}"
    if gate.archived:
        return False, f"archived; {summary}"
    if gate.stars < min_stars:
        return False, f"under {min_stars} stars, downloads unchecked; {summary}"
    cutoff = datetime.now(timezone.utc) - window
    if gate.activity is None or gate.activity < cutoff:
        try:
            release = feed_updated(f"https://github.com/{repo}/releases.atom")
        except SourceError:
            release = None
        if release is None or release < cutoff:
            return False, f"no commit or release in {window.days} days; {summary}, release={release.date() if release else 'none'}"
        summary += f", release={release.date()}"
    if gate.archived is None:
        summary += ", archived unverified"
    return True, summary


# Search sources: each takes every repo and pattern at once and returns a Search per repo.


def sourcegraph_query(repos: list, regex: str, patterns: Patterns) -> dict:
    """Return {repo: (sha, {path: lines})} for the repos with a match."""
    names = {f"github.com/{repo}".lower(): repo for repo in repos}
    query = "repo:^({})$ archived:yes fork:yes case:{} count:all /{}/".format(
        "|".join(re.escape(name) for name in names), "no" if patterns.ignore_case else "yes", regex
    )
    if patterns.path:
        query += f" file:{patterns.path}"
    if patterns.exclude:
        query += f" -file:{patterns.exclude}"
    body = fetch("https://sourcegraph.com/.api/search/stream?" + urllib.parse.urlencode({"q": query, "display": "100000"}))
    if body is None:
        raise SourceError("sourcegraph: search endpoint not found")
    found: dict = {}
    done = False
    for block in body.decode("utf-8", errors="replace").split("\n\n"):
        lines = block.split("\n")
        event = lines[0][len("event: "):] if lines[0].startswith("event: ") else ""
        data = "\n".join(line[len("data: "):] for line in lines if line.startswith("data: "))
        if event in ("alert", "error"):
            raise SourceError(f"sourcegraph {event}: {data[:200]}")
        if event == "progress":
            for skipped in json.loads(data).get("skipped", []):
                # display caps only what is shown; any other reason means the count is incomplete
                if skipped.get("reason") != "display":
                    raise SourceError(f"sourcegraph skipped results: {skipped.get('reason')}")
        elif event == "done":
            done = True
        elif event == "matches":
            for match in json.loads(data):
                repo = names.get(match.get("repository", "").lower())
                if match.get("type") != "content" or repo is None or not patterns.keeps(match["path"]):
                    continue
                sha, files = found.setdefault(repo, (match["commit"], {}))
                if match["commit"] != sha:
                    raise SourceError(f"sourcegraph: {repo} answered from two commits")
                files[match["path"]] = len({line["lineNumber"] for line in match["lineMatches"]})
    if not done:
        raise SourceError("sourcegraph: stream ended before done")
    return found


def search_sourcegraph(repos: list, patterns: Patterns, folder: Path) -> dict:
    with ThreadPoolExecutor(max_workers=len(patterns.items)) as pool:
        answers = list(pool.map(lambda item: sourcegraph_query(repos, item[1], patterns), patterns.items))
    shas: dict = {}
    counts: dict = {repo: {} for repo in repos}
    for (label, _), found in zip(patterns.items, answers):
        for repo in repos:
            sha, files = found.get(repo, ("", {}))
            counts[repo][label] = files
            if sha and shas.setdefault(repo, sha) != sha:
                raise SourceError(f"sourcegraph: {repo} answered from two commits")
    results = {repo: Search(sha, counts[repo]) for repo, sha in shas.items()}
    # a repo with no match carries no commit, so clone it for its absence row
    unmatched = [repo for repo in repos if repo not in shas]
    if unmatched:
        results.update(search_clone(unmatched, patterns, folder))
    return results


def clone(repo: str, folder: Path) -> Path:
    target = folder / repo.replace("/", "__")
    if not target.exists():
        url = f"https://github.com/{repo}.git"
        git(["clone", "--quiet", "--depth", "1", "--no-checkout", url, str(target)], timeout=CLONE_TIMEOUT_SECONDS)
    return target


def grep_clone(clone_dir: Path, patterns: Patterns) -> Search:
    sha = git(["-C", str(clone_dir), "rev-parse", "HEAD"]).strip()
    counts: dict = {}
    for label, regex in patterns.items:
        args = ["-C", str(clone_dir), "grep", "-I", "-c", "-P"] + (["-i"] if patterns.ignore_case else [])
        files = {}
        for line in git([*args, regex, "HEAD"], no_match_ok=True).splitlines():
            # each line reads HEAD:<path>:<count>
            path, _, hits = line[len("HEAD:"):].rpartition(":")
            if patterns.keeps(path):
                files[path] = int(hits)
        counts[label] = files
    return Search(sha, counts)


def search_clone(repos: list, patterns: Patterns, folder: Path) -> dict:
    with ThreadPoolExecutor(max_workers=len(repos)) as pool:
        clone_dirs = list(pool.map(lambda repo: clone(repo, folder), repos))
    return {repo: grep_clone(clone_dir, patterns) for repo, clone_dir in zip(repos, clone_dirs)}


def search_tarball_repo(repo: str, patterns: Patterns) -> Search:
    body = fetch(f"https://codeload.github.com/{repo}/tar.gz/HEAD")
    if body is None:
        raise SourceError(f"tarball: {repo} not found")
    flags = re.IGNORECASE if patterns.ignore_case else 0
    compiled = [(label, re.compile(regex, flags)) for label, regex in patterns.items]
    counts: dict = {label: {} for label, _ in patterns.items}
    with tarfile.open(fileobj=io.BytesIO(body), mode="r:gz") as archive:
        # GitHub writes the commit id into the archive's global header
        sha = archive.pax_headers.get("comment", "")
        for member in archive:
            # members sit under one top folder, such as atom-HEAD/
            path = member.name.partition("/")[2]
            if not member.isfile() or not patterns.keeps(path):
                continue
            content = archive.extractfile(member).read()  # type: ignore[union-attr]
            if b"\0" in content[:8000]:
                continue
            lines = content.decode("utf-8", errors="replace").splitlines()
            for label, regex in compiled:
                hits = sum(1 for line in lines if regex.search(line))
                if hits:
                    counts[label][path] = hits
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise SourceError(f"tarball: {repo} carries no commit id")
    return Search(sha, counts)


def search_tarball(repos: list, patterns: Patterns, folder: Path) -> dict:
    with ThreadPoolExecutor(max_workers=len(repos)) as pool:
        return dict(zip(repos, pool.map(lambda repo: search_tarball_repo(repo, patterns), repos)))


SEARCHES = {"sourcegraph": search_sourcegraph, "clone": search_clone, "tarball": search_tarball}


def search_all(repos: list, patterns: Patterns, folder: Path, skip: set) -> tuple:
    """Search with the first source that answers."""
    misses = []
    for source in SEARCH_SOURCES:
        if source in skip:
            continue
        try:
            return source, SEARCHES[source](repos, patterns, folder), misses
        except SourceError as error:
            misses.append(str(error))
    raise SourceError("every search source failed: " + "; ".join(misses))


SHOW_URLS = {
    "githubusercontent": "https://raw.githubusercontent.com/{repo}/{sha}/{path}",
    "sourcegraph": "https://sourcegraph.com/github.com/{repo}@{sha}/-/raw/{path}",
}


def show(spec: str, skip: set) -> str:
    repo, _, rest = spec.partition("@")
    sha, _, path = rest.partition(":")
    misses = []
    for source, url in SHOW_URLS.items():
        if source in skip:
            continue
        try:
            body = fetch(url.format(repo=repo, sha=sha, path=path))
        except SourceError as error:
            misses.append(str(error))
            continue
        if body is not None:
            return body.decode("utf-8", errors="replace")
        misses.append(f"{source}: not found")
    raise SourceError(f"{spec}: " + "; ".join(misses))


def last_touched(spec: str) -> str:
    """Name the newest commit at or before sha that touched path, from its commit feed."""
    repo, _, rest = spec.partition("@")
    sha, _, path = rest.partition(":")
    try:
        body = fetch(f"https://github.com/{repo}/commits/{sha}/{path}.atom")
    except SourceError:
        return "unknown"
    feed = (body or b"").decode("utf-8", errors="replace")
    commit = re.search(r"Commit/([0-9a-f]{40})", feed)
    updated = re.search(r"<entry>.*?<updated>([^<]+)</updated>", feed, re.S)
    return f"{commit.group(1)[:12]} {updated.group(1)[:10]}" if commit and updated else "unknown"


def survey(options: argparse.Namespace, skip: set, folder: Path) -> int:
    patterns = Patterns([tuple(entry.split("=", 1)) for entry in options.pattern], options.path, options.exclude, options.ignore_case)

    gate_sources = [source for source in GATE_SOURCES if source not in skip]
    with ThreadPoolExecutor(max_workers=len(options.repos)) as pool:
        gated = dict(zip(options.repos, pool.map(lambda repo: gate_repo(repo, gate_sources), options.repos)))

    window = timedelta(days=options.window_days)
    verdicts = {}
    for repo, (gate, misses) in gated.items():
        if gate is None:
            verdicts[repo] = (False, "no gate source knows it: " + "; ".join(misses))
        else:
            verdicts[repo] = verdict(repo, gate, options.min_stars, window)
    passing = [repo for repo, (passed, _) in verdicts.items() if passed]

    searches: dict = {}
    if passing:
        source, searches, misses = search_all(passing, patterns, folder, skip)
        print(f"search via {source}" + (f" (after: {'; '.join(misses)})" if misses else ""))

    for repo in options.repos:
        passed, summary = verdicts[repo]
        if not passed:
            print(f"\n## {repo}: excluded ({summary})")
            continue
        search = searches[repo]
        print(f"\n## {repo}: passes gate ({summary})")
        print(f"head: {search.sha[:12]}  link: https://github.com/{repo}/blob/{search.sha}/")
        for label, files in search.counts.items():
            print(f"- {label}: {sum(files.values())} lines in {len(files)} files")
            for path, hits in sorted(files.items(), key=lambda item: -item[1])[: options.top]:
                print(f"    {hits:>5}  {path}")
    return 0


def show_all(specs: list, skip: set) -> int:
    """Print every requested file, fetching all files and their last commits at once."""

    def one(spec: str) -> str:
        try:
            return f"===== {spec} (last touched: {last_touched(spec)})\n{show(spec, skip)}"
        except SourceError as error:
            return f"===== {spec}\nerror: {error}"

    with ThreadPoolExecutor(max_workers=len(specs)) as pool:
        outputs = list(pool.map(one, specs))
    print("\n".join(outputs))
    return 1 if any("\nerror: " in output for output in outputs) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repos", nargs="*", help="owner/name of each candidate")
    parser.add_argument("-p", "--pattern", action="append", default=[], help="label=regex, valid in RE2 and PCRE")
    parser.add_argument("--path", default="", help="regex a searched path must match, such as '\\.py$'")
    parser.add_argument("--exclude", default="", help="regex a searched path must not match, such as 'test'")
    parser.add_argument("--ignore-case", action="store_true")
    parser.add_argument("--top", type=int, default=5, help="files listed per pattern and repo")
    parser.add_argument("--min-stars", type=int, default=1000)
    parser.add_argument("--window-days", type=int, default=90)
    parser.add_argument("--skip", action="append", default=[], help="source to leave out; repeatable")
    parser.add_argument("--show", action="append", default=[], help="owner/repo@sha:path to print; repeatable")
    options = parser.parse_args()
    skip = set(options.skip)
    try:
        if options.show:
            return show_all(options.show, skip)
        if not options.repos or not options.pattern:
            parser.error("give at least one repo and one --pattern")
        folder = Path(tempfile.mkdtemp(prefix="pq-ask-top-repos-"))
        try:
            return survey(options, skip, folder)
        finally:
            shutil.rmtree(folder, ignore_errors=True)
    except SourceError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
