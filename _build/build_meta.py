"""Adds description, canonical, Open Graph / Twitter tags and favicon to every page.
Usage: python3 tools/build_meta.py <site dir>"""
import re, os, sys, glob, html
os.chdir(sys.argv[1])
SITE = 'https://www.corbelle.ai'
A = re.search(r'src="([^"]*)bren-headshot\.jpg"', open('strategy-leadership.html').read()).group(1)  # 'assets/' or 'assets/'
OG_IMG = SITE + '/assets/og-corbelle.jpg'

DESC = {
 'index.html': 'Corbelle helps UK owner-led businesses find the hours lost to manual work and give them back. Fixed price, people first, no new system you don\'t need.',
 'services.html': 'What Corbelle does: time and process audits, automation and AI, joined-up systems, change management, strategy and fractional leadership, and AI adoption.',
 'time-process-audit.html': 'Find out where your team\'s hours go and what each manual step costs, before you spend a penny on software. A fixed-price time and process audit.',
 'automation-ai.html': 'Kill the copy-paste. Corbelle automates repetitive jobs using tools you already pay for, and uses AI only where it genuinely saves time.',
 'joined-up-systems.html': 'Stop re-keying the same data into three places. Corbelle connects the systems you already have so information lives once.',
 'change-management.html': 'New ways of working only stick if people own them. Change management that brings your team with you and is still working six months on.',
 'strategy-leadership.html': 'Senior direction without the full-time hire: independent assessments, roadmaps, partner selection and a fractional technology and operations lead.',
 'ai-adoption.html': 'Practical AI for owner-led businesses. Fix the process first, then use AI where it saves time, with simple rules your team understands.',
 'experience.html': 'Twenty years inside Big 4, banking, private equity and media, and Corbelle clients from multi-country groups to trade businesses.',
 'case-studies.html': 'Real Corbelle client work: what was broken, what we changed, and what it\'s worth now.',
 'about.html': 'Corbelle is a London-based business optimisation practice founded by Brendan Ellis, ACCA Fellow and former Head of Data.',
 'partners.html': 'Corbelle stays deliberately small and brings in trusted specialists for cyber security, data engineering, branding and software builds, under one plan.',
 'enquiry-sent.html': 'Thanks for getting in touch with Corbelle. You will hear back within one working day.',
 'tools.html': 'Free and paid Corbelle tools: the cost of busywork calculator, AI Use Case Gameplan, AI Cost Validator and more.',
}

for f in sorted(glob.glob('*.html')):
    s = open(f).read()
    if 'redesign.css' not in s:
        continue  # leave the older standalone tool pages alone
    head_end = s.index('</head>')
    head = s[:head_end]
    # strip anything we manage, then re-add
    m = re.search(r'<meta name="description" content="([^"]*)"\s*/?>', head)
    desc = DESC.get(f) or (html.unescape(m.group(1)) if m else 'Corbelle: business optimisation for UK owner-led businesses.')
    head = re.sub(r'\n?<!-- meta:start -->.*?<!-- meta:end -->', '', head, flags=re.S)
    head = re.sub(r'\s*<meta name="description"[^>]*>', '', head)
    title = html.unescape(re.search(r'<title>(.*?)</title>', head).group(1))
    url = SITE + '/' + ('' if f == 'index.html' else f)
    e = lambda x: html.escape(x, quote=True)
    block = f'''
<!-- meta:start -->
<meta name="description" content="{e(desc)}" />
<link rel="canonical" href="{url}" />
<link rel="icon" href="{A}favicon.svg" type="image/svg+xml" />
<meta name="theme-color" content="#163A5F" />
<meta property="og:type" content="{'article' if 'byline' in s else 'website'}" />
<meta property="og:site_name" content="Corbelle" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE + '/assets/insights/' + f.replace('.html','.jpg') if os.path.exists('assets/insights/' + f.replace('.html','.jpg')) else OG_IMG}" />
<meta name="twitter:card" content="summary_large_image" />
<!-- meta:end -->'''
    head = head.replace('</title>', '</title>' + block, 1)
    s = head + s[head_end:]
    open(f, 'w').write(s)
print('meta added to', sum('redesign.css' in open(x).read() for x in glob.glob('*.html')), 'pages')
