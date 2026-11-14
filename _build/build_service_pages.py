"""Generates the four service pages from one Hopton-style template.
Usage: python3 tools/build_service_pages.py <redesign dir>
Then run tools/build_nav.py to insert the header nav."""
import re, os, sys
os.chdir(sys.argv[1])
about = open('about.html').read()
HEAD = about[:about.index('<nav>')]
FOOT = about[about.index('<footer>'):]

def ico(p):
    return '<div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + p + '</svg></div>'
I = {
 'search': '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 'map': '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
 'pound': '<path d="M17 5.5A4.5 4.5 0 0 0 9 8.5V19M6 12h8M6 19h12"/>',
 'list': '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
 'bin': '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
 'chat': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
 'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
 'doc': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
 'bell': '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
 'chart': '<path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/>',
 'shield': '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6l8-3z"/><path d="M9.5 12l2 2 3.5-4"/>',
 'link': '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
 'db': '<ellipse cx="12" cy="5.5" rx="7" ry="2.5"/><path d="M5 5.5v13c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-13M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.5 3.4-5.5 6.5-5.5s5.7 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18.5 14.8c1.6.8 2.7 2.6 3 5.2"/>',
 'key': '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3L21 2M17 6l3 3"/>',
 'scale': '<path d="M12 3v18M5 7h14M5 7l-3 6a3 3 0 0 0 6 0L5 7zM19 7l-3 6a3 3 0 0 0 6 0l-3-6z"/>',
 'flag': '<path d="M4 22V4M4 4h13l-2 4 2 4H4"/>',
 'cap': '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/>',
 'star': '<path d="M12 2l2.6 6.2 6.4.5-4.9 4.2 1.5 6.3L12 15.8 6.4 19.2l1.5-6.3L3 8.7l6.4-.5L12 2z"/>',
 'mega': '<path d="M3 11v2a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M16 9a3 3 0 0 1 0 6"/>',
 'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'org': '<rect x="9" y="3" width="6" height="5" rx="1"/><rect x="3" y="16" width="6" height="5" rx="1"/><rect x="15" y="16" width="6" height="5" rx="1"/><path d="M12 8v4M6 16v-2h12v2"/>',
}
CTA = '<a class="btn btn-light" href="https://cal.com/brennie/30min" target="_blank" rel="noopener">Book a free time audit</a>'
ALL = [
 ('time-process-audit.html', 'Time &amp; Process Audit', 'Find where the hours go.'),
 ('automation-ai.html', 'Automation &amp; AI Quick Wins', 'Kill the copy-paste.'),
 ('joined-up-systems.html', 'Joined-Up Systems', 'Type it once.'),
 ('change-management.html', 'Change Management', 'Make change stick.'),
 ('strategy-leadership.html', 'Strategy &amp; Fractional Leadership', 'Senior direction, part-time.'),
]

