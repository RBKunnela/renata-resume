# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Single-page bilingual (EN/FI) portfolio / CV site for Renata Baldissara-Kunnela. Plain static HTML/CSS/JS — no bundler, no framework. Three files do the website: `index.html`, `styles.css`, `script.js`. Two additional HTML files in `docs/` source the CV PDFs (see "CV PDFs" section below).

## Running locally

Open `index.html` directly in a browser, or serve the directory with any static server (e.g. `python -m http.server 8080`). There are no tests, no linter.

The CV PDFs are regenerated via:
```powershell
pwsh ./scripts/build-cvs.ps1
```
This re-renders `docs/cv-en.html` → `docs/cv-en-pdf/...EN.pdf` and `docs/cv-fi.html` → `docs/cv-fi-pdf/...FI.pdf` using headless Chrome. Run after editing either HTML CV source.

## Deploy targets

- **Railway** (primary): `railway.toml` → `Dockerfile` → nginx:alpine serving `/app` on port 8080. The Dockerfile inlines the nginx config; edit it there, not in a separate file. `/health.html` is served as a 200 by nginx directly.
- **Vercel**: `vercel.json` forces correct `Content-Type` headers for `styles.css` and `script.js` — Vercel has historically misdetected these as `text/plain`, which breaks the page. Don't remove those route entries.

When changing the deployed file set, update **all three**: `Dockerfile` COPY lines, `vercel.json` routes if new asset types are added, and the HTML `<link>`/`<script>` tags.

## Architecture notes that aren't obvious from one file

### Bilingual content lives in the DOM

Every translatable element carries both `data-en="…"` and `data-fi="…"` attributes. `setLang(lang)` in `script.js` rewrites `el.innerHTML` from `data-${lang}` across the document. Consequences:

- To add translatable copy, always add both `data-en` and `data-fi`. The visible text between the tags is just the initial render before `setLang` runs.
- `data-en` uses `innerHTML` (HTML allowed, e.g. `<strong>`), but nav links use `textContent`. Form placeholders use `data-placeholder-en` / `data-placeholder-fi` instead.
- The hero typing animation is driven by `translations.{en,fi}.typedPhrases` in `script.js`, **not** by DOM attributes. Update it there when adding phrases.
- Language is persisted in `localStorage` (`portfolio-lang`) and mirrored to the URL hash (`#en` / `#fi`). `#en` and `#fi` are intentionally excluded from smooth-scroll handling in `initSmoothScroll`.

### Theme

`data-theme="dark|light"` on `<html>`. All CSS colors are CSS variables swapped at that boundary. Persisted in `localStorage` as `portfolio-theme`.

### AI / ATS optimization (current approach)

The site is optimized for AI and ATS crawlers through **visible, legitimate** signals only — no hidden text, no fabricated meta tags. The previous approach used `.ai-keywords` hidden divs and `<meta name="ai-skills">` self-rating tags; both were removed (2026-05-15) because modern AI screeners flag hidden-keyword stuffing as manipulation and the self-ratings ("APPROVED-FOR-NEXT-LEVEL" etc.) had no schema meaning.

What's in place now:

