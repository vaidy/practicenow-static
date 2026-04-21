#!/usr/bin/env python3
"""Generate practicenow-static/teachers/index.html with featured testimonials
and a 'trusted by' grid of all customer studios."""
import os, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = json.load(open(os.path.join(ROOT, "images/wp/_manifest.json")))

# Map studio image filename → (display name, subdomain).
# Subdomains pulled from earlier crawl of teachers/ internal links.
STUDIOS = [
    ("aayana.jpg", "Aayana", "aayana.practicenow.us"),
    ("abs-aesthetics.jpg", "ABS Aesthetics", "absaesthetics.practicenow.us"),
    ("absolute-yoga.jpg", "Absolute Yoga", "absoluteyoga.practicenow.us"),
    ("amrutha-bindu-yoga.jpg", "Amrutha Bindu Yoga", "amruthabindu.practicenow.us"),
    ("anubhooti-yoga.jpg", "Anubhooti Yoga", "anubhootiyoga.practicenow.us"),
    ("Attakkalari.jpg", "Attakkalari", "attakkalari.practicenow.us"),
    ("atha-yoga-shala.jpg", "Atha Yoga Shala", "athayogashala.practicenow.us"),
    ("athmayaan-athayaan.jpg", "Atmayaan", "atmayaan.practicenow.us"),
    ("atmayogashala.jpg", "Atma Yoga Shala", "atmayogashala.practicenow.us"),
    ("aware-yoga.jpg", "Aware Yoga", "awareyoga.practicenow.us"),
    ("ayuh-yoga.jpg", "The Ayuh Project", "theayuhproject.practicenow.us"),
    ("balance-Yoga.jpg", "Balance Yoga", "balanceyoga.practicenow.us"),
    ("Bhumi-Anga-yoga.jpg", "Bhumi Anga Yoga", "bhumianga.practicenow.us"),
    ("Chaitanya-Wellness.jpg", "Chaitanya Wellness", "chaitanya.practicenow.us"),
    ("chakra-project.jpg", "Chakra Project", "chakraproject.practicenow.us"),
    ("chennai-yoga-studio.jpg", "Chennai Yoga", "chennaiyoga.practicenow.us"),
    ("dhimahi.jpg", "Dhimahi", "dhimahi.practicenow.us"),
    ("dorris-yoga.jpg", "Dorris Yoga", "dorrisyoga.practicenow.us"),
    ("Eka-Meditation.jpg", "Eka Meditation", "eka.practicenow.us"),
    ("ekatra-yoga.jpg", "Ekatra Yoga", "ekatrayoga.practicenow.us"),
    ("ekatva.jpg", "Ekatva", "ekatva.practicenow.us"),
    ("finding-your-yoga.jpg", "Finding Your Yoga", "fyy.practicenow.us"),
    ("genesis.jpg", "Genesis Life", "genesislife.practicenow.us"),
    ("gurukripa.jpg", "Gurukripa", "gurukripa.practicenow.us"),
    ("Indea-Yoga.jpg", "Indea Yoga", "indeayoga.practicenow.us"),
    ("isha-space-for-arts.jpg", "Isha Space for Arts", "ishaspace.practicenow.us"),
    ("Journey-of-yoga.jpg", "Journey of Yoga", "joy.practicenow.us"),
    ("little-world-of-yoga.jpg", "Little World of Yoga", "littleworldofyoga.practicenow.us"),
    ("lockdown-fitness.jpg", "Lockdown Fitness", "lockdownfitness.practicenow.us"),
    ("lta.jpg", "LTA School of Beauty", "ltaschoolofbeauty.practicenow.us"),
    ("movement-with-komal.jpg", "Movement with Komal", "movementwithkomal.practicenow.us"),
    ("pancha-yoga.jpg", "Pancha Yoga", "panchayoga.practicenow.us"),
    ("param-yoga.jpg", "Param Yoga", "paramyoga.practicenow.us"),
    ("prasanna-yoga.jpg", "Prasanna Yoga", "prasannayoga.practicenow.us"),
    ("Samyak-Yoga.jpg", "Samyak Yoga", "samyakyoga.practicenow.us"),
    ("samyama.jpg", "Samyama", "samyama.practicenow.us"),
    ("sanjay-yoga.jpg", "Sanjay Yoga", "sanjayyoga.practicenow.us"),
    ("sense-22-yoga.jpg", "Sense 22 Yoga", "sense22yoga.practicenow.us"),
    ("sharshmi-yoga.jpg", "Dharshmi Yoga", "dharshmi.practicenow.us"),
    ("swadhyay-yoga-shala.jpg", "Swadhyay Yoga Shala", "swadhyayyogashala.practicenow.us"),
    ("taamara-rasa.jpg", "Taamara Rasa", "taamararasa.practicenow.us"),
    ("the-yoga-studio.jpg", "The Yoga Studio", None),
    ("Uddiyana-yoga.jpg", "Uddiyana Yoga", "uddiyanayoga.practicenow.us"),
    ("Wellnesutra.jpg", "Wellnessutra", "wellnessutra.practicenow.us"),
    ("yoga-bharata.jpg", "Yoga Bharata", "yogabharata.practicenow.us"),
    ("yogabhyasa.jpg", "Yoga Bhyasa", "yogabhyasa.practicenow.us"),
    ("yoga-for-cure.jpg", "Yoga for Cure", "yogaforcure.practicenow.us"),
    ("yogahitha.jpg", "Yoga Hitha", "yogahitha.practicenow.us"),
    ("yoga-natya.jpg", "Yog Natya", "yognatya.practicenow.us"),
    ("yogaplus.jpg", "Yoga Plus", "yogaplus.practicenow.us"),
    ("yogaranya.jpg", "Yoga Ranya", "yogaranya.practicenow.us"),
    ("yogasakhi.jpg", "Yoga Sakhi", "yogasakhi.practicenow.us"),
    ("yoga-yatri.jpg", "Yoga Yatri", "yogayatri.practicenow.us"),
    ("6-am-yoga-1.jpg", "6 AM Yoga", "6am.practicenow.us"),
    ("yoga-sadhana-mandir.jpg", "Yoga Sadhana Mandir", "ysmyoga.practicenow.us"),
]

