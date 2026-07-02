# practicenow.us — static marketing site (repo)

Static HTML/CSS/JS marketing site for **practicenow.us**, hosted on **GitHub Pages**.

| Path | Purpose |
|------|---------|
| `site/` | **Published** web root (only this folder is deployed to GitHub Pages) |
| `scripts/` | Build helpers (legal pages, teachers page, image download) — **not published** |
| `README.md` | Developer notes — **not published** |

The product app remains at **app.practicenow.us**. CTAs point there.

---

## Why static?

In **April 2026** we replaced the legacy WordPress marketing site with this static rebuild:

- No PHP, database, or WordPress admin surface
- Hand-written HTML + Tailwind CSS
- Hosted on GitHub Pages behind Cloudflare

---

## Pages (under `site/`)

| URL | File |
| --- | --- |
| `/` | `site/index.html` |
| `/about-us/` | `site/about-us/index.html` |
| `/teachers/` | `site/teachers/index.html` |
| `/features/` | `site/features/index.html` |
| `/support/` | `site/support/index.html` |
| `/privacy/` | `site/privacy/index.html` |
| `/terms-conditions/` | `site/terms-conditions/index.html` |
| `/terms-service/` | `site/terms-service/index.html` |

External: **app** / pricing → `https://app.practicenow.us`

---

## Local preview

```sh
cd practicenow-static
npm run serve
# open http://localhost:8080
```

Or: `python3 -m http.server 8080 --directory site`

---

## Rebuild Tailwind CSS

```sh
npm run build:css
```

Source: `site/css/input.css` → output `site/css/tailwind.css`

---

## Deploy (GitHub Pages)

1. Push `main` to `https://github.com/vaidy/practicenow-static.git`
2. **Settings → Pages:** branch `main`, folder **`/site`** (not repo root)
3. Custom domain: `practicenow.us` (`site/CNAME`)
4. Apex DNS → GitHub Pages IPs (see GitHub Pages docs)

**Important:** Publishing from repo root exposes `README.md`, `scripts/`, etc. at `practicenow.us/<filename>`. Always use **`/site`** as the Pages source.

---

## Editing content

- Marketing pages: edit HTML under `site/`
- Shared header/footer: `site/js/layout.js`
- Legal pages: `python3 scripts/build_legal_pages.py` (writes under `site/`)

---

## Safety

- No code from the old WordPress install is executed on this site
- JS/CSS is hand-written or compiled Tailwind
- Images under `site/images/wp/` were validated before commit
