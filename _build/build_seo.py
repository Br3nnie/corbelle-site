"""Search-engine set-up for www.corbelle.ai: page titles, robots rules, canonical
URLs on the older standalone pages, plus robots.txt and sitemap.xml.

This file is the single list of which pages are public (in the sitemap) and which
are hidden (noindex). Add any new page here.

Run order after any page rebuild:
    python3 _build/build_seo.py .     # titles, legacy-page tags, robots.txt, sitemap.xml
    python3 _build/build_meta.py .    # description/canonical/OG on redesign pages (reads the titles set here)
"""
import re, os, sys, html, subprocess, datetime

os.chdir(sys.argv[1] if len(sys.argv) > 1 else '.')
SITE = 'https://www.corbelle.ai'
e = lambda x: html.escape(x, quote=True)

# file: (canonical path, title, description or None to keep the page's own)
# Redesign pages: build_meta.py manages description + canonical; only the title is set here.
REDESIGN = {
 'index.html':               ('/', 'Corbelle — Business optimisation for owner-led businesses'),
 'services.html':            ('/services.html', 'What we do: process, automation and AI — Corbelle'),
 'time-process-audit.html':  ('/time-process-audit.html', 'Time & Process Audit for UK businesses — Corbelle'),
 'automation-ai.html':       ('/automation-ai.html', 'Business Automation & AI Quick Wins — Corbelle'),
 'joined-up-systems.html':   ('/joined-up-systems.html', 'Joined-Up Systems: connect the tools you have — Corbelle'),
 'change-management.html':   ('/change-management.html', 'Change Management for growing businesses — Corbelle'),
 'strategy-leadership.html': ('/strategy-leadership.html', 'Strategy & Fractional Leadership — Corbelle'),
 'ai-adoption.html':         ('/ai-adoption.html', 'Practical AI Adoption for owner-led businesses — Corbelle'),
 'experience.html':          ('/experience.html', 'Experience and track record — Corbelle'),
 'case-studies.html':        ('/case-studies.html', 'Case studies: process and AI results — Corbelle'),
 'about.html':               ('/about.html', 'Our story: about Corbelle and Brendan Ellis'),
 'partners.html':            ('/partners.html', 'Specialist partners — Corbelle'),
 'insights.html':            ('/insights.html', 'Insights on process, automation and AI — Corbelle'),
 'tools.html':               ('/tools.html', 'Tools for process, AI and cost decisions — Corbelle'),
 'five-manual-jobs.html':    ('/five-manual-jobs.html', '5 manual jobs every growing business still does — Corbelle'),
 'tuesday-strategy.html':    ('/tuesday-strategy.html', 'You need a Tuesday strategy, not an AI strategy — Corbelle'),
 'busy-is-a-symptom.html':   ('/busy-is-a-symptom.html', "Busy isn't a badge. It's a symptom. — Corbelle"),
 'chatgpt-padded-quote.html':('/chatgpt-padded-quote.html', 'Before you approve a ChatGPT-padded tech quote — Corbelle'),
 'who-sees-the-ai-bill.html':('/who-sees-the-ai-bill.html', 'Who sees the AI bill? — Corbelle'),
 'privacy.html':             ('/privacy.html', 'Privacy policy — Corbelle'),
 'terms.html':               ('/terms.html', 'Website terms — Corbelle'),
 'cookies.html':             ('/cookies.html', 'Cookie policy — Corbelle'),
}

# Older standalone pages and funnels: this script manages title, description, canonical, robots.
LEGACY = {
 'aicost.html': ('/aicost', 'AI Implementation Cost Validator — Corbelle', None),
 'process-pain-check.html': ('/check', 'The Process Pain Check — Corbelle', None),
 'clarity-engine.html': ('/clarity-engine', 'Clarity Engine: structured decision memos — Corbelle',
    'A Corbelle skill that turns high-stakes choices into structured decision memos, explicit trade-offs and scheduled retrospectives.'),
 'costofinaction.html': ('/costofinaction', 'Cost of Inaction Diagnostic — Corbelle',
    'Put a board-level financial frame around deferring a technology investment, before operating drag, risk and lost growth force the decision.'),
 'magneticleadership.html': ('/magneticleadership', 'Magnetic Leadership tool — Corbelle',
    'A Corbelle tool for leaders who want to build trust, presence and influence with their team and board.'),
 'usecasegameplan.html': ('/usecasegameplan', 'AI Use Case Gameplan — Corbelle', None),
 'real-problem-diagnostic.html': ('/problemdiagnostic', 'The Real Problem Diagnostic — Corbelle', None),
 'performance_ceiling.html': ('/performance-ceiling', 'The Performance Ceiling: research paper — Corbelle',
    "Why performance and fitness brands are about to repeat financial services' most expensive technology mistakes, and how to avoid them."),
 'million-pound-plan.html': ('/mpp', 'The Million-Pound Operating Plan — Corbelle', None),
 'programme/index.html': ('/programme/', 'The Leadership Credibility Programme — Corbelle',
    'A 90-day partnership for senior leaders who have the title and are ready to own it: board presentations, hard conversations and decisions.'),
}

