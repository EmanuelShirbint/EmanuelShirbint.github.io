#!/usr/bin/env python3
"""
verify_site.py — read-only integrity checks for the Emanuel Shirbint Research
Review static site. Run from the repository root:  python3 automation/verify_site.py

Exit code 0 = all checks passed (safe to commit & push).
Exit code 1 = at least one problem found (do NOT push; investigate / notify).

Checks performed:
  1. feed.xml, research/feed.xml, sitemap.xml are well-formed XML.
  2. Every internal page link (href="/...") resolves to a real file on disk
     (a directory link must contain index.html).
  3. Every /assets/... link points to a file that exists.
  4. Record-count sanity: number of /research/works/<slug>/ directories matches
     the "<N> records" figure on the homepage and the Emanuel Shirbint author
     count in research/index.html (warnings only, not hard failures).
"""
import glob
import os
import re
import sys
import xml.dom.minidom

ROOT = os.getcwd()
problems = []
warnings = []

# 1) XML well-formedness ------------------------------------------------------
for f in ["feed.xml", "research/feed.xml", "sitemap.xml"]:
    if not os.path.exists(f):
        problems.append(f"missing XML file: {f}")
        continue
    try:
        xml.dom.minidom.parse(f)
    except Exception as e:  # noqa: BLE001
        problems.append(f"malformed XML in {f}: {e}")

# 2) internal page links ------------------------------------------------------
htmls = glob.glob("**/*.html", recursive=True)
link_re = re.compile(r'href="(/[^"#?]*)"')
for h in htmls:
    txt = open(h, encoding="utf-8").read()
    for m in link_re.finditer(txt):
        p = m.group(1).lstrip("/")
        if p == "":
            continue  # site root
        if p.endswith((".pdf", ".xml", ".bib", ".ris", ".txt", ".css", ".png",
                        ".jpg", ".jpeg", ".svg", ".ico", ".js")):
            cand = p
        else:
            cand = os.path.join(p, "index.html")
        if not os.path.exists(cand):
            problems.append(f"broken link in {h}: {m.group(1)}")

# 3) asset links --------------------------------------------------------------
asset_re = re.compile(r'(?:href|src)="(/assets/[^"]+)"')
for h in htmls:
    txt = open(h, encoding="utf-8").read()
    for m in asset_re.finditer(txt):
        a = m.group(1).lstrip("/")
        if not os.path.exists(a):
            problems.append(f"missing asset referenced in {h}: {m.group(1)}")

# 4) record-count sanity ------------------------------------------------------
work_dirs = [d for d in glob.glob("research/works/*") if os.path.isdir(d)]
n_works = len(work_dirs)
try:
    home = open("index.html", encoding="utf-8").read()
    m = re.search(r"<span>(\d+)\s+records</span>", home)
    if m and int(m.group(1)) != n_works:
        warnings.append(
            f'homepage says "{m.group(1)} records" but there are {n_works} '
            f"work directories")
except FileNotFoundError:
    problems.append("missing index.html")

try:
    arch = open("research/index.html", encoding="utf-8").read()
    m = re.search(r"Emanuel Shirbint</strong>\s*<strong>\(archive author\)</strong>\s*"
                  r"<span class=\"small\">— (\d+) record", arch)
    if m and int(m.group(1)) != n_works:
        warnings.append(
            f'author index says "{m.group(1)} records" but there are {n_works} '
            f"work directories")
except FileNotFoundError:
    problems.append("missing research/index.html")

# report ----------------------------------------------------------------------
for w in warnings:
    print(f"WARNING: {w}")
if problems:
    for p in problems:
        print(f"FAIL: {p}")
    print(f"\n{len(problems)} problem(s) found — do NOT push.")
    sys.exit(1)
print(f"OK: {n_works} works, XML valid, all internal links and assets resolve.")
sys.exit(0)
