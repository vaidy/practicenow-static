/**
 * PracticeNow static site — shared layout.
 * Injects: favicon, header (sticky), footer, floating WhatsApp button.
 * No external script dependencies, no analytics, no tracking.
 *
 * BASE_PATH detection allows the same code to work both:
 *  - locally at /  (e.g. python -m http.server in practicenow-static/)
 *  - from a custom domain at /
 *  - from a github.io project subpath /<repo>/
 */
(function () {
    'use strict';

    const APP_TRIAL_URL = 'https://app.practicenow.us/trial/scale-non-teaching-tasks';
    const APP_PRICING_URL = 'https://app.practicenow.us/pricing';
    // Phone for the floating WhatsApp button — pulled from PracticeNow footer.
    // To update: change WHATSAPP_NUMBER below; format is E.164 without "+".
    const WHATSAPP_NUMBER = '917899156587';
    const WHATSAPP_GREETING = "Hi PracticeNow team — I'd like to know more.";

    function getBasePath() {
        const path = window.location.pathname || '/';
        const segments = path.split('/').filter(Boolean);
        if (segments.length === 0) return '';
        const first = segments[0];
        // Known top-level subdirs that indicate we are at site root.
        const knownTop = new Set([
            'about', 'teachers', 'support', 'features',
            'privacy',
            'terms-conditions', 'terms-service',
            'index.html'
        ]);
        if (knownTop.has(first) || first.endsWith('.html')) return '';
        // Otherwise treat the first segment as the project subpath
        // (e.g. github.io/practicenow-static/).
        return '/' + first;
    }

    const BASE = getBasePath();
    const url = (p) => (BASE + p).replace(/\/+/g, '/');

    const NAV = [
        { label: 'Features', href: url('/features/') },
        { label: 'Teachers', href: url('/teachers/') },
        { label: 'Support', href: url('/support/') },
        { label: 'Pricing', href: APP_PRICING_URL },
        { label: 'About', href: url('/about/') }
    ];

    function ensureFavicon() {
        if (document.querySelector('link[rel="icon"]')) return;
        const link = document.createElement('link');
        link.rel = 'icon';
        link.type = 'image/svg+xml';
        // Tiny inline indigo "PN" mark
        const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' +
            '<rect width="64" height="64" rx="14" fill="#4f46e5"/>' +
            '<text x="32" y="42" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="800" font-size="30" fill="white">PN</text>' +
            '</svg>';
        link.href = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);
        document.head.appendChild(link);
    }

    function buildHeader() {
        const isCurrent = (href) => {
            if (/^https?:\/\//.test(href)) return false;
            const path = window.location.pathname.replace(/\/+$/, '/') || '/';
            const target = href.replace(/\/+$/, '/') || '/';
            if (target === url('/') ) return path === url('/') || path === '/';
            return path.startsWith(target);
        };

        const navLinks = NAV.map(item => {
            const active = isCurrent(item.href);
            const cls = active
                ? 'text-brand-700 font-semibold'
                : 'text-slate-700 hover:text-brand-700';
            return `<a href="${item.href}" class="${cls} transition-colors px-3 py-2 text-sm">${item.label}</a>`;
        }).join('');

        const navLinksMobile = NAV.map(item => {
            return `<a href="${item.href}" class="block px-4 py-3 text-slate-700 hover:bg-slate-50 hover:text-brand-700 text-base font-medium">${item.label}</a>`;
        }).join('');

        const html = `
<header class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <a href="${url('/')}" class="flex items-center gap-2 group">
        <span class="inline-flex items-center justify-center w-9 h-9 rounded-xl bg-brand-600 text-white font-extrabold text-sm shadow-sm group-hover:bg-brand-700 transition-colors">PN</span>
        <span class="text-lg font-extrabold tracking-tight text-slate-900">PracticeNow</span>
      </a>
      <nav class="hidden md:flex items-center gap-1" aria-label="Primary">
        ${navLinks}
      </nav>
      <div class="hidden md:flex items-center gap-3">
        <a href="${APP_TRIAL_URL}" class="inline-flex items-center px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm hover:shadow transition-all">Try it free</a>
      </div>
      <button type="button" class="md:hidden inline-flex items-center justify-center w-10 h-10 rounded-lg text-slate-700 hover:bg-slate-100" aria-label="Open menu" data-pn-menu-toggle>
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </div>
  <div class="md:hidden border-t border-slate-200 bg-white hidden" data-pn-mobile-drawer>
    ${navLinksMobile}
    <div class="border-t border-slate-200 mt-2 pt-2 px-4 pb-4 flex flex-col gap-2">
      <a href="${APP_TRIAL_URL}" class="block w-full text-center px-4 py-2.5 rounded-lg bg-brand-600 text-white font-semibold">Try it free</a>
    </div>
  </div>
</header>`;
        const wrap = document.createElement('div');
        wrap.innerHTML = html.trim();
        document.body.insertBefore(wrap.firstChild, document.body.firstChild);

        const toggle = document.querySelector('[data-pn-menu-toggle]');
        const drawer = document.querySelector('[data-pn-mobile-drawer]');
        if (toggle && drawer) {
            toggle.addEventListener('click', () => {
                drawer.classList.toggle('hidden');
            });
        }
    }

    function buildFooter() {
        const year = new Date().getFullYear();
        const html = `
<footer class="bg-slate-900 text-slate-300 mt-24">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-12">
      <div class="lg:col-span-1">
        <a href="${url('/')}" class="flex items-center gap-2 mb-4">
          <span class="inline-flex items-center justify-center w-9 h-9 rounded-xl bg-brand-600 text-white font-extrabold text-sm">PN</span>
          <span class="text-lg font-extrabold text-white">PracticeNow</span>
        </a>
        <p class="text-sm text-slate-400 leading-relaxed">
          The all-in-one business app for independent teachers. We accelerate teachers' growth with online payments, class management, stories &amp; community engagement.
        </p>
      </div>
      <div>
        <h3 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">Product</h3>
        <ul class="space-y-3 text-sm">
          <li><a href="${url('/features/')}" class="text-slate-400 hover:text-white transition-colors">Features</a></li>
          <li><a href="${APP_PRICING_URL}" class="text-slate-400 hover:text-white transition-colors">Pricing</a></li>
          <li><a href="${url('/teachers/')}" class="text-slate-400 hover:text-white transition-colors">Teachers</a></li>
          <li><a href="${APP_TRIAL_URL}" class="text-slate-400 hover:text-white transition-colors">Try it free</a></li>
        </ul>
      </div>
      <div>
        <h3 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">Company</h3>
        <ul class="space-y-3 text-sm">
          <li><a href="${url('/about/')}" class="text-slate-400 hover:text-white transition-colors">About us</a></li>
          <li><a href="${url('/support/')}" class="text-slate-400 hover:text-white transition-colors">Support</a></li>
          <li><a href="${url('/privacy/')}" class="text-slate-400 hover:text-white transition-colors">Privacy</a></li>
          <li><a href="${url('/terms-conditions/')}" class="text-slate-400 hover:text-white transition-colors">Terms &amp; Conditions</a></li>
          <li><a href="${url('/terms-service/')}" class="text-slate-400 hover:text-white transition-colors">Terms of Service</a></li>
        </ul>
      </div>
      <div>
        <h3 class="text-sm font-semibold text-white uppercase tracking-wider mb-4">Contact</h3>
        <ul class="space-y-3 text-sm">
          <li><a href="mailto:hello@practicenow.us" class="text-slate-400 hover:text-white transition-colors">hello@practicenow.us</a></li>
          <li><a href="https://wa.me/${WHATSAPP_NUMBER}" target="_blank" rel="noopener" class="text-slate-400 hover:text-white transition-colors">+91 78991 56587</a></li>
          <li class="text-slate-400 leading-relaxed">B404, Mahaveer Riviera,<br>Achappa Layout, Off 24th Main,<br>JP Nagar 5th Phase,<br>Bangalore - 560078</li>
        </ul>
      </div>
    </div>
    <div class="mt-12 pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
      <p class="text-xs text-slate-500">&copy; ${year} Multunus Software Pvt. Ltd. All rights reserved.</p>
      <p class="text-xs text-slate-500">Empowering independent teachers since 2020.</p>
    </div>
  </div>
</footer>`;
        const wrap = document.createElement('div');
        wrap.innerHTML = html.trim();
        document.body.appendChild(wrap.firstChild);
    }

    function buildWhatsApp() {
        const a = document.createElement('a');
        a.href = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_GREETING)}`;
        a.target = '_blank';
        a.rel = 'noopener';
        a.setAttribute('aria-label', 'Chat with PracticeNow on WhatsApp');
        a.className = 'fixed bottom-6 right-6 z-50 inline-flex items-center justify-center w-14 h-14 rounded-full bg-[#25D366] text-white shadow-lg hover:shadow-xl hover:scale-105 transition-all';
        a.innerHTML = `
<svg viewBox="0 0 32 32" width="28" height="28" fill="currentColor" aria-hidden="true">
  <path d="M16 .5C7.44.5.5 7.44.5 16c0 2.83.74 5.49 2.04 7.81L.5 31.5l7.86-2.06A15.45 15.45 0 0 0 16 31.5c8.56 0 15.5-6.94 15.5-15.5S24.56.5 16 .5Zm0 28.13c-2.51 0-4.86-.69-6.87-1.88l-.49-.29-4.66 1.22 1.24-4.54-.32-.5A12.62 12.62 0 0 1 3.38 16C3.38 9.05 9.05 3.38 16 3.38S28.62 9.05 28.62 16 22.95 28.63 16 28.63Zm7.06-9.46c-.39-.2-2.29-1.13-2.65-1.26-.36-.13-.62-.2-.88.2-.26.39-1 1.26-1.23 1.52-.23.26-.45.29-.84.1-.39-.2-1.64-.6-3.13-1.92-1.16-1.03-1.94-2.31-2.17-2.7-.23-.39-.02-.6.17-.79.18-.18.39-.45.59-.68.2-.23.26-.39.39-.65.13-.26.07-.49-.03-.68-.1-.2-.88-2.13-1.21-2.92-.32-.77-.65-.66-.88-.67-.23-.01-.49-.01-.75-.01-.26 0-.68.1-1.04.49-.36.39-1.36 1.33-1.36 3.24s1.4 3.76 1.59 4.02c.2.26 2.75 4.2 6.66 5.89.93.4 1.65.64 2.22.82.93.3 1.78.26 2.45.16.75-.11 2.29-.94 2.62-1.84.32-.91.32-1.68.23-1.84-.1-.16-.36-.26-.75-.45Z"/>
</svg>`;
        document.body.appendChild(a);
    }

    function preventScrollUnderHeader() {
        // Add top padding for the fixed header, only if body isn't already padded.
        const cls = document.body.className || '';
        if (!/\bpt-\d/.test(cls)) {
            document.body.classList.add('pt-16');
        }
    }

    function init() {
        ensureFavicon();
        preventScrollUnderHeader();
        buildHeader();
        buildFooter();
        buildWhatsApp();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
