"""Rebuilds the header nav (desktop dropdowns + collapsible phone menu) and the
footer Services/Tools columns on every page.
Usage: python3 tools/build_nav.py <redesign dir> <css version>"""
import re, os, sys
os.chdir(sys.argv[1])
CSSV = sys.argv[2]
BOOK = 'https://cal.com/brennie/30min'
chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>'
groups = [
 ('Services', 'services', [('What we do', 'services.html'), ('Change Management', 'change-management.html'), ('Strategy &amp; Leadership', 'strategy-leadership.html'), ('AI Adoption', 'ai-adoption.html')]),
 ('Experience', 'experience', [('Overview', 'experience.html'), ('Case studies', 'case-studies.html'), ('Speaking ↗', 'https://speaking.brendanellis.com/')]),
 ('About', 'about', [('Our story', 'about.html'), ('Partners', 'partners.html')]),
 ('Insights', 'insights', [('Latest thinking', 'insights.html'), ('Tools', 'tools.html')]),
]
pages = {
 'index.html': None, 'services.html': 'services', 'strategy-leadership.html': 'services', 'ai-adoption.html': 'services',
 'time-process-audit.html': 'services', 'automation-ai.html': 'services', 'joined-up-systems.html': 'services', 'change-management.html': 'services',
 'experience.html': 'experience', 'case-studies.html': 'experience',
 'about.html': 'about', 'partners.html': 'about', 'tools.html': 'insights', 'insights.html': 'insights', 'privacy.html': None, 'terms.html': None, 'cookies.html': None, 'five-manual-jobs.html': 'insights', 'tuesday-strategy.html': 'insights', 'busy-is-a-symptom.html': 'insights', 'chatgpt-padded-quote.html': 'insights', 'who-sees-the-ai-bill.html': 'insights',
}
ext = lambda h: ' target="_blank" rel="noopener"' if h.startswith('http') else ''
SCRIPT = '''<script>
document.querySelectorAll('.dd').forEach(d=>{const b=d.querySelector('.dd-btn');
  b.addEventListener('click',e=>{e.stopPropagation();const o=!d.classList.contains('open');document.querySelectorAll('.dd.open').forEach(x=>{x.classList.remove('open');x.querySelector('.dd-btn').setAttribute('aria-expanded','false')});d.classList.toggle('open',o);b.setAttribute('aria-expanded',o)});
  d.addEventListener('keydown',e=>{if(e.key==='Escape'){d.classList.remove('open');b.setAttribute('aria-expanded','false');b.focus()}});});
document.addEventListener('click',()=>document.querySelectorAll('.dd.open').forEach(x=>{x.classList.remove('open');x.querySelector('.dd-btn').setAttribute('aria-expanded','false')}));
const bg=document.querySelector('.burger'),mn=document.querySelector('.mnav');
bg.addEventListener('click',()=>{const o=mn.classList.toggle('open');bg.setAttribute('aria-expanded',o);document.body.classList.toggle('menu-open',o)});
mn.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{mn.classList.remove('open');bg.setAttribute('aria-expanded','false');document.body.classList.remove('menu-open')}));
addEventListener('resize',()=>{if(innerWidth>=768&&mn.classList.contains('open')){mn.classList.remove('open');bg.setAttribute('aria-expanded','false');document.body.classList.remove('menu-open')}});
</script>'''

def nav(f, active):
    li = ['      <li><a href="index.html"' + (' class="active"' if f == 'index.html' else '') + '>Home</a></li>']
    m = ['<a class="m-top" href="index.html">Home</a>']
    for label, key, items in groups:
        a = ' active' if key == active else ''
        sub = ''.join(f'<li><a href="{h}"' + (' class="current"' if h == f else '') + ext(h) + f'>{t}</a></li>' for t, h in items)
        li.append(f'      <li class="dd"><button class="dd-btn{a}" type="button" aria-haspopup="true" aria-expanded="false">{label} {chev}</button><ul class="dd-menu">{sub}</ul></li>')
        msub = ''.join(f'<a href="{h}"{ext(h)}>{t}</a>' for t, h in items)
        m.append(f'<details{" open" if key == active else ""}><summary>{label}{chev}</summary><div>{msub}</div></details>')
    li.append('      <li><a href="index.html#contact">Contact</a></li>')
    m.append('<a class="m-top" href="index.html#contact">Contact</a>')
    return f'''<nav>
  <div class="wrap">
    <a class="logo" href="index.html">Corbelle<span>.</span></a>
    <ul class="nav-links">
{chr(10).join(li)}
    </ul>
    <div class="nav-right">
      <a class="btn btn-primary nav-cta" href="{BOOK}" target="_blank" rel="noopener"><span class="cta-long">Book a free time audit</span><span class="cta-short">Book an audit</span></a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
  <div class="mnav">{''.join(m)}<a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">Book a free time audit</a></div>
</nav>
{SCRIPT}'''

