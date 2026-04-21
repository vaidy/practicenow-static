# practicenow.us — static marketing site

Static HTML/CSS/JS clone of the previous WordPress marketing site at `practicenow.us`.

Hosted on **GitHub Pages** with the custom domain **practicenow.us**.

The product app remains at **app.practicenow.us** (unchanged). All "Try it Free" / "Pricing" / sign-in CTAs point there.

---

## Why a static site?

The previous WordPress site was infected with malware and was time-consuming to maintain. This static rebuild:

- Has zero dynamic surface area (no PHP, no DB, no admin login).
- Reuses the design system from the Sparktutor marketing site (Tailwind, Inter, indigo brand colour).
- Is hosted on GitHub Pages — free, fast, with HTTPS.
- Costs nothing to operate.

---

## Pages

| URL | Purpose |
| --- | --- |
| `/` | Home |
| `/about/` | About PracticeNow / Spark |
| `/teachers/` | Customer studios + testimonials |
| `/features/` | All 9 product capabilities, in one page |
| `/feature-updates/` | Release notes |
| `/support/` | Onboarding + how to contact us |
| `/privacy/` | Privacy policy |
| `/terms-conditions/` | User terms & conditions |
| `/terms-service/` | Customer terms of service |

External links:

- **App / sign-in / pricing:** `https://app.practicenow.us`
- **WhatsApp:** `https://wa.me/917899156587`
- **Help center:** `https://practicenow.crisp.help`

---

## Local preview

```sh
cd practicenow-static
python3 -m http.server 8080
# open http://localhost:8080
```

## Rebuild Tailwind CSS

`css/tailwind.css` is precompiled and committed. Rebuild it whenever you add new Tailwind utility classes to any HTML file (Tailwind v4 only emits the classes it sees in source files):

```sh
# from this directory:
../marketing/node_modules/.bin/tailwindcss -i ./css/input.css -o ./css/tailwind.css --minify

# or, after `npm install`:
npm run build:css
```

Source: `css/input.css` (Tailwind v4 with `@theme` brand tokens and `@source` globs that scan all HTML and JS in this folder).

---

## Layout & design

- Tailwind CSS is precompiled in `css/tailwind.css` (copied from the Sparktutor marketing site).
- `js/layout.js` injects the header, footer, favicon and floating WhatsApp button on every page.
  - Brand wordmark: `PracticeNow` next to a small "PN" rounded-square logo.
  - Nav: Home · Features · Teachers · Pricing (→ app) · About · Support.
  - CTA: **Try it Free** → `https://app.practicenow.us/trial/scale-non-teaching-tasks`.

To change nav/footer content site-wide, edit only `js/layout.js`.

---

## Images

All images are downloaded from the old WordPress site into `images/wp/` after passing magic-byte validation (`scripts/download_images.py`).

Only `jpg / png / webp / svg` are kept. SVGs containing `<script>` tags are rejected.

---

## Deploy to GitHub Pages

This subfolder is a self-contained git repo (`git init` already done).

1. Create a new GitHub repo, e.g. `practicenow/practicenow-website`.
2. Add the remote and push:

   ```sh
   git remote add origin git@github.com:practicenow/practicenow-website.git
   git branch -M main
   git push -u origin main
   ```

3. In **Settings → Pages**:
   - Source: `main` branch, root (`/`).
   - Custom domain: `practicenow.us` — when you're ready to switch DNS, rename `CNAME.production` → `CNAME` and commit. (It's stored aside so the github.io preview URL works without DNS changes.)
   - Enforce HTTPS: ✅
4. At the DNS provider for `practicenow.us`, point the apex `A` records (or `ALIAS` / `ANAME`) at GitHub Pages IPs:

   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```

   (`app.practicenow.us` should remain on its current `CNAME` to the product app.)

---

## Editing content

All pages are hand-written HTML using Tailwind utility classes.

- Marketing pages (home / about / features / support / teachers): edit the `index.html` directly.
- Legal + release-notes (`privacy`, `terms-conditions`, `terms-service`, `feature-updates`): regenerate via

  ```sh
  python3 scripts/build_legal_pages.py
  ```

  The script reads `/tmp/pn_crawl/extract_<slug>.md` (the cleaned markdown extract from the old WordPress HTML).

---

## Safety notes

- No part of this site executes any code copied from the old WordPress install.
- All JS/CSS in `js/` and `css/` is hand-written or known-good Tailwind output.
- All downloaded images were re-validated via magic-byte sniffing before being committed.