- **JSON-LD `schema.org/Person`** (in `<head>`) — the primary machine-readable signal. Includes `hasOccupation`, `hasCredential`, `knowsAbout`, `knowsLanguage`, `alumniOf`, and `subjectOf` (open source projects). This is what Google, Bing, ChatGPT, Claude, and Perplexity actually read.
- **Inline microdata** (`itemscope`/`itemprop`) on the visible DOM — `<body>` is the `Person` root; the hero `<h1>` carries `itemprop="name"`, the summary carries `itemprop="description"`, the contact section carries `itemprop="email"`/`telephone`/`address`. Redundant with JSON-LD but cheap belt-and-braces.
- **`/resume.txt`** — plain-text single-column ATS-clean resume at a stable URL. Easiest target for any automated scraper.
- **`/resume.json`** — JSON Resume v1.0.0 schema (jsonresume.org). The richest machine-readable view.
- **`/llms.txt`** — follows the [llmstxt.org](https://llmstxt.org/) convention; a markdown summary pointing AI agents to the canonical machine-readable views.
- **`robots.txt`** — explicitly allows GPTBot, ClaudeBot, Google-Extended, PerplexityBot, Bytespider, CCBot.

When adding new content, mirror it across `index.html`, `resume.txt`, `resume.json`, and (where it materially changes scope) `llms.txt`. The JSON-LD block in `<head>` should also be updated when work history or certifications change.

### Contact form

Submits to Web3Forms (`https://api.web3forms.com/submit`) as multipart form-data. The access key is in the form HTML (public by design — Web3Forms keys are scoped to a destination email). Success auto-closes the modal after 3s. No backend to configure.

### CV PDFs (single source-of-truth workflow)

The two PDFs at `docs/cv-en-pdf/Renata-Baldissara-Kunnela-CV-EN.pdf` and `docs/cv-fi-pdf/Renata-Baldissara-Kunnela-CV-FI.pdf` are **pre-rendered from HTML sources in this repo**. No external CV builder. No Python ReportLab pipeline (the previous `scripts/generate_cv_fi.py` is archived at `docs/archive/scripts/`).

Single-column, polished, AI-friendly. Designed to satisfy human reviewers AND ATS/AI parsers in one document.

| File | Role |
|---|---|
| `docs/cv-en.html` | Source HTML for the English CV |
| `docs/cv-fi.html` | Source HTML for the Finnish CV |
| `scripts/build-cvs.ps1` | PowerShell script that renders both HTML files to PDFs via headless Chrome |
| `docs/cv-en-pdf/Renata-Baldissara-Kunnela-CV-EN.pdf` | Rendered output, served by the site |
| `docs/cv-fi-pdf/Renata-Baldissara-Kunnela-CV-FI.pdf` | Rendered output, served by the site |

**Edit cycle:** edit HTML → `pwsh ./scripts/build-cvs.ps1` → commit → push → Vercel/Railway deploy.

**Download button:** `script.js#exportToPDF()` is language-aware (picks EN or FI based on `currentLang`) and serves the pre-rendered PDF directly. It does NOT call `window.print()`.

**Critical CSS constraints for ATS-friendly PDF rendering (do not violate):**

- **No `letter-spacing` on h2** — wide tracking breaks PDF word extraction. `letter-spacing: 1.4pt` causes parsers to see "S UMMA RY" instead of "SUMMARY".
- **No `::before` / `::after` accent elements on the header** — pseudo-elements with positioning can invert PDF text-paint order, pushing the name/contact below body text in the extraction stream. Use plain `border-bottom` on the header instead.
- **No `position: absolute` on list bullet markers** — absolute-positioned `::before` dots grouped section headers separately from their content in the extraction. Use standard `list-style: disc` with `::marker { color: var(--accent) }` for colored bullets that stay in flow.
- **Inline microdata + JSON-LD only** — never re-introduce hidden keyword divs.

The full text-extraction order (what an ATS sees) must read top-to-bottom: name, role, status, contact line, SUMMARY heading, summary text, STRENGTHS heading, strengths content, KEY ACHIEVEMENTS heading, achievements content, EXPERIENCE heading, role blocks in order, SKILLS heading, keywords block, skill rows, FOCUS AREAS, FEATURED PROJECTS, EDUCATION, CERTIFICATIONS, LANGUAGES. If you change the CSS and the extraction order breaks, you've hit one of the constraints above.

### Keyboard shortcuts

`Alt+1` / `Alt+e` → EN, `Alt+2` / `Alt+f` → FI, `Alt+t` → theme toggle. Escape closes the contact modal.

## Conventions

- No build step means no transpilation: write browser-native ES202x only. Font Awesome loads from cdnjs.
- Keep `styles.css` as the single stylesheet. There is no inline `<style>` in `index.html`.
- Commit style from git log: short imperative subject, often prefixed with the area (`Fix contact form: …`, `Remove … stat — …`).
