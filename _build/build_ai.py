"""AI and rich-result readiness for www.corbelle.ai:
  1. JSON-LD structured data on every public page (Organization, Person, WebSite,
     page type, Service, Article, FAQPage, BreadcrumbList)
  2. An author box with credentials at the end of each article
  3. /llms.txt, a plain-text guide to the site for AI tools

Pages come from _build/site_pages.py (public pages only; hidden pages get nothing).
Run last, after build_seo.py and build_meta.py:   python3 _build/build_ai.py .
Safe to rerun: everything it adds sits between marker comments and is replaced."""
import re, os, sys, json, html, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_pages import REDESIGN, LEGACY

os.chdir(sys.argv[1] if len(sys.argv) > 1 else '.')
SITE = 'https://www.corbelle.ai'
ORG, PERSON, WEBSITE = SITE + '/#organization', SITE + '/#brendan', SITE + '/#website'
LINKEDIN_CO = 'https://www.linkedin.com/company/corbelleadvisory/'
LINKEDIN_ME = 'https://www.linkedin.com/in/brendanmellis'
COMPANIES_HOUSE = 'https://find-and-update.company-information.service.gov.uk/company/08106968'
SPEAKING = 'https://speaking.brendanellis.com/'

SERVICES = {  # file: service type
 'time-process-audit.html': 'Business process audit',
 'automation-ai.html': 'Business process automation',
 'joined-up-systems.html': 'Systems integration',
 'change-management.html': 'Change management consulting',
 'strategy-leadership.html': 'Fractional technology and operations leadership',
 'ai-adoption.html': 'AI adoption consulting',
}
SECTION = {  # breadcrumb parent for pages below the top level
 **{f: ('What we do', '/services.html') for f in SERVICES},
 **{f: ('Insights', '/insights.html') for f in ['five-manual-jobs.html', 'tuesday-strategy.html', 'busy-is-a-symptom.html', 'chatgpt-padded-quote.html', 'who-sees-the-ai-bill.html']},
 'case-studies.html': ('Experience', '/experience.html'),
 'partners.html': ('About', '/about.html'),
 **{f: ('Tools', '/tools.html') for f in ['aicost.html', 'process-pain-check.html', 'clarity-engine.html', 'costofinaction.html', 'magneticleadership.html', 'usecasegameplan.html']},
}
COLLECTION = {'services.html', 'insights.html', 'tools.html', 'case-studies.html', 'experience.html'}

text = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def git_date(f, first=False):
    args = ['git', 'log', '--format=%cs'] + (['--diff-filter=A'] if first else ['-1']) + ['--', f]
    out = subprocess.run(args, capture_output=True, text=True).stdout.split()
    return (out[-1] if first else out[0]) if out else None

ORG_NODE = {
 '@type': ['Organization', 'ProfessionalService'], '@id': ORG,
 'name': 'Corbelle', 'legalName': 'Corbelle Limited', 'url': SITE + '/',
 'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/favicon.svg'},
 'image': SITE + '/assets/og-corbelle.jpg',
 'description': 'Corbelle is a London-based business optimisation practice that helps UK owner-led businesses with 50 to 400 staff find the hours lost to manual work, connect their systems and adopt AI safely.',
 'slogan': 'Less busywork, more business.',
 'email': 'hello@corbelle.ai',
 'address': {'@type': 'PostalAddress', 'addressLocality': 'London', 'addressCountry': 'GB'},
 'areaServed': {'@type': 'Country', 'name': 'United Kingdom'},
 'identifier': {'@type': 'PropertyValue', 'propertyID': 'Companies House company number', 'value': '08106968'},
 'founder': {'@id': PERSON},
 'knowsAbout': ['Business process improvement', 'Process automation', 'Systems integration', 'AI adoption', 'Change management', 'Fractional leadership'],
 'sameAs': [LINKEDIN_CO, COMPANIES_HOUSE],
}
PERSON_NODE = {
 '@type': 'Person', '@id': PERSON, 'name': 'Brendan Ellis', 'jobTitle': 'Founder',
 'worksFor': {'@id': ORG}, 'url': SITE + '/about.html', 'image': SITE + '/assets/bren-headshot.jpg',
 'description': 'Founder of Corbelle. ACCA Fellow and former Head of Data, with twenty years across Big 4, banking, private equity and media.',
 'hasCredential': {'@type': 'EducationalOccupationalCredential', 'credentialCategory': 'Professional certification', 'name': 'Fellow of the Association of Chartered Certified Accountants (FCCA)'},
 'knowsAbout': ['Business optimisation', 'Data leadership', 'AI adoption', 'Process automation'],
 'sameAs': [LINKEDIN_ME, SPEAKING],
}
WEBSITE_NODE = {'@type': 'WebSite', '@id': WEBSITE, 'url': SITE + '/', 'name': 'Corbelle', 'publisher': {'@id': ORG}, 'inLanguage': 'en-GB'}

