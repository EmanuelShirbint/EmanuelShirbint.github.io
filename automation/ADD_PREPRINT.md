# Procedure — add a newly published preprint to the site

This file is the single source of truth for the automated "publish preprint"
job **and** for any manual run. Follow it exactly. The site is a hand-authored
static site (no build step, `.nojekyll`), so every page is edited directly.

Golden rule: **copy an existing record and change only the facts.** Never invent
results, figures, or claims beyond the official abstract. Every new work is a
preprint → status is always "Not peer-reviewed" unless the source clearly says
otherwise.

---

## 0. Inputs you need before editing

For each new preprint, collect:

- `title` — exact title from Preprints.org
- `authors` — full author list, in order (usually just "Emanuel Shirbint")
- `date` — posting date, `YYYY-MM-DD` and human form "4 August 2026"
- `doi` — e.g. `10.20944/preprints202608.0212.v1`
- `manuscript` — e.g. `202608.0212` → page `https://www.preprints.org/manuscript/202608.0212`
- `abstract` — full abstract text (authoritative summary; do not paraphrase)
- `keywords` — semicolon-separated list from the paper
- `slug` — short kebab-case id, e.g. `reinforcement-learning-contour`
- `type` — one or more of: `Conceptual Framework`, `Empirical Study`,
  `Synthetic Controlled Pilot` (pick from the abstract)
- `area(s)` — one or two of: `governed-agent-systems`, `llm-safety-evaluation`,
  `human-medical-digital-twins`, `ai-ethics-governance`, `clinical-ai`,
  `data-ai-architecture`
- `series` — an existing series slug under `/series/`, or a new one if the work
  starts a distinct programme

Download the official PDF to `assets/research/<slug>.pdf`.

## 1. Dedupe (skip if already published)

If `<doi>` already appears in `publications/index.html`, the work is already on
the site — **stop, do nothing** for that preprint.

## 2. Create the record (3 files + PDF)

Copy an existing record folder as the template — the closest match in `type`,
e.g. `research/works/institutional-volition-systemic-error/` for a conceptual
framework. Create:

- `research/works/<slug>/index.html` — replace title, description, canonical URL,
  all `citation_*` meta, the JSON-LD block (headline/name/datePublished/abstract/
  keywords/identifier/url/encoding), byline, `artmeta` rows (date, DOI, official
  source, PDF), the `actions` buttons (drop the "Presentation" button unless a
  presentation PDF exists), the abstract, the numbered body sections
  (Research problem / Contribution / Evidence status / Related research / Cite),
  and the APA/Chicago/BibTeX/RIS citation panes. Keep the header, nav, footer,
  and the `<script>` block byte-for-byte from the template.
- `research/works/<slug>/cite.bib` — BibTeX (`@misc{shirbint2026<slugnodashes>, …}`)
- `research/works/<slug>/cite.ris` — RIS record
- `assets/research/<slug>.pdf` — the downloaded PDF

## 3. Update the index pages

Add the work (newest first) everywhere it belongs. Use the entry markup already
present on each page as the pattern.

1. **`index.html`** (homepage)
   - bump `<span>N records</span>` by 1
   - prepend a `<li class="entry">` card to the Latest Research `<ol class="contents">`
   - add to "Most Significant Contributions" as `01` and renumber the rest
   - if the series is new, add it to the "Research Series" aside list
2. **`publications/index.html`**
   - bump `Preprints &amp; conceptual frameworks (N)` by 1
   - prepend an `<li>` to the preprints `<ol class='references'>`
3. **`research/index.html`**
   - prepend a `ScholarlyArticle` to the JSON-LD `hasPart` array
   - prepend an `<li class="entry" …>` to the correct year group in the
     Chronological Archive (set `data-year`, `data-type`, `data-status="preprint"`,
     `data-area="…"`, `data-doi`, and a lowercase `data-search` string of
     title + authors + doi + keywords)
   - insert into the alphabetical Title Index in sort order
   - in the Research-Area Index, bump each relevant area's `(N)` and add a `<li>`;
     create a new `idx-block` if the area had none
   - in the Author Index, bump Emanuel Shirbint's `— N record(s):` and prepend the
     new year link (add co-authors if any)
4. **Area pages** — for each area in `area(s)`, e.g. `governed-agent-systems/index.html`:
   bump `Works in this area (N)`, prepend the entry, and add the series to
   "Related series" if new.
5. **Series**
   - existing series `series/<series>/index.html`: prepend the work to
     "Constituent works" and update the count/status line
   - new series: create `series/<series>/index.html` (copy an existing series
     page), add an `idx-block` to `series/index.html`, and add a `<url>` for it
     to `sitemap.xml`
6. **Feeds** — `feed.xml` and `research/feed.xml`:
   set `<lastBuildDate>` to today and prepend an `<item>` (title, link, guid,
   dc:creator, `<category>Not peer-reviewed</category>`, pubDate, ~600-char
   description).
7. **`sitemap.xml`** — add a `<url>` for `/research/works/<slug>/` (and the new
   series if any); set `<lastmod>` to today on every page you changed.

## 4. Verify (gate before pushing)

```
python3 automation/verify_site.py
```

It must print `OK` and exit 0. If it reports FAIL, **do not push** — fix the
issue, or if unsure, stop and notify the maintainer with the failure text.

## 5. Commit & push

```
git add -A
git commit -m "Add preprint: <short title> (DOI <doi>)"
git push origin main
```

GitHub Pages redeploys automatically in ~1–2 minutes; the live site then shows
the new record and the incremented record count.

## Canonical facts (never contradict these)

- Author: **Emanuel Shirbint** — ORCID `0009-0004-8538-7140`,
  Scopus `57223002583`, Independent Researcher, Tel Aviv, Israel
- Repo: `https://github.com/EmanuelShirbint/EmanuelShirbint.github.io`, branch `main`
- Site: `https://emanuelshirbint.github.io/`
- Preprints are **not peer-reviewed**; state this on every preprint record.