# Featured testimonials (from /teachers/ page).
TESTIMONIALS = [
    {
        "img": "Komal-150x150.png",
        "name": "Komal Dubey",
        "title": "Freelance Yoga & Animal Flow Instructor, Mumbai",
        "subdomain": "movementwithkomal.practicenow.us",
        "quote": "I do not have to follow up for payments or track student attendance anymore. It saves me energy and time, which I can use in coming up with workshops or planning my sequences. PracticeNow is like my online studio. It makes me look more professional, as I schedule classes that learners can join in one click rather than coordinating over WhatsApp.",
    },
    {
        "img": "santhanam-100x100.jpg",
        "name": "Santhanam Sridharan",
        "title": "Senior Yoga Teacher",
        "subdomain": "swadhyayyogashala.practicenow.us",
        "quote": "PracticeNow gave my school a clean, professional online presence. Students can find class times, pay, and join — without me lifting a finger.",
    },
    {
        "img": "rohini-100x100.jpg",
        "name": "Rohini Manohar",
        "title": "Founder, Chakra Project",
        "subdomain": "chakraproject.practicenow.us",
        "quote": "The team at PracticeNow listens. Every feature I asked for in my first three months has shipped. They genuinely care about teachers' growth.",
    },
    {
        "img": "vikar-100x100.jpg",
        "name": "Vikas Shenoy",
        "title": "Founder, Pancha Yoga",
        "subdomain": "panchayoga.practicenow.us",
        "quote": "I no longer have to chase fees. I no longer have to maintain spreadsheets. I no longer have to share links every class. PracticeNow handles all of it.",
    },
    {
        "img": "Sivakumar-Puthenmadathil-yoga-teacher.jpg",
        "name": "Sivakumar Puthenmadathil",
        "title": "Yoga Teacher",
        "subdomain": "chennaiyoga.practicenow.us",
        "quote": "Even my older students manage their own subscriptions on PracticeNow. The interface is genuinely simple — that's its biggest superpower.",
    },
    {
        "img": "jaya-ramesh-yoga-teacher.jpg",
        "name": "Jaya Ramesh",
        "title": "Yoga Teacher",
        "subdomain": "ekatva.practicenow.us",
        "quote": "I run multiple class formats — group, personal, workshops. PracticeNow handles all of them in one place, with one set of plans and one set of payments.",
    },
    {
        "img": "Chandraprakash-R-yoga-teacher.jpg",
        "name": "Chandraprakash R",
        "title": "Yoga Teacher",
        "subdomain": "samyama.practicenow.us",
        "quote": "International payments used to be a nightmare. Now my students in 6 countries pay me in their local currency, and I get my money in INR. Zero forex headaches.",
    },
    {
        "img": "rani-naveen-yoga-teacher.jpg",
        "name": "Rani Naveen",
        "title": "Founder, Prerana Yoga Shala",
        "subdomain": "preranayogashala.practicenow.us",
        "quote": "Subscriptions, attendance, reminders — all on autopilot. I finally feel like I'm running a real business, not chasing receipts.",
    },
    {
        "img": "Nita-Saini-yoga-teacher.jpg",
        "name": "Nita Saini",
        "title": "Yoga Teacher",
        "subdomain": None,
        "quote": "The free trial gave me everything I needed to convince myself. By day three I had migrated all my students. By day ten I'd run my first online workshop.",
    },
    {
        "img": "Soorya-Senthil-Kumar-yoga-teacher.jpg",
        "name": "Soorya Senthil Kumar",
        "title": "Yoga Teacher",
        "subdomain": None,
        "quote": "I came to PracticeNow for the payments. I stayed for the storyteller — automated WhatsApp sequences that warm up new inquiries while I sleep.",
    },
]

