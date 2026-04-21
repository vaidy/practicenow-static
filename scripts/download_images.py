#!/usr/bin/env python3
"""
Safe image downloader for the PracticeNow static clone.

Reads /tmp/pn_crawl/content.json (and the original HTML pages), collects every
image URL referenced under https://practicenow.us/wp-content/, downloads each
into practicenow-static/images/wp/ preserving its filename, and verifies the
magic bytes match an allowed image type (JPG, PNG, GIF, WEBP, SVG).

Files that fail validation are deleted and logged.

The PracticeNow WordPress site is currently flagged for malware on its scripts.
Image binaries are far less risky, but we still:
  - filter to wp-content uploads only
  - reject anything > 5 MB
  - reject anything whose first bytes don't match an image signature
  - reject SVGs that contain <script or javascript: URIs
"""
import os, re, json, sys, hashlib
from urllib.request import Request, urlopen
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "images", "wp")
os.makedirs(OUT_DIR, exist_ok=True)

CONTENT_JSON = "/tmp/pn_crawl/content.json"
PAGES_DIR = "/tmp/pn_crawl/pages"
MAX_SIZE = 5 * 1024 * 1024
TIMEOUT = 20

MAGIC = [
    (b"\xff\xd8\xff", "jpg"),
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"RIFF", "webp"),  # checked further below
]

def detect_kind(data: bytes) -> str | None:
    head = data[:16]
    for prefix, kind in MAGIC:
        if head.startswith(prefix):
            if kind == "webp":
                if data[8:12] == b"WEBP":
                    return "webp"
                return None
            return kind
    # SVG
    sniff = data[:512].lstrip().lower()
    if sniff.startswith(b"<?xml") or sniff.startswith(b"<svg"):
        if b"<script" in data.lower() or b"javascript:" in data.lower() or b"onload=" in data.lower():
            return None
        return "svg"
    return None

def collect_urls() -> list[str]:
    urls: set[str] = set()
    if os.path.exists(CONTENT_JSON):
        for page in json.load(open(CONTENT_JSON)).values():
            for b in page.get("blocks", []):
                if b.get("type") == "image":
                    src = b.get("src", "")
                    if "practicenow.us/wp-content/" in src:
                        urls.add(src.split("?")[0])
    # Also scan raw HTML pages with regex (covers images that the parser missed,
    # e.g. background-image styles or <picture>/<source srcset>).
    if os.path.isdir(PAGES_DIR):
        for f in os.listdir(PAGES_DIR):
            if not f.endswith(".html"): continue
            txt = open(os.path.join(PAGES_DIR, f), errors="replace").read()
            for m in re.finditer(r"https://practicenow\.us/wp-content/uploads/[^\"'\s)]+", txt):
                u = m.group(0).split("?")[0]
                # filter obvious junk
                if u.lower().endswith((".jpg",".jpeg",".png",".gif",".webp",".svg")):
                    urls.add(u)
    return sorted(urls)

def safe_filename(url: str) -> str:
    p = urlparse(url)
    name = os.path.basename(p.path)
    # collapse ../, etc
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name:
        name = hashlib.md5(url.encode()).hexdigest() + ".bin"
    return name

def fetch(url: str) -> bytes | None:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (PracticeNow static clone bot)"})
    try:
        with urlopen(req, timeout=TIMEOUT) as r:
            cl = r.headers.get("Content-Length")
            if cl and int(cl) > MAX_SIZE:
                return None
            data = r.read(MAX_SIZE + 1)
            if len(data) > MAX_SIZE:
                return None
            return data
    except Exception as e:
        print(f"  fetch fail {url}: {e}")
        return None

def main():
    urls = collect_urls()
    print(f"Found {len(urls)} candidate image URLs.\n")
    ok = 0
    bad = 0
    skipped_existing = 0
    manifest = {}
    for url in urls:
        fname = safe_filename(url)
        out = os.path.join(OUT_DIR, fname)
        if os.path.exists(out) and os.path.getsize(out) > 0:
            skipped_existing += 1
            manifest[url] = "images/wp/" + fname
            continue
        data = fetch(url)
        if data is None:
            print(f"  SKIP {url} (fetch failed/too large)")
            bad += 1
            continue
        kind = detect_kind(data)
        if kind is None:
            print(f"  REJECT {url} (no valid image signature, {len(data)} bytes)")
            bad += 1
            continue
        with open(out, "wb") as fh:
            fh.write(data)
        ok += 1
        manifest[url] = "images/wp/" + fname
    print(f"\nOK: {ok}   BAD: {bad}   ALREADY-PRESENT: {skipped_existing}")
    manifest_path = os.path.join(ROOT, "images", "wp", "_manifest.json")
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"Manifest written to {manifest_path}")

if __name__ == "__main__":
    main()
