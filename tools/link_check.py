"""Crawl-based link checker for the AlgoViz Flask app.

Walks every route in the app's url_map, fetches each page with the test
client, and validates every href/src/data-sync attribute found in the
rendered HTML (so Jinja url_for() calls are checked as the browser sees
them):

- external schemes (http/https/mailto/tel/javascript/urn/data/...),
  fragments and empty links are skipped;
- "/static/..." URLs are verified against the real directory listing with
  an exact case-sensitive comparison, so "videos/" vs "Videos/" is caught
  even on case-insensitive filesystems (Windows) before a Linux deploy;
- everything else is fetched with the test client: 2xx/3xx is OK, 4xx/5xx
  is broken;
- <a> tags without an href are counted as non-failing dead-anchor warnings.

run() returns (known_broken, new_broken, warnings) so pytest can assert
that no NEW broken link appeared versus the baseline allowlist
(docs/Plan/baseline-broken-links.txt).
"""

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ALLOWLIST = ROOT / "docs" / "Plan" / "baseline-broken-links.txt"
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "urn", "data", "blob", "about"}
LINK_ATTRS = ("href", "src", "data-sync")


def _load_flask_app():
    website_dir = ROOT / "Website"
    if str(website_dir) not in sys.path:
        sys.path.insert(0, str(website_dir))
    from website import create_app

    return create_app()


class _LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []
        self.dead_anchor_lines: list[int] = []

    def handle_starttag(self, tag, attrs):
        names = [name for name, _ in attrs]
        if tag == "a" and "href" not in names:
            self.dead_anchor_lines.append(self.getpos()[0])
        for name, value in attrs:
            if name in LINK_ATTRS and value:
                self.urls.append(value)


def _static_file_reason(static_root: Path, url_path: str) -> str | None:
    rel = unquote(url_path)[len("/static/"):]
    parts = [part for part in rel.split("/") if part]
    if not parts:
        return "static root itself referenced"
    current = static_root
    for part in parts:
        try:
            names = {entry.name for entry in current.iterdir()}
        except OSError:
            return f"static directory missing: {current.name}"
        if part not in names:
            return f"static file not found (exact case): static/{rel}"
        current = current / part
    if not current.is_file():
        return f"static target is not a file: static/{rel}"
    return None


def _page_status(client, cache: dict[str, int], resolved: str) -> int:
    parts = urlsplit(resolved)
    target = quote(unquote(parts.path)) + (f"?{parts.query}" if parts.query else "")
    if target not in cache:
        cache[target] = client.get(target).status_code
    return cache[target]


def _classify(client, status_cache: dict[str, int], static_root: Path, page: str, raw_url: str):
    url = raw_url.strip()
    if not url or url.startswith("#"):
        return None
    if urlsplit(url).scheme in EXTERNAL_SCHEMES:
        return None
    resolved = urljoin(page, url)
    parts = urlsplit(resolved)
    if parts.scheme or parts.netloc:
        return None
    if parts.path.startswith("/static/"):
        reason = _static_file_reason(static_root, parts.path)
        if reason:
            return resolved, reason
        return None
    status = _page_status(client, status_cache, resolved)
    if 200 <= status < 400:
        return None
    return resolved, f"route returned {status}"


def _allowlist_urls(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    urls = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(" -> ")
        urls.add(fields[1] if len(fields) >= 3 else line)
    return urls


def run(allowlist_path=None, strict=False):
    """Crawl every app page and classify its links.

    Returns (known_broken, new_broken, warnings): the first two are lists of
    "origin page -> URL -> reason" lines, warnings are dead-anchor notes.
    """
    app = _load_flask_app()
    client = app.test_client()
    static_root = Path(app.static_folder)
    if strict:
        allowlist_urls: set[str] = set()
    else:
        allowlist = Path(allowlist_path) if allowlist_path else DEFAULT_ALLOWLIST
        allowlist_urls = _allowlist_urls(allowlist)
    pages = sorted(
        rule.rule
        for rule in app.url_map.iter_rules()
        if rule.endpoint != "static" and not rule.arguments
    )
    broken: dict[str, str] = {}
    warnings: dict[str, None] = {}
    status_cache: dict[str, int] = {}

    for page in pages:
        response = client.get(quote(page))
        if response.status_code >= 400:
            broken.setdefault(page, f"{page} -> {page} -> route returned {response.status_code}")
            continue
        if response.status_code >= 300:
            continue
        extractor = _LinkExtractor()
        extractor.feed(response.get_data(as_text=True))
        for line in extractor.dead_anchor_lines:
            warnings[f"{page}:{line} <a> without href"] = None
        for raw_url in extractor.urls:
            finding = _classify(client, status_cache, static_root, page, raw_url)
            if finding:
                url, reason = finding
                broken.setdefault(url, f"{page} -> {url} -> {reason}")

    known = [line for url, line in sorted(broken.items()) if url in allowlist_urls]
    new = [line for url, line in sorted(broken.items()) if url not in allowlist_urls]
    return known, new, list(warnings)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check all links rendered by the Flask app.")
    parser.add_argument("--allowlist", default=str(DEFAULT_ALLOWLIST), help="baseline allowlist file")
    parser.add_argument("--strict", action="store_true", help="ignore the allowlist entirely")
    parser.add_argument("--verbose", action="store_true", help="also list dead-anchor warnings")
    args = parser.parse_args(argv)

    known, new, warnings = run(allowlist_path=args.allowlist, strict=args.strict)

    print(f"new broken links: {len(new)}")
    for line in new:
        print(line)
    print(f"known-broken (allowlisted): {len(known)}")
    for line in known:
        print(line)
    print(f"dead-anchor warnings: {len(warnings)} (do not fail the run)")
    if args.verbose:
        for line in warnings:
            print(line)
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