def img(path):
    """Return image path if downloaded, else placeholder."""
    full = "images/wp/" + path
    if os.path.exists(os.path.join(ROOT, full)):
        return full
    # try url-encoded version
    return "images/wp/" + path

def render_testimonial(t):
    avatar = img(t["img"])
    sub = ""
    if t.get("subdomain"):
        sub = f'<a href="https://{t["subdomain"]}" target="_blank" rel="noopener" class="text-brand-600 hover:text-brand-700 text-sm font-medium">{t["subdomain"]}</a>'
    return f'''
<article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8">
    <svg class="w-8 h-8 text-brand-600 mb-4" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true">
        <path d="M9.4 8h6.4l-3.2 6.4h3.2v9.6H6.2V14.4L9.4 8Zm10.6 0h6.4l-3.2 6.4h3.2v9.6h-9.6V14.4L20 8Z"/>
    </svg>
    <p class="text-slate-700 leading-relaxed mb-6 text-base">{html.escape(t["quote"])}</p>
    <div class="flex items-center gap-4 pt-4 border-t border-slate-100">
        <img src="{avatar}" alt="{html.escape(t["name"])}" class="w-12 h-12 rounded-full object-cover bg-slate-100" loading="lazy">
        <div class="min-w-0">
            <div class="font-semibold text-slate-900">{html.escape(t["name"])}</div>
            <div class="text-xs text-slate-500 truncate">{html.escape(t["title"])}</div>
            {sub}
        </div>
    </div>
</article>'''