def faq(s):
    m = re.search(r'<div class="faq">(.*?)</div>', s, re.S)
    if not m: return None
    qa = re.findall(r'<summary>(.*?)</summary>\s*(.*?)</details>', m.group(1), re.S)
    return [{'@type': 'Question', 'name': text(q), 'acceptedAnswer': {'@type': 'Answer', 'text': text(a)}} for q, a in qa] or None

def graph_for(f, path, s):
    url = SITE + path
    title = text(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    name = re.sub(r'\s+—\s+Corbelle$', '', title)
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s)
    desc = html.unescape(m.group(1)) if m else None
    ptype = 'AboutPage' if f == 'about.html' else 'CollectionPage' if f in COLLECTION else 'WebPage'
    page = {'@type': ptype, '@id': url + '#webpage', 'url': url, 'name': title, 'isPartOf': {'@id': WEBSITE},
            'about': {'@id': ORG}, 'inLanguage': 'en-GB'}
    if desc: page['description'] = desc
    if f == 'about.html': page['mainEntity'] = {'@id': PERSON}
    nodes = [ORG_NODE, PERSON_NODE, WEBSITE_NODE, page]
    if path != '/':
        crumbs = [('Home', '/')] + ([SECTION[f]] if f in SECTION else []) + [(name, path)]
        bc = {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
              {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p} for i, (n, p) in enumerate(crumbs)]}
        page['breadcrumb'] = {'@id': bc['@id']}; nodes.append(bc)
    if f in SERVICES:
        nodes.append({'@type': 'Service', '@id': url + '#service', 'name': name, 'serviceType': SERVICES[f], 'url': url,
                      'description': desc, 'provider': {'@id': ORG}, 'areaServed': {'@type': 'Country', 'name': 'United Kingdom'},
                      'audience': {'@type': 'BusinessAudience', 'audienceType': 'UK owner-led businesses with 50 to 400 staff'}})
        page['mainEntity'] = {'@id': url + '#service'}
    if 'class="byline"' in s:
        h1 = text(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
        nodes.append({'@type': 'BlogPosting', '@id': url + '#article', 'headline': h1, 'description': desc,
                      'image': SITE + '/assets/insights/' + f.replace('.html', '.jpg'),
                      'datePublished': git_date(f, first=True), 'dateModified': git_date(f),
                      'author': {'@id': PERSON}, 'publisher': {'@id': ORG}, 'mainEntityOfPage': {'@id': url + '#webpage'},
                      'inLanguage': 'en-GB'})
    qa = faq(s)
    if qa:  # FAQ is part of the page; stated as its own node so assistants can lift Q&A pairs
        nodes.append({'@type': 'FAQPage', '@id': url + '#faq', 'url': url, 'mainEntity': qa, 'isPartOf': {'@id': url + '#webpage'}})
    return {'@context': 'https://schema.org', '@graph': nodes}

AUTHOR_BOX = '''<!-- author:start --><div class="author-box"><img src="assets/bren-headshot.jpg" alt="Brendan Ellis" loading="lazy" /><div><p class="ab-name">Written by Brendan Ellis</p><p class="ab-bio">Founder of Corbelle. ACCA Fellow and former Head of Data, with twenty years across Big 4, banking, private equity and media. Brendan helps UK owner-led businesses find the hours lost to manual work and give them back.</p><p class="ab-links"><a href="about.html">More about Brendan</a><span>·</span><a href="https://www.linkedin.com/in/brendanmellis" target="_blank" rel="noopener">LinkedIn</a></p></div></div><!-- author:end -->'''

pages = {**{f: v[0] for f, v in REDESIGN.items()}, **{f: v[0] for f, v in LEGACY.items()}}
done = []
for f, path in pages.items():
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!-- schema:start -->.*?<!-- schema:end -->\n', '', s, flags=re.S)
    s = re.sub(r'<!-- author:start -->.*?<!-- author:end -->', '', s, flags=re.S)
    if 'class="byline"' in s:
        s = s.replace('</article>', AUTHOR_BOX + '</article>', 1)
    ld = json.dumps(graph_for(f, path, s), ensure_ascii=False, indent=1).replace('</', '<\\/')
    s = s.replace('</head>', f'<!-- schema:start -->\n<script type="application/ld+json">\n{ld}\n</script>\n<!-- schema:end -->\n</head>', 1)
    open(f, 'w', encoding='utf-8').write(s); done.append(f)

# ---- llms.txt ----
def desc_of(f):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', open(f, encoding='utf-8').read())
    return html.unescape(m.group(1)) if m else ''
def name_of(f):
    t = text(re.search(r'<title>(.*?)</title>', open(f, encoding='utf-8').read(), re.S).group(1))
    return re.sub(r'\s+—\s+Corbelle$', '', t)
link = lambda f, path: f'- [{name_of(f)}]({SITE}{path}): {desc_of(f)}'
ARTICLES = [f for f in REDESIGN if f in SECTION and SECTION[f][0] == 'Insights']
lines = ['# Corbelle', '',
 '> Corbelle is a London-based business optimisation practice founded by Brendan Ellis (ACCA Fellow, former Head of Data). '
 'It helps UK owner-led businesses with 50 to 400 staff find the hours lost to manual work, connect the systems they already have, '
 'and adopt AI safely. Work is fixed price and people first, and starts with a free time audit.', '',
 'Key facts:',
 '- Who it is for: owners and managing directors of UK owner-led businesses with 50 to 400 staff.',
 '- Average time saved: 7 hours per person, per week.',
 '- First step: a free 30-minute time audit call, https://cal.com/brennie/30min',
 '- Contact: hello@corbelle.ai',
 '- Company: Corbelle Limited, registered in England and Wales, company number 08106968.',
 '- Specialist partners (cyber security, data engineering, branding, software builds) are brought in under one plan. '
 'Where a partner or vendor pays Corbelle a revenue share, Corbelle says so up front.', '',
 '## Services', link('services.html', '/services.html')] + [link(f, REDESIGN[f][0]) for f in SERVICES] + [
 '', '## About', link('about.html', '/about.html'), link('experience.html', '/experience.html'),
 link('case-studies.html', '/case-studies.html'), link('partners.html', '/partners.html'),
 '', '## Insights'] + [link(f, REDESIGN[f][0]) for f in ARTICLES] + [
 '', '## Tools', link('tools.html', '/tools.html')] + [link(f, LEGACY[f][0]) for f in LEGACY if SECTION.get(f, ('',))[0] == 'Tools'] + [
 '', '## Optional'] + [link(f, LEGACY[f][0]) for f in LEGACY if SECTION.get(f, ('',))[0] != 'Tools'] + [
 link('privacy.html', '/privacy.html'), link('terms.html', '/terms.html'), '']
open('llms.txt', 'w', encoding='utf-8').write('\n'.join(lines))
print(f'structured data on {len(done)} pages; author box on {sum("author:start" in open(f).read() for f in done)} articles; llms.txt written')