PAGES = [
dict(
 file='time-process-audit.html', name='Time &amp; Process Audit', anchor='audit',
 h1='Time and process audit',
 sub="Find out where your team's hours actually go, and what each manual step is costing you, before you spend a penny on software.",
 cta='Book a free time audit',
 panel=('What the audit changes', [("“We're just busy”", 'Hours mapped, team by team'), ('Gut feel', 'A £ cost on every manual step'), ('Software demos', 'A ranked list of fixes, biggest first'), ('Loudest voice wins', 'Every voice in the findings')]),
 offers_h='Everything you need to decide what to fix first.',
 offers=[
  ('search', 'Time mapping', 'We interview and shadow the people doing the work to see how a normal week really runs, not how the process document says it does.', 'A true picture of where the hours go'),
  ('map', 'Process mapping', 'Every manual, repeated step drawn out end to end, including the workarounds nobody wrote down.', 'One shared view of how work flows'),
  ('pound', 'Cost of busywork', 'We put a £ figure on every leak, using your own salaries and volumes, so priorities are based on money, not opinion.', 'A cost on every manual step'),
  ('list', 'Ranked fix list', 'Fixes ranked by value and effort: what to simplify, what to automate, what to join up and what to leave alone.', 'Biggest wins first, quick wins flagged'),
  ('bin', 'Clear-out by exception', "Reports, spreadsheets and steps nobody uses get retired before anything is automated or migrated.", 'Less to maintain from day one'),
  ('chat', 'Playback session', 'We play findings back in your team\'s own words, grouped into themes, so everyone can see their view in the decision.', 'A team that backs the plan'),
 ],
 how_h='How the audit works',
 steps=[('Listen', 'Short conversations with the people who do the work, plus time watching it happen.'), ('Map', 'Every manual, repeated step drawn out, with the workarounds and handoffs.'), ('Cost', 'A £ figure on each leak using your own numbers, ranked by value.'), ('Play back', 'Findings and a ranked plan shared with you and your team, in plain English.')],
 block=('Fixed scope, fixed price', 'Before we start, we agree which teams and processes are in scope, how long it takes and what it costs. No day rates, no surprises.', 'Typically one to two weeks, depending on the size of the business.', ['Interviews with the people doing the work', 'Process maps for every area in scope', 'A £ cost of busywork, line by line', 'A ranked list of fixes, biggest first', 'A playback session with your team', 'A recommended next step, if you want one']),
 faq=[('How long does an audit take?', 'It depends on how many teams are in scope. We agree the timeline and the price before we start.'), ('Will it disrupt my team?', 'Very little. Most people spend under an hour with us, and we watch the work as it happens rather than pulling people into workshops.'), ('Do you need access to our systems?', 'Only to look, not to change anything. Seeing the real spreadsheets and screens is how we find the workarounds.'), ('What happens after the audit?', "You own the findings. Many clients ask us to fix the top items, but you're free to do it yourselves or with someone else.")],
 case=('Before Corbelle', '“Just get me the report.” It wasn’t a report problem.', 'The data existed. The process for collecting it had never been looked at again. Fixed upstream, not with another workaround.'),
),
dict(
 file='automation-ai.html', name='Automation &amp; AI Quick Wins', anchor='automation',
 h1='Automation and AI quick wins',
 sub='Kill the copy-paste. We automate the repetitive jobs using tools you already pay for, and use AI only where it genuinely saves time.',
 cta='Talk to us about automation',
 panel=('What changes', [('Re-typing the same data', 'Typed once, used everywhere'), ('Chasing by email', 'Automatic reminders'), ('Evening admin', 'Done on the go'), ('AI because everyone is', 'AI where it pays')]),
 offers_h='Practical automation, built around how you already work.',
 offers=[
  ('bolt', 'Workflow automation', 'Approvals, handoffs and data moving between tools, done automatically instead of by copy and paste.', 'Hours back from repetitive admin'),
  ('doc', 'Documents and quotes', 'Quotes, proposals and reports generated from what you already know, ready to check and send.', 'Faster quotes, fewer errors'),
  ('bell', 'Reminders and chasing', 'Invoices, timesheets and follow-ups chased automatically, so nobody has to remember to.', 'Nothing falls through the cracks'),
  ('spark', 'AI assistants for everyday work', 'Drafting, summarising meetings and pulling out actions, set up safely for your team.', 'Less time writing, more time doing'),
  ('chart', 'Reporting automation', 'The weekly report that takes a morning to build, refreshed automatically from the source.', 'Numbers on time, every time'),
  ('shield', 'Safe AI rules', 'One simple standard for what data can go where, with freedom for teams to choose tools inside it.', 'AI use you can explain to a client or board'),
 ],
 how_h='How automation works',
 steps=[('Pick', 'Start from the ranked fix list, so we automate the jobs that are worth the most.'), ('Simplify', 'Remove unnecessary steps first. Automating a bad process just makes mistakes faster.'), ('Automate', 'Build with tools you already own where we can, and bring in a build partner when we can\'t.'), ('Hand over', 'Show your team how it works, who owns it and what to do if something changes.')],
 block=('Tools you already own', 'Most of the wins come from Microsoft 365, Google Workspace, Xero, your CRM and the apps you already pay for. When a job needs a custom build, a trusted build partner delivers it under our plan.', None, ['Automations built and tested with your team', 'Clear notes on how each one works', 'A named owner for every automation', 'Simple rules for using AI safely', 'Training for the people who use it', 'A check-in once it has bedded in']),
 faq=[('Do we need to buy new software?', 'Usually not. We start with what you already pay for and only recommend something new when it clearly pays for itself.'), ('Is it safe to use AI with our data?', 'It can be, with the right settings and rules. We set a simple standard for what can and can\'t go into AI tools before anyone starts.'), ('What happens if an automation breaks?', 'Every automation has a named owner and plain-English notes, so your team knows how to fix or switch it off.'), ('Can you build custom tools?', 'Yes. For bigger builds we work with a trusted engineering partner, scoped and checked by us.')],
 case=('Case study', 'Fencing &amp; landscaping firm', 'The surveyor says the job out loud and gets a priced PDF quote in about 3 seconds, sent from site by WhatsApp. No forms, no evening admin.'),
),
dict(
 file='joined-up-systems.html', name='Joined-Up Systems', anchor='systems',
 h1='Joined-up systems',
 sub="Stop re-keying the same data into three places. We connect the systems you already have so information lives once and flows where it's needed.",
 cta='Talk to us about your systems',
 panel=('What changes', [('Three spreadsheets', 'One record everyone trusts'), ('Copy-paste between systems', 'Automatic sync'), ('Nobody sure who can see what', 'Clear access rules'), ('New CRM, old habits', 'Systems people actually use')]),
 offers_h='Your systems, working together.',
 offers=[
  ('map', 'Systems map', 'A simple picture of every system, spreadsheet and handoff, and where the same data is typed in twice.', 'See where data gets re-keyed'),
  ('link', 'Integrations', 'Connecting the tools you have, from no-code connectors to proper integrations built with our data engineering partner.', 'Data that flows without copy-paste'),
  ('db', 'Single source of truth', 'Agree where each piece of information lives and who owns it, then retire the duplicates.', 'One version of the numbers'),
  ('users', 'CRM set-up and clean-up', 'Get the CRM you already have working the way your team sells, so the side spreadsheets can go.', 'A CRM that replaces the spreadsheet'),
  ('key', 'Access and permissions', 'Who can see and change what, mapped and tidied, with a short report owners and boards can read.', 'Fewer admins, clearer control'),
  ('scale', 'Supplier selection', 'When you do need something new, clear requirements and a fair head-to-head before you sign.', 'The right system for the right reasons'),
 ],
 how_h='How joining up systems works',
 steps=[('Map', 'Draw every system and spreadsheet, and where data is typed in twice.'), ('Design', 'Agree where each piece of information should live and who owns it.'), ('Connect', 'Link the systems, with a specialist partner for heavier engineering.'), ('Check', 'Retire the duplicates, check access and make sure people use the new flow.')],
 block=('When we bring in partners', 'Simple connections we set up ourselves. When the job needs pipelines, a data platform or tighter security, we bring in data engineering and cyber security partners we know and trust, under one plan.', None, ['A map of your systems and data flows', 'Agreed owners for each source of data', 'Integrations built and tested', 'Duplicate spreadsheets retired', 'Access rules tidied and documented', 'Training on the new way of working']),
 faq=[('Do we have to replace our systems?', 'Rarely. Most businesses already own systems that can talk to each other. We connect what you have before suggesting anything new.'), ('What about GDPR and data security?', 'We agree what data is shared, where it lives and who can see it, and bring in a security partner where the risk needs it.'), ('Who builds the integrations?', 'We set up simple connections ourselves. Heavier engineering goes to a trusted data engineering partner, scoped and checked by us.'), ('We bought a CRM and nobody uses it. Can you help?', 'Yes. That\'s usually a set-up and adoption problem, not a software one. We fix the set-up and switch off the side spreadsheets.')],
 case=('Case study', 'International corporate finance group', 'Independent assessment, three IT partners assessed and one chosen, and admin roles going from around 28 to 4.'),
),
dict(
 file='change-management.html', name='Change Management', anchor='adoption',
 h1='Change management',
 sub='New ways of working only stick if people own them. We bring your team with you, so the change is still working six months on.',
 cta='Talk to us about change',
 panel=('What changes', [('Go live and hope', 'Adoption planned up front'), ('Old spreadsheet back by Friday', 'Old way switched off on day one'), ('One training session', 'Owners and champions'), ('Change done to people', 'Change designed with them')]),
 offers_h='Change that lasts after we leave.',
 offers=[
  ('flag', 'Adoption plan', 'Decide what "being used" looks like before go-live, and how you will know if it is working.', 'A clear definition of success'),
  ('cap', 'Training', 'Short, practical sessions built around your team\'s real work, not a generic software demo.', 'People confident on day one'),
  ('star', 'Owners and champions', 'A named owner for every new process and a champion in each team to answer questions.', 'Help on hand after we leave'),
  ('users', 'Leadership coaching', 'Coaching for owners and managers leading their teams through change they didn\'t choose.', 'Leaders who can bring people with them'),
  ('mega', 'Communication', 'What\'s changing, why and what it means for each person, in plain English, at the right time.', 'No surprises, fewer rumours'),
  ('cal', 'Check-ins', 'Planned check-ins after go-live to catch drift back to old habits early.', 'Changes still working months later'),
 ],
 how_h='How change management works',
 steps=[('Involve', 'Design changes with the people who do the work, from the start.'), ('Train', 'Practical training on real tasks, with owners and champions named.'), ('Switch over', 'Turn the old way off on day one so there is nothing to slip back to.'), ('Check in', 'Measure use against the plan and fix what isn\'t sticking.')],
 block=('Coaching for leaders', 'Brendan is a qualified transformational coach and is completing an MSc in Leadership &amp; Management. Most adoption problems are leadership problems in disguise, so we support the people leading the change, not just the people using the tools.', None, ['An adoption plan with clear measures', 'Training built around real tasks', 'Named owners and champions', 'Coaching for owners and managers', 'Plain-English communication plan', 'Check-ins after go-live']),
 faq=[('My team hates change. Will this work?', 'People resist change that is done to them. When they help design it and can see their own ideas in it, most become its biggest supporters.'), ('How do you measure adoption?', 'We agree measures before go-live, such as how many people use the new process and whether the old spreadsheet is still open, and check them after.'), ('Do you only work on your own projects?', 'No. If you have already bought a system that isn\'t being used, we can help get it adopted.'), ('Is this coaching or consulting?', 'Both. We help you plan and run the change, and coach the leaders who have to carry it.')],
 case=('Pattern we see often', 'New CRM. Old spreadsheet still running behind it.', 'One business needed one and a half extra people just to work around a new CRM. Decide what "being used" looks like before you sign.'),
),
]

