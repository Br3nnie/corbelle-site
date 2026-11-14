"""Tells IndexNow (Bing, Yandex, Seznam, Naver, Yep) which public pages changed.

    python3 -I _build/indexnow.py --all              # every URL in the site list
    git diff --name-only A B | python3 -I _build/indexnow.py   # only the pages in that diff

Run by .github/workflows/indexnow.yml after each production deploy. Google does
not use IndexNow; it relies on sitemap.xml and Search Console.
The key is public by design: it must also be served at /<key>.txt.
"""
import glob, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_pages import REDESIGN, LEGACY

HOST = 'www.corbelle.ai'
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
keys = [f for f in glob.glob('*.txt') if len(f) == 36 and all(c in '0123456789abcdef' for c in f[:32])]
if len(keys) != 1:
    sys.exit(f'Expected one IndexNow key file at the site root, found {keys}')
KEY = keys[0][:-4]

pages = {f: p for f, (p, *_) in {**REDESIGN, **LEGACY}.items()}
if '--all' in sys.argv:
    files = list(pages)
else:
    files = [l.strip() for l in sys.stdin if l.strip() in pages]
urls = sorted({f'https://{HOST}{pages[f]}' for f in files})
if not urls:
    print('No public pages changed; nothing to send.'); sys.exit(0)

body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt',
                   'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'})
if '--dry-run' in sys.argv:
    print(body.decode()); sys.exit(0)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f'IndexNow answered {r.status} for {len(urls)} URLs:'); print('\n'.join(urls))
except urllib.error.HTTPError as err:
    sys.exit(f'IndexNow refused the submission: {err.code} {err.reason} {err.read()[:300]!r}')
