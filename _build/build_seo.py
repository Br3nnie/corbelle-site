"""Search-engine set-up for www.corbelle.ai: page titles, robots rules, canonical
URLs on the older standalone pages, plus robots.txt and sitemap.xml.

The list of public and hidden pages lives in _build/site_pages.py.

Run order after any page rebuild:
    python3 _build/build_seo.py .     # titles, legacy-page tags, robots.txt, sitemap.xml
    python3 _build/build_meta.py .    # description/canonical/OG on redesign pages (reads the titles set here)
"""
import re, os, sys, html, subprocess, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.chdir(sys.argv[1] if len(sys.argv) > 1 else '.')
SITE = 'https://www.corbelle.ai'
e = lambda x: html.escape(x, quote=True)

from site_pages import REDESIGN, LEGACY, NOINDEX  # the public/hidden page list


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