def build(p):
    panel = ''.join(f'<div class="ba-line"><s>{a}</s><i>→</i><b>{b}</b></div>' for a, b in p['panel'][1])
    offers = ''.join(f'''
      <div class="card offer">{ico(I[ic])}<h3>{t}</h3><p>{d}</p><p class="outcome">↳ {o}</p></div>''' for ic, t, d, o in p['offers'])
    steps = ''.join(f'<div class="step"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p['steps']))
    bt, bp, bdur, bl = p['block']
    dur = f'\n      <p>{bdur}</p>' if bdur else ''
    checks = ''.join(f'<li>{x}</li>' for x in bl)
    faq = ''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(p['faq']))
    others = [x for x in ALL if x[0] != p['file']][:3]
    explore = ''.join(f'<a class="card offer" href="{f}"><span class="lab">Service</span><h3>{n}</h3><p>{d}</p></a>' for f, n, d in others)
    cl, ct, cd = p['case']
    body = f'''<!-- HERO -->
<header class="page-hero svc-hero" style="padding-bottom:88px">
  <div class="wrap">
    <div>
      <p class="crumbs"><a href="/">Home</a> / <a href="services.html">What we do</a> / {p['name']}</p>
      <h1>{p['h1']}</h1>
      <p class="sub">{p['sub']}</p>
      <div style="margin-top:30px"><a class="btn btn-light" href="https://cal.com/brennie/30min" target="_blank" rel="noopener">{p['cta']}</a></div>
    </div>
    <div class="ba-panel"><small>{p['panel'][0]}</small>{panel}</div>
  </div>
</header>

<!-- WHAT WE OFFER -->
<section>
  <div class="wrap">
    <div class="stack-head"><p class="eyebrow">What we offer</p><h2>{p['offers_h']}</h2></div>
    <div class="grid3">{offers}
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="sand">
  <div class="wrap">
    <div class="stack-head"><p class="eyebrow">How it works</p><h2>{p['how_h']}</h2></div>
    <div class="steps4">{steps}</div>
  </div>
</section>

<!-- PEOPLE -->
<section>
  <div class="wrap">
    <div class="stack-head"><h2>The people behind this work</h2><p>Senior experience from inside the business, not theory from the outside.</p></div>
    <div class="people">
      <div class="card person">
        <img src="assets/bren-headshot.jpg" alt="Brendan Ellis" style="object-position:55% 40%" />
        <h3>Brendan Ellis</h3><p class="title">Founder</p>
        <p>ACCA Fellow and former Head of Data at Shawbrook Bank and Pantheon. Twenty years inside Big 4, banking, private equity and media, now helping owner-led businesses get their time back.</p>
        <div class="tags"><span class="tag">Strategy</span><span class="tag">Process</span><span class="tag">Data &amp; AI</span></div>
        <a class="lnk" href="https://www.linkedin.com/in/brendanmellis" target="_blank" rel="noopener">LinkedIn</a>
      </div>
      <div class="card person" style="background:var(--teal-pale);border-color:transparent">
        {ico(I['org'])}
        <h3>Specialist partners</h3><p class="title">Brought in when the job needs them</p>
        <p>Cyber security, data engineering, branding and software builds, delivered by people we know and trust, under one Corbelle plan.</p>
        <a class="lnk" href="partners.html">How we work with partners →</a>
      </div>
    </div>
  </div>
</section>

<!-- BLOCK + INCLUDED -->
<section class="tint">
  <div class="wrap two-text">
    <div>
      <span class="lab">How we deliver</span>
      <h2 style="font-size:clamp(28px,3.4vw,40px);margin-bottom:18px">{bt}</h2>
      <p>{bp}</p>{dur}
      <a class="link-arrow" href="https://cal.com/brennie/30min" target="_blank" rel="noopener">Book a free time audit →</a>
    </div>
    <div class="card">
      <span class="lab">What's included</span>
      <ul class="checklist">{checks}</ul>
    </div>
  </div>
</section>

<!-- FAQ -->
<section>
  <div class="wrap">
    <div class="head center"><p class="eyebrow">Common questions</p><h2>{p['name']} questions</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>

<!-- ALSO EXPLORE -->
<section class="sand">
  <div class="wrap">
    <div class="stack-head"><p class="eyebrow">Also explore</p></div>
    <div class="grid3">{explore}</div>
  </div>
</section>

<!-- SEE IT IN ACTION -->
<section>
  <div class="wrap">
    <div class="stack-head"><p class="eyebrow">See it in action</p></div>
    <a class="card offer" href="case-studies.html" style="max-width:560px">
      <span class="lab">{cl}</span><h3>{ct}</h3><p>{cd}</p><span class="more">Read case study →</span>
    </a>
  </div>
</section>

<!-- GET STARTED -->
<section class="closing">
  <div class="wrap">
    <p class="eyebrow">Get started</p>
    <h2>Ready to get your week back?</h2>
    <p>Book a free 30-minute time audit. We'll look at how your week runs and tell you where to start.</p>
    <div class="stacked">{CTA}</div>
  </div>
</section>

'''
    head = re.sub(r'<title>.*?</title>', f"<title>{p['name']} — Corbelle</title>", HEAD)
    open(p['file'], 'w').write(head + '<nav></nav>\n\n' + body + FOOT)
    print('wrote', p['file'])

for p in PAGES:
    build(p)

# What we do: point each card at its page
s = open('services.html').read()
for p in PAGES:
    if f'href="{p["file"]}">Learn more' in s: continue
    pat = rf'(<div class="card offer" id="{p["anchor"]}">.*?<p class="outcome">.*?</p>)(\s*</div>)'
    s = re.sub(pat, lambda m: m.group(1) + f'\n        <a class="more" href="{p["file"]}">Learn more →</a>' + m.group(2), s, count=1, flags=re.S)
for p in PAGES:
    s = s.replace(f'<li><a href="#{p["anchor"]}">', f'<li><a href="{p["file"]}">')
s = s.replace('<li><a href="#strategy">', '<li><a href="strategy-leadership.html">')
open('services.html', 'w').write(s)
print('services links:', s.count('Learn more →'))
