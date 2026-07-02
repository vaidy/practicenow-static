# practicenow.us — static marketing site (repo)

Static HTML/CSS/JS marketing site for **practicenow.us**, hosted on **GitHub Pages**.

| Path | Purpose |
|------|---------|
| `docs/` | **Published** web root (only this folder is deployed to GitHub Pages) |
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

## Pages (under `docs/`)

| URL | File |
| --- | --- |
| `/` | `docs/index.html` |
| `/about-us/` | `docs/about-us/index.html` |
| `/teachers/` | `docs/teachers/index.html` |
| `/features/` | `docs/features/index.html` |
| `/support/` | `docs/support/index.html` |
| `/privacy/` | `docs/privacy/index.html` |
| `/terms-conditions/` | `docs/terms-conditions/index.html` |
| `/terms-service/` | `docs/terms-service/index.html` |

External: **app** / pricing → `https://app.practicenow.us`

---

## Local preview

```sh
cd practicenow-static
npm run serve
# open http://localhost:8080
```

Or: `python3 -m http.server 8080 --directory docs`

---

## Rebuild Tailwind CSS

```sh
npm run build:css
```

Source: `docs/css/input.css` → output `docs/css/tailwind.css`

---

## Deploy (GitHub Pages)

1. Push `main` to `https://github.com/vaidy/practicenow-static.git`
2. **Settings → Pages:** branch `main`, folder **`/docs`** (not repo root)
3. Custom domain: `practicenow.us` (`docs/CNAME`)
4. Apex DNS → GitHub Pages IPs (see GitHub Pages docs)

**Important:** Publishing from repo root exposes `README.md`, `scripts/`, etc. at `practicenow.us/<filename>`. Always use **`/docs`** as the Pages source.

---

## Editing content

- Marketing pages: edit HTML under `docs/`
- Shared header/footer: `docs/js/layout.js`
- Legal pages: `python3 scripts/build_legal_pages.py` (writes under `docs/`)

---

## Safety

- No code from the old WordPress install is executed on this site
- JS/CSS is hand-written or compiled Tailwind
- Images under `docs/images/wp/` were validated before commit
