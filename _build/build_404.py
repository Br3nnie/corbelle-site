"""Builds 404.html (Vercel serves it for any missing URL) from enquiry-sent.html,
so the header and footer always match the rest of the site.
Run after build_nav.py:  python3 _build/build_404.py .

Every relative link is made root-relative, because the 404 page is shown at
whatever broken address was requested (e.g. /old/page), where 'services.html'
would resolve to /old/services.html."""
import re, os, sys

os.chdir(sys.argv[1] if len(sys.argv) > 1 else '.')
s = open('enquiry-sent.html', encoding='utf-8').read()

head = '''<title>Page not found — Corbelle</title>
<meta name="robots" content="noindex" />
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
<meta name="theme-color" content="#163A5F" />'''
s = re.sub(r'<title>.*?</title>\s*<!-- meta:start -->.*?<!-- meta:end -->\s*<meta name="robots"[^>]*>', head, s, count=1, flags=re.S)

POPULAR = [
    ('What we do', '/services.html'),
    ('Time &amp; Process Audit', '/time-process-audit.html'),
    ('Case studies', '/case-studies.html'),
    ('Latest thinking', '/insights.html'),
    ('Tools and calculators', '/tools.html'),
    ('Our story', '/about.html'),
]
rows = ''.join(f'<a class="row" href="{h}">{t}<span>→</span></a>' for t, h in POPULAR)
body = f'''<header class="page-hero" style="padding-bottom:72px">
  <div class="wrap">
    <p class="eyebrow">Error 404</p>
    <h1 style="margin-top:6px">We can't find that page.</h1>
    <p class="sub">The link may be out of date, as we rebuilt the site in November 2026, or the address may have a typo. Try one of the pages below, or tell us what you were looking for.</p>
    <div style="margin-top:30px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-light" href="/">Go to the homepage</a><a class="btn btn-ghost" href="/#contact">Get in touch</a></div>
  </div>
</header>

<section style="padding:56px 0 72px">
  <div class="wrap" style="max-width:640px">
    <div class="start-box">
      <p class="lab eyebrow">Popular pages</p>
      <h3>Where most people are heading</h3>
      {rows}
      <a class="btn btn-light" href="https://cal.com/brennie/30min" target="_blank" rel="noopener">Book a free time audit</a>
    </div>
  </div>
</section>
'''
s = re.sub(r'<header class="page-hero".*?</header>\n', body, s, count=1, flags=re.S)

# root-relative: href="x.html", href="assets/..", src="assets/..", href="redesign.css?.."
s = re.sub(r'(href|src)="(?![a-z]+:|/|#)([^"]+)"', r'\1="/\2"', s)
open('404.html', 'w', encoding='utf-8').write(s)
print('404.html written')