def render_studio(s):
    fname, name, sub = s
    src = "../images/wp/" + fname
    if not os.path.exists(os.path.join(ROOT, "images/wp", fname)):
        return ""
    if sub:
        return f'''<a href="https://{sub}" target="_blank" rel="noopener" class="group block">
    <div class="aspect-square overflow-hidden rounded-xl bg-slate-100 border border-slate-200 group-hover:shadow-md transition-shadow">
        <img src="{src}" alt="{html.escape(name)}" class="w-full h-full object-cover group-hover:scale-105 transition-transform" loading="lazy">
    </div>
    <div class="mt-2 text-sm font-medium text-slate-900 truncate group-hover:text-brand-700">{html.escape(name)}</div>
    <div class="text-xs text-slate-500 truncate">{sub}</div>
</a>'''
    else:
        return f'''<div class="block">
    <div class="aspect-square overflow-hidden rounded-xl bg-slate-100 border border-slate-200">
        <img src="{src}" alt="{html.escape(name)}" class="w-full h-full object-cover" loading="lazy">
    </div>
    <div class="mt-2 text-sm font-medium text-slate-900 truncate">{html.escape(name)}</div>
</div>'''

testimonial_html = "\n".join(render_testimonial(t) for t in TESTIMONIALS)
studio_html = "\n".join(filter(None, (render_studio(s) for s in STUDIOS)))

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teachers — PracticeNow</title>
    <meta name="description" content="Hundreds of independent teachers trust PracticeNow to run their teaching business. Read their stories.">
    <link rel="canonical" href="https://practicenow.us/teachers/">
    <link rel="stylesheet" href="../css/tailwind.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="../js/layout.js" defer></script>
    <style>body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; }}</style>
</head>
<body class="bg-white text-slate-900 antialiased">

<section class="bg-gradient-to-b from-brand-50 to-white py-16 lg:py-20">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm font-semibold tracking-[0.18em] uppercase text-brand-600 mb-3">Teacher stories</p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 mb-6 leading-tight">Hundreds of teachers run their business on PracticeNow.</h1>
        <p class="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">From independent yoga teachers to multi-instructor schools, our customers ship classes, collect payments and grow their community without a developer or a marketer.</p>
    </div>
</section>

<section class="bg-slate-900 text-white py-14">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 grid sm:grid-cols-3 gap-8 text-center">
        <div><div class="text-4xl font-extrabold mb-1">₹9 Crore+</div><div class="text-sm text-slate-400 uppercase tracking-wider">Fees processed</div></div>
        <div><div class="text-4xl font-extrabold mb-1">30 Lakh+</div><div class="text-sm text-slate-400 uppercase tracking-wider">Minutes taught</div></div>
        <div><div class="text-4xl font-extrabold mb-1">3 Lakh+</div><div class="text-sm text-slate-400 uppercase tracking-wider">Student check-ins</div></div>
    </div>
</section>

<section class="py-20">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-14">
            <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-900 mb-3">Love from teachers</h2>
            <p class="text-lg text-slate-600">In their own words.</p>
        </div>
        <div class="grid md:grid-cols-2 gap-6">
            {testimonial_html}
        </div>
    </div>
</section>

<section class="bg-slate-50 py-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
            <p class="text-sm font-semibold tracking-[0.18em] uppercase text-brand-600 mb-3">Trusted by</p>
            <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-900 mb-3">Studios &amp; teachers running on PracticeNow.</h2>
            <p class="text-slate-600">Each one of these has its own free, professional website powered by PracticeNow.</p>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-5">
            {studio_html}
        </div>
    </div>
</section>

<section class="py-20">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-brand-600 rounded-3xl p-10 lg:p-14 text-center text-white">
            <h2 class="text-3xl sm:text-4xl font-extrabold mb-3">Join the teachers above. Sign up today.</h2>
            <p class="text-brand-100 text-lg mb-8">Free trial. No credit card required. Cancel anytime.</p>
            <a href="https://app.practicenow.us/trial/scale-non-teaching-tasks" class="inline-flex items-center justify-center px-8 py-4 rounded-xl bg-white text-brand-700 font-semibold text-lg shadow-lg hover:shadow-xl transition-all">Try PracticeNow free</a>
        </div>
    </div>
</section>

</body>
</html>'''

OUT = os.path.join(ROOT, "teachers", "index.html")
with open(OUT, "w") as fh:
    fh.write(PAGE)
print(f"wrote {OUT} ({len(PAGE)} bytes)")