# Corbelle newsletter: paste the Kit form ID here (Kit > Grow > Landing Pages & Forms > your form > Embed > the number in the HTML).
KIT_FORM_ID = ''
if KIT_FORM_ID:
    FORM_OPEN = f'<form class="subscribe" method="POST" action="https://app.kit.com/forms/{KIT_FORM_ID}/subscriptions" target="_blank">'
else:  # not connected yet: nothing is sent anywhere
    FORM_OPEN = '<form class="subscribe" onsubmit="event.preventDefault();this.querySelector(\'button\').textContent=\'Coming soon\'">'
FORM = FORM_OPEN + '<div class="sub-row"><input type="text" name="fields[first_name]" required placeholder="First name" aria-label="First name" /><input type="text" name="fields[last_name]" placeholder="Last name" aria-label="Last name" /></div><div class="sub-join"><input type="email" name="email_address" required placeholder="your@email.com" aria-label="Email address" /><button type="submit">Subscribe</button></div><p class="sub-note">Practical ideas on getting your team\'s time back. Unsubscribe anytime.</p></form>'
FOOT_BRAND = '<div class="f-brand"><a class="logo" href="index.html">Corbelle<span>.</span></a><p>Business optimisation for UK owner-led businesses. Less busywork, more business.</p><div class="stay"><span>Stay informed</span><a class="li" href="https://www.linkedin.com/company/corbelleadvisory/" target="_blank" rel="noopener" aria-label="Corbelle on LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg></a></div>' + FORM + '</div>'
FOOT_SERV = '<div><h4>Services</h4><ul><li><a href="services.html">What we do</a></li><li><a href="time-process-audit.html">Time &amp; Process Audit</a></li><li><a href="automation-ai.html">Automation &amp; AI</a></li><li><a href="joined-up-systems.html">Joined-Up Systems</a></li><li><a href="change-management.html">Change Management</a></li><li><a href="strategy-leadership.html">Strategy &amp; Leadership</a></li><li><a href="ai-adoption.html">AI Adoption</a></li></ul></div>'
FOOT_TOOLS = '<div><h4>Tools</h4><ul><li><a href="index.html#calculator">Cost of busywork calculator</a></li><li><a href="/usecasegameplan">AI Use Case Gameplan</a></li><li><a href="/aicost">AI Cost Validator</a></li><li><a href="tools.html">All tools</a></li></ul></div>'
FOOT_CO = '<div><h4>Company</h4><ul><li><a href="about.html">About</a></li><li><a href="partners.html">Partners</a></li><li><a href="experience.html">Experience</a></li><li><a href="case-studies.html">Case studies</a></li><li><a href="https://speaking.brendanellis.com/" target="_blank" rel="noopener">Speaking</a></li><li><a href="index.html#contact">Contact</a></li></ul></div>'

for f, act in pages.items():
    if not os.path.exists(f):
        print('missing', f); continue
    s = open(f).read()
    s = re.sub(r'<nav>.*?</nav>\n?(<script>\s*document\.querySelectorAll\(\'\.dd\'\).*?</script>)?', lambda _: nav(f, act), s, count=1, flags=re.S)
    s = re.sub(r'redesign\.css\?v=\d+', f'redesign.css?v={CSSV}', s)
    s = re.sub(r'(<div class="fgrid">\s*)<div( class="f-brand")?>.*?(?=\s*<div><h4>Services)', lambda m: m.group(1) + FOOT_BRAND, s, count=1, flags=re.S)
    s = re.sub(r'<div><h4>Services</h4><ul>.*?</ul></div>', FOOT_SERV, s, count=1, flags=re.S)
    s = re.sub(r'<div><h4>Tools</h4><ul>.*?</ul></div>', FOOT_TOOLS, s, count=1, flags=re.S)
    s = re.sub(r'<div><h4>Company</h4><ul>.*?</ul></div>', FOOT_CO, s, count=1, flags=re.S)
    s = re.sub(r'<div class="fbottom">.*?</div>', '<div class="fbottom"><span>© 2026 Corbelle</span><span><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a> · <a href="cookies.html">Cookies</a></span></div>', s, count=1, flags=re.S)
    open(f, 'w').write(s)
    print(f, s.count('class="dd"'), s.count('<nav>'))