# Hidden from search: noindex, never in the sitemap.
NOINDEX = {
 '404.html': 'noindex',                     # built by build_404.py
 'enquiry-sent.html': 'noindex',            # thank-you page (tag already in page)
 'thankyou/index.html': 'noindex',
 'ai-suite-upgrade.html': 'noindex,nofollow',
 'privateinvite.html': 'noindex,nofollow',
 'prospective-client-events.html': 'noindex,nofollow',
 'transcript-reveals.html': 'noindex,nofollow',
}


def read(f): return open(f, encoding='utf-8').read()
def write(f, s): open(f, 'w', encoding='utf-8').write(s)

def set_title(s, title):
    return re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', s, count=1, flags=re.S)

def set_robots(s, value):
    s = re.sub(r'\n?\s*<meta\s+name=["\']robots["\'][^>]*>', '', s, flags=re.I)
    return s.replace('</title>', f'</title>\n<meta name="robots" content="{value}" />', 1)

changed = []
for f, (path, title) in REDESIGN.items():
    s = read(f); n = set_title(s, title)
    if n != s: write(f, n); changed.append(f)

for f, (path, title, desc) in LEGACY.items():
    s = read(f)
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', s, re.I | re.S)
    d = desc or (html.unescape(m.group(1)) if m else None)
    s = re.sub(r'\n?<!-- seo:start -->.*?<!-- seo:end -->', '', s, flags=re.S)
    s = re.sub(r'\n?\s*<meta\s+name=["\']description["\'][^>]*>', '', s, flags=re.I)
    s = re.sub(r'\n?\s*<link\s+rel=["\']canonical["\'][^>]*>', '', s, flags=re.I)
    s = re.sub(r'\n?\s*<meta\s+name=["\']robots["\'][^>]*>', '', s, flags=re.I)
    s = set_title(s, title)
    url = SITE + path
    block = '\n<!-- seo:start -->\n' + (f'<meta name="description" content="{e(d)}" />\n' if d else '') + \
            f'<link rel="canonical" href="{url}" />\n<!-- seo:end -->'
    s = s.replace('</title>', '</title>' + block, 1)
    s = s.replace('content="https://corbelle.ai/', 'content="https://www.corbelle.ai/')  # og/twitter URLs on the canonical host
    if s != read(f): write(f, s); changed.append(f)

for f, value in NOINDEX.items():
    s = read(f); n = set_robots(s, value)
    if n != s: write(f, n); changed.append(f)

# Every HTML file must be classified, so nothing new slips through unseen.
import glob
known = set(REDESIGN) | set(LEGACY) | set(NOINDEX) | {'usecasevalidator.html'}  # redirected to /usecasegameplan
unknown = sorted(set(glob.glob('*.html') + glob.glob('*/index.html')) - known)
if unknown:
    sys.exit('Unclassified pages, add them to build_seo.py: ' + ', '.join(unknown))

def lastmod(f):
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', f], capture_output=True, text=True).stdout.strip()
    return out or datetime.date.today().isoformat()

urls = [(SITE + p, lastmod(f), '1.0' if p == '/' else '0.8') for f, (p, t) in REDESIGN.items()] + \
       [(SITE + p, lastmod(f), '0.6') for f, (p, t, d) in LEGACY.items()]
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      ''.join(f'  <url><loc>{u}</loc><lastmod>{m}</lastmod><priority>{p}</priority></url>\n' for u, m, p in urls) +
      '</urlset>\n')
write('robots.txt', 'User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: ' + SITE + '/sitemap.xml\n')
print(f'{len(changed)} pages updated; sitemap has {len(urls)} URLs')
for f in changed: print('  ', f)
