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

# Featured testimonials, sourced verbatim from https://practicenow.us/teachers/
# (apostrophes/dashes normalised; HTML entities decoded). Order matches the
# original page; subdomain mappings come from each testimonial's "Visit site"
# link on the live page.
TESTIMONIALS = [
    {
        "img": "komal.jpg",
        "name": "Komal Dubey",
        "title": "Freelance Yoga & Animal Flow Instructor, Mumbai",
        "subdomain": "movementwithkomal.practicenow.us",
        "quote": "I do not have to follow up for payments or track student attendance anymore. It saves me energy and time which I can use in coming up with workshops or planning my sequences. PracticeNow is like my online studio. It makes me look more professional as I schedule classes that learners can join in one click rather than coordinating over WhatsApp.",
    },
    {
        "img": "santhanam.jpg",
        "name": "Santhanam Sridharan",
        "title": "Founder, Chakra Project",
        "subdomain": "chakraproject.practicenow.us",
        "quote": "Maintaining excel sheets, making a list of whom to call, what to talk about, when to call, date and time — I have done it all. And I know how it can suck the time away from the things you want to do. When I saw PracticeNow, I said I am immediately taking it. I would definitely recommend PracticeNow. Don't even think twice.",
    },
    {
        "img": "rohini.jpg",
        "name": "Rohini Manohar",
        "title": "Founder, Chennai Yoga Studio, Chennai",
        "subdomain": "chennaiyoga.practicenow.us",
        "quote": "As a teacher, my first love is always teaching. To be bogged down by all the other work was taking away from what I could do as a teacher. What's more, the team at PracticeNow actually cares and listens. Suggestions are actually heard. This makes a world of difference.",
    },
    {
        "img": "vikar.jpg",
        "name": "Vikas Shenoy",
        "title": "Founder, Pancha Yoga",
        "subdomain": "panchayoga.practicenow.us",
        "quote": "Earlier, I would hardly sleep at the start and the end of each month. Students from different time zones would pay at 2 AM and expect a Zoom link overnight. Also, when they transferred fees I just couldn't figure out who did. PracticeNow has saved 80% to 90% of my time. I can find time to watch IPL, play with my children, do personal practice, learn something new.",
    },
    {
        "img": "Regeesh-Vattakandy-e1643975730328.jpg",
        "name": "Regeesh Vattakandy",
        "title": "Founder, Aayana",
        "subdomain": "aayana.practicenow.us",
        "quote": "Before PracticeNow, we used to send Zoom links and manually mark attendance. It was complicated. With PracticeNow we can see what time who attended the class. It's made our lives much more free. Students can see the schedule and buy the package online — we don't have to send the details. They can also see how many classes they have left before their package expires.",
    },
    {
        "img": "meghna.jpg",
        "name": "Meghna KV",
        "title": "Founder, The Ayuh Project",
        "subdomain": "theayuhproject.practicenow.us",
        "quote": "PracticeNow gives you a website of your own. The video recordings are something that the students are enjoying so much. Most of my students are working professionals and a few are school-going students as well, so if they do miss out on classes, they can go back and watch these recorded class videos and practice by themselves.",
    },
    {
        "img": "Sabir-150x150.jpg",
        "name": "Sabir Sheikh",
        "title": "Founder, Yoga Sadhana Mandir",
        "subdomain": "ysmyoga.practicenow.us",
        "quote": "Video recordings are really helping us and our students. People who were not able to join our live sessions are now able to go through the recordings, and enjoy them at a different time of the day on their own. They are also subscribing in order to access these video recordings. My yoga text students especially use them to revise what has been taught.",
    },
    {
        "img": "Sivakumar-Puthenmadathil-yoga-teacher.jpg",
        "name": "Sivakumar Puthenmadathil",
        "title": "Founder, 6 AM Yoga",
        "subdomain": "6am.practicenow.us",
        "quote": "It eliminates manual and non-productive work of monitoring attendance, payments and billing cycles. It is highly user-friendly and professional. People join the class, make payments, mark attendance, all on their own. Plus, whenever I am stuck, the support from PracticeNow is just flawless. I raise a ticket on Instagram or WhatsApp, and immediately someone helps me bounce back.",
    },
    {
        "img": "jaya-ramesh-yoga-teacher.jpg",
        "name": "Jaya Ramesh",
        "title": "Founder, Param Yoga",
        "subdomain": "paramyoga.practicenow.us",
        "quote": "When COVID started, it became a nightmare for me to manage the volume of members, to see how many classes they have attended. PracticeNow's recorded videos and the Zoom class feature has helped us a lot with invoicing and tracking who has paid and who has not. I recommend it to anybody who takes classes online — be it music or dance. This software will make your life easier.",
    },
    {
        "img": "Chandraprakash-R-yoga-teacher.jpg",
        "name": "Chandraprakash R",
        "title": "Founder, Uddiyana Yoga",
        "subdomain": "uddiyanayoga.practicenow.us",
        "quote": "This past year I couldn't have gone through without PracticeNow. I was spending a lot of time not teaching and just managing attendance and finances. PracticeNow has helped me track who is regular each month and how much money I have made through group or private classes.",
    },
    {
        "img": "rani-naveen-yoga-teacher.jpg",
        "name": "Rani Naveen",
        "title": "Founder, Prerana Yoga Shala",
        "subdomain": "preranayogashala.practicenow.us",
        "quote": "Because of USA and India pricing flexibility, my finances have become so strong. Earlier, I had to keep everything in mind, collect fees and ensure I don't ask for fees from someone who's already paid. Also, students who missed classes asked for refund. But with PracticeNow, the subscription automatically ends on the expiry date. After that, they need to renew it. I now don't need to worry about scheduling classes, collecting fees, or charging appropriately.",
    },
    {
        "img": "Nita-Saini-yoga-teacher.jpg",
        "name": "Nita Saini",
        "title": "Founder, Swadhyay Yoga Shala",
        "subdomain": "swadhyayyogashala.practicenow.us",
        "quote": "One day while sleeping I got a call. I said I can forward you the class link and you can GPay me. But he said army protocols required a QR code. That same evening I called up PracticeNow. Now my students find it very easy to pay. If homemakers miss the morning class, they have the flexibility to attend the 7:30 class or the afternoon class, or mid-evening class — and their money is not wasted. PracticeNow helps deliver customer satisfaction.",
    },
    {
        "img": "Soorya-Senthil-Kumar-yoga-teacher.jpg",
        "name": "Soorya Senthil Kumar",
        "title": "Founder, Lockdown Fitness",
        "subdomain": "lockdownfitness.practicenow.us",
        "quote": "I am a very messy person but at work, I like to stay organized. I saw PracticeNow could make my setup look professional. Participants could pay on the site rather than needing our bank details. Our PracticeNow site looks very nice and gives all the details about our team and our Instagram feed. We do not need to share Zoom links for every class. If someone doesn't show up, that is logged in. It also tracks how much we've made in revenue each month.",
    },
]

