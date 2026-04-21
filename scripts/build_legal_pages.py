#!/usr/bin/env python3
"""
Generate the static HTML for PracticeNow's legal pages and the Feature Updates
release-notes page from the extracted WordPress content.

Reads /tmp/pn_crawl/extract_<slug>.md (markdown-ish dump produced from
content.json) and writes practicenow-static/<slug>/index.html.

The first ~12 lines of each extract are the WordPress nav menu — they are
trimmed before rendering.
"""
import os
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = Path('/tmp/pn_crawl')

PAGES = [
    {
        'slug': 'feature-updates',
        'out': 'feature-updates/index.html',
        'eyebrow': 'Release notes',
        'title': 'Feature updates',
        'subtitle': "What's new in PracticeNow. Recent improvements that save you time.",
        'meta_desc': 'Recent feature updates and improvements to PracticeNow.',
    },
    {
        'slug': 'privacy',
        'out': 'privacy/index.html',
        'eyebrow': 'Legal',
        'title': 'Privacy Policy',
        'subtitle': 'How we collect, store and process your information.',
        'meta_desc': 'PracticeNow privacy policy — how we collect, store and process your information.',
    },
    {
        'slug': 'terms-conditions',
        'out': 'terms-conditions/index.html',
        'eyebrow': 'Legal',
        'title': 'Terms & Conditions',
        'subtitle': 'The terms that govern your use of PracticeNow.',
        'meta_desc': 'PracticeNow terms and conditions for users of the platform.',
    },
    {
        'slug': 'terms-service',
        'out': 'terms-service/index.html',
        'eyebrow': 'Legal',
        'title': 'Terms of Service',
        'subtitle': 'Customer terms of service for studios and teachers using PracticeNow.',
        'meta_desc': 'PracticeNow customer terms of service for studios and teachers.',
    },
]

NAV_PATTERNS = {
    'about us', 'teachers', 'pricing', 'support', 'try it free!', '.', 'try it free',
    'home',
}


def parse_blocks(md_text: str):
    """Convert the simple markdown dump to a list of (kind, value) tuples.

    Skips the WordPress nav menu list at the top (anything before the first
    ## heading that looks like a real heading).
    """
    lines = md_text.splitlines()
    blocks = []
    current_para = []

    def flush_para():
        if current_para:
            text = ' '.join(s.strip() for s in current_para if s.strip())
            if text:
                blocks.append(('p', text))
            current_para.clear()

    in_list = False
    list_items = []

    def flush_list():
        nonlocal in_list, list_items
        if list_items:
            blocks.append(('ul', list_items[:]))
            list_items.clear()
        in_list = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_para()
            flush_list()
            continue
        if line.startswith('## '):
            flush_para(); flush_list()
            blocks.append(('h2', line[3:].strip()))
        elif line.startswith('- '):
            flush_para()
            item = line[2:].strip()
            if item.lower() in NAV_PATTERNS:
                continue
            in_list = True
            list_items.append(item)
        else:
            flush_list()
            current_para.append(line.strip())
    flush_para(); flush_list()

    cleaned = []
    skipping_nav = True
    for kind, val in blocks:
        if skipping_nav:
            if kind == 'h2' and val.lower() not in NAV_PATTERNS:
                skipping_nav = False
            else:
                continue
        cleaned.append((kind, val))
    return cleaned


URL_RE = re.compile(r'(https?://[^\s<>"\)]+)')
EMAIL_RE = re.compile(r'\[email\xa0protected\]|\[email protected\]')


def linkify(text: str) -> str:
    text = html.escape(text)
    text = EMAIL_RE.sub('hello@practicenow.us', text)
    text = URL_RE.sub(
        lambda m: f'<a href="{m.group(1)}" class="text-brand-700 hover:underline" target="_blank" rel="noopener">{m.group(1)}</a>',
        text,
    )
    return text


def render_blocks(blocks, *, is_release_notes: bool) -> str:
    out = []
    for i, (kind, val) in enumerate(blocks):
        if kind == 'h2':
            cls = 'text-2xl font-bold text-slate-900 mt-12 mb-4'
            if is_release_notes and re.match(r'^\[New feature\]|^Enhancement|^New Feature', val, re.I):
                cls = 'text-2xl font-bold text-slate-900 mt-2 mb-3'
            elif is_release_notes and re.match(r'^[A-Z][a-z]+ \d', val):
                cls = 'text-sm font-semibold tracking-[0.18em] uppercase text-brand-600 mt-12 mb-3'
            out.append(f'<h2 class="{cls}">{linkify(val)}</h2>')
        elif kind == 'p':
            out.append(f'<p class="text-slate-700 leading-relaxed mb-4">{linkify(val)}</p>')
        elif kind == 'ul':
            items = '\n'.join(f'  <li>{linkify(it)}</li>' for it in val)
            out.append(
                '<ul class="list-disc pl-6 mb-4 space-y-2 text-slate-700">\n' + items + '\n</ul>'
            )
    return '\n'.join(out)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — PracticeNow</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="https://practicenow.us/{slug}/">
    <link rel="stylesheet" href="../css/tailwind.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="../js/layout.js" defer></script>
    <style>body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}</style>
</head>
<body class="bg-white text-slate-900 antialiased">

<section class="bg-gradient-to-b from-brand-50 to-white py-16 lg:py-20">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm font-semibold tracking-[0.18em] uppercase text-brand-600 mb-3">{eyebrow}</p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 mb-6 leading-tight">{title}</h1>
        <p class="text-lg sm:text-xl text-slate-600 leading-relaxed">{subtitle}</p>
    </div>
</section>

<main class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
{body}
</main>

<section class="py-16 bg-slate-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-2xl font-bold text-slate-900 mb-3">Questions?</h2>
        <p class="text-slate-600 mb-6">Email <a href="mailto:hello@practicenow.us" class="text-brand-700 font-semibold hover:underline">hello@practicenow.us</a> or message us on WhatsApp at <a href="https://wa.me/917899156587" class="text-brand-700 font-semibold hover:underline" target="_blank" rel="noopener">+91 78991 56587</a>.</p>
    </div>
</section>

</body>
</html>
"""


def main():
    for cfg in PAGES:
        src = SRC_DIR / f"extract_{cfg['slug']}.md"
        if not src.exists():
            print('skip (missing):', src)
            continue
        blocks = parse_blocks(src.read_text())
        body = render_blocks(blocks, is_release_notes=(cfg['slug'] == 'feature-updates'))
        out = ROOT / cfg['out']
        out.parent.mkdir(parents=True, exist_ok=True)
        html_doc = PAGE_TEMPLATE.format(body=body, **cfg)
        out.write_text(html_doc)
        print('wrote', out, f'({len(html_doc)} bytes)')


if __name__ == '__main__':
    main()