def initials(name: str) -> str:
    parts = [p for p in name.replace(".", " ").split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()

def avatar_html(t):
    """<img> if the local file exists, otherwise an initials-circle fallback."""
    fname = t["img"]
    if fname and os.path.exists(os.path.join(ROOT, "images", "wp", fname)):
        return (
            f'<img src="../images/wp/{fname}" alt="{html.escape(t["name"])}" '
            f'class="w-12 h-12 rounded-full object-cover bg-slate-100 flex-shrink-0" loading="lazy">'
        )
    return (
        f'<div class="w-12 h-12 rounded-full bg-brand-100 text-brand-700 '
        f'font-semibold flex items-center justify-center flex-shrink-0" '
        f'aria-label="{html.escape(t["name"])}">{initials(t["name"])}</div>'
    )

def render_testimonial(t):
    sub = ""
    if t.get("subdomain"):
        sub = (f'<a href="https://{t["subdomain"]}" target="_blank" rel="noopener" '
               f'class="text-brand-600 hover:text-brand-700 text-sm font-medium">'
               f'{t["subdomain"]}</a>')
    return f'''
<article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8">
    <svg class="w-8 h-8 text-brand-600 mb-4" fill="currentColor" viewBox="0 0 32 32" aria-hidden="true">
        <path d="M9.4 8h6.4l-3.2 6.4h3.2v9.6H6.2V14.4L9.4 8Zm10.6 0h6.4l-3.2 6.4h3.2v9.6h-9.6V14.4L20 8Z"/>
    </svg>
    <p class="text-slate-700 leading-relaxed mb-6 text-base">{html.escape(t["quote"])}</p>
    <div class="flex items-center gap-4 pt-4 border-t border-slate-100">
        {avatar_html(t)}
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
