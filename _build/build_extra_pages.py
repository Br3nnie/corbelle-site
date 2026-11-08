"""Builds ai-adoption.html, experience.html and tools.html (Hopton-style).
Usage: python3 tools/build_extra_pages.py <redesign dir>; then run tools/build_nav.py."""
import re, os, sys
os.chdir(sys.argv[1])
about = open('about.html').read()
HEAD = about[:about.index('<nav>')]
FOOT = about[about.index('<footer>'):]
BOOK = 'https://cal.com/brennie/30min'
CTA = f'<a class="btn btn-light" href="{BOOK}" target="_blank" rel="noopener">Book a free time audit</a>'

def write(fn, title, body):
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', HEAD)
    open(fn, 'w').write(head + '<nav></nav>\n\n' + body + FOOT)
    print('wrote', fn)

def closing(h, p):
    return f'''<section class="closing">
  <div class="wrap">
    <p class="eyebrow">Get started</p>
    <h2>{h}</h2>
    <p>{p}</p>
    <div class="stacked">{CTA}</div>
  </div>
</section>

'''

PEOPLE = '''<section>
  <div class="wrap">
    <div class="stack-head"><h2>The people behind the work</h2><p>Senior experience from inside the business, plus specialists when the job needs them.</p></div>
    <div class="people">
      <div class="card person">
        <img src="assets/bren-headshot.jpg" alt="Brendan Ellis" style="object-position:55% 40%" />
        <h3>Brendan Ellis</h3><p class="title">Founder</p>
        <p>ACCA Fellow and former Head of Data at Shawbrook Bank and Pantheon. Twenty years inside Big 4, banking, private equity and media.</p>
        <div class="tags"><span class="tag">Strategy</span><span class="tag">Process</span><span class="tag">Data &amp; AI</span></div>
        <a class="lnk" href="https://www.linkedin.com/in/brendanmellis" target="_blank" rel="noopener">LinkedIn</a>
      </div>
      <div class="card person" style="background:var(--teal-pale);border-color:transparent">
        <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="5" rx="1"/><rect x="3" y="16" width="6" height="5" rx="1"/><rect x="15" y="16" width="6" height="5" rx="1"/><path d="M12 8v4M6 16v-2h12v2"/></svg></div>
        <h3>Specialist partners</h3><p class="title">Brought in when the job needs them</p>
        <p>Cyber security, data engineering, branding and software builds, delivered by people we know and trust, under one Corbelle plan.</p>
        <a class="lnk" href="partners.html">How we work with partners →</a>
      </div>
    </div>
  </div>
</section>

'''

# ---------------- AI ADOPTION ----------------
areas = [
 ('01', 'AI-ready processes', 'AI on top of a messy process just makes the mess faster. We fix and simplify the process first, so AI has something sensible to work with. Most failed AI starts here.', 'time-process-audit.html'),
 ('02', 'Practical AI in everyday work', 'Drafting, summarising meetings, turning notes into quotes and chasing the routine stuff, set up inside the tools your team already uses.', 'automation-ai.html'),
 ('03', 'Safe AI rules', 'One simple standard for what data can go where and who sees the bill, with freedom for each team to choose tools inside it.', 'strategy-leadership.html'),
 ('04', 'AI skills and adoption', 'Training and coaching so people actually use AI well, and leaders can explain why. Access is easy. Judgement is the hard part.', 'change-management.html'),
]
area_html = ''.join(f'''
      <a class="card area" href="{h}"><span class="n">{n}</span><h3>{t}</h3><p>{d}</p><span class="more">Learn more →</span></a>''' for n, t, d, h in areas)
built = [
 ('Spoken quotes, priced in seconds', 'A phone app for a trade business: say the job out loud and get a priced PDF quote to send from site.'),
 ('AI Use Case Gameplan', 'Pressure-tests an AI idea before time, money and political capital are committed.'),
 ('AI Cost Validator', 'Models the full running cost of an AI use case: seats, usage, review time and overhead.'),
 ('Our own AI chief of staff', 'Evening voice notes become a prioritised brief by morning. We run Corbelle on the same tools we recommend.'),
]
built_html = ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in built)
ai = f'''<header class="page-hero svc-hero" style="padding-bottom:88px">
  <div class="wrap">
    <div>
      <p class="crumbs"><a href="index.html">Home</a> / <a href="services.html">What we do</a> / AI Adoption</p>
      <p class="eyebrow" style="margin-top:18px">AI adoption</p>
      <h1 style="margin-top:6px">Practical AI for owner-led businesses</h1>
      <p class="sub">AI is only as useful as the process underneath it. We get the basics right first, then apply AI where it actually saves time: fewer manual steps, quicker answers and less admin.</p>
      <div style="margin-top:30px;display:flex;gap:12px;flex-wrap:wrap">{CTA}<a class="btn btn-ghost" href="#areas">Start with the basics</a></div>
    </div>
    <div class="ba-panel"><small>What changes</small>
      <div class="ba-line"><s>"We should do something with AI"</s><i>→</i><b>A short list of uses that pay</b></div>
      <div class="ba-line"><s>Staff pasting client data anywhere</s><i>→</i><b>One clear standard</b></div>
      <div class="ba-line"><s>Licences nobody uses</s><i>→</i><b>Tools people use every day</b></div>
      <div class="ba-line"><s>Hype</s><i>→</i><b>Hours back</b></div>
    </div>
  </div>
</header>

<div class="quote-band">
  <div class="wrap">
    <p class="eyebrow">Our approach</p>
    <blockquote>"Most AI projects never pay back. It's not a technology problem. It's a people and process problem, and that's where we start."</blockquote>
    <cite>Brendan Ellis, Founder</cite>
  </div>
</div>

<section id="areas">
  <div class="wrap">
    <div class="stack-head">
      <p class="eyebrow">Four areas</p>
      <h2>Where we apply AI</h2>
      <p>Each builds on the last. You can start anywhere, but most clients start with the process.</p>
    </div>
    <div class="grid2">{area_html}
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <div class="stack-head">
      <p class="eyebrow">What we've built</p>
      <h2>We don't just recommend AI. We build with it.</h2>
      <p>We build and use our own AI tools, which is how we know what works for a small business and what doesn't.</p>
    </div>
    <div class="built">
      <div class="grid2">{built_html}</div>
      <div class="start-box">
        <span class="lab">Where to start</span>
        <h3>Is AI worth it for you?</h3>
        <a class="row" href="/usecasegameplan">Test an AI idea<span>Gameplan →</span></a>
        <a class="row" href="/aicost">What would it cost to run?<span>Validator →</span></a>
        <a class="row" href="index.html#calculator">What is busywork costing you?<span>Calculator →</span></a>
        <a class="btn btn-light" href="{BOOK}" target="_blank" rel="noopener">Book a free time audit</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="stack-head"><p class="eyebrow">Further reading</p><h2>Useful starting points</h2></div>
    <div class="grid3">
      <a class="card offer" href="tuesday-strategy.html"><span class="lab">Article</span><h3>You don't need an AI strategy. You need a Tuesday strategy.</h3><p>Why the boring wins pay for the shiny ones.</p></a>
      <a class="card offer" href="chatgpt-padded-quote.html"><span class="lab">Article</span><h3>Before you approve a ChatGPT-padded tech quote</h3><p>What to check when an AI-written proposal suddenly costs a quarter more.</p></a>
      <a class="card offer" href="who-sees-the-ai-bill.html"><span class="lab">Guide</span><h3>Who sees the AI bill?</h3><p>Usage costs, who owns them, and when AI in a core process gets expensive.</p></a>
    </div>
  </div>
</section>

''' + closing('Ready to talk about AI?', "Thirty minutes. An honest read on where AI could genuinely help your business, and what needs to be in place first.")
write('ai-adoption.html', 'AI Adoption — Corbelle', ai)

# ---------------- EXPERIENCE ----------------
xp = f'''<header class="page-hero" style="padding-bottom:80px">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / Experience</p>
    <h1>Experience that speaks for itself</h1>
    <p class="sub">Twenty years inside nine organisations, from Big 4 audit to Head of Data, and now Corbelle clients from multi-country groups to trade businesses. Here's the evidence.</p>
  </div>
</header>

<section>
  <div class="wrap">
    <div class="stack-head"><h2>Proven in practice</h2><p>Selected examples. Client names are withheld unless they've said yes.</p></div>
    <div class="grid2">
      <a class="card xp-case" href="case-studies.html">
        <h3>International corporate finance group</h3><p class="who">Financial services · offices across Europe</p>
        <span class="lab">The situation</span>
        <p>The group had grown country by country, each with its own IT and licences. When a senior executive asked who could see and change what, nobody could answer it, and the board wanted comfort fast.</p>
        <span class="lab">What we delivered</span>
        <p>An independent assessment, a fair selection across three IT partners, and a governance model: one minimum security standard, with each country free to choose its own tools, AI included, inside it.</p>
        <p class="sum">Admin roles going from ~28 to 4 · one IT partner chosen · Phase 3 on the table</p>
        <div class="tags" style="margin:14px 0 0"><span class="tag">Assessment</span><span class="tag">Partner selection</span><span class="tag">Governance</span></div>
      </a>
      <a class="card xp-case" href="case-studies.html">
        <h3>Fencing &amp; landscaping firm</h3><p class="who">Trade business · South East England</p>
        <span class="lab">The situation</span>
        <p>Great on site, buried in admin. Every survey meant going back later to work out a price, and customers were left chasing for a week. Off-the-shelf apps had been tried before and didn't stick.</p>
        <span class="lab">What we delivered</span>
        <p>A phone app built around how the team already works: say the job out loud and get a priced PDF quote using the firm's own rates, sent by WhatsApp while still on site.</p>
        <p class="sum">~3 seconds to price a spoken job · no forms, no evening admin</p>
        <div class="tags" style="margin:14px 0 0"><span class="tag">Automation &amp; AI</span><span class="tag">Mobile</span></div>
      </a>
    </div>
    <a class="link-arrow" href="case-studies.html">See all case studies →</a>
  </div>
</section>

<div class="stats-plain">
  <div class="wrap">
    <div><b>20+</b><span>Years experience</span></div>
    <div><b>9</b><span>Organisations worked inside</span></div>
    <div><b>11</b><span>Conference stages</span></div>
    <div><b>2009</b><span>Chartered accountant since</span></div>
  </div>
</div>

<section class="sand">
  <div class="wrap">
    <div class="stack-head"><h2>Client feedback</h2><p>Don't take our word for it.</p></div>
    <div class="quotes">
      <div class="quote"><blockquote>This is the kind of thinking partnership I didn't know I was missing until I had it.</blockquote><cite>COO, PE-backed business</cite></div>
      <div class="quote"><blockquote>I walked into the board presentation knowing exactly what I was going to say and why.</blockquote><cite>Group MD, Family Office</cite></div>
      <div class="quote"><blockquote>Brendan's value isn't the report. It's the thinking that happens before anyone writes anything.</blockquote><cite>CEO, £200M AUM firm</cite></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="plain-offer">
      <span class="lab">Speaking</span>
      <h2>On stage, as well as in the room.</h2>
      <p>Brendan has spoken at CXO Data Summits, SuperReturn North America, CDAO UK, IDC and Microsoft Ignite, on why technology projects succeed or fail for human reasons.</p>
      <a class="link-arrow" style="margin-top:8px" href="https://speaking.brendanellis.com/" target="_blank" rel="noopener">See talks and book Brendan →</a>
    </div>
  </div>
</section>

''' + PEOPLE + closing('Want to see what we could do for you?', "Book a free time audit. We'll look at how your week runs and show you what's possible.")
write('experience.html', 'Experience — Corbelle', xp)

# ---------------- TOOLS ----------------
tools = [
 ('Live', 'Cost of busywork calculator', 'Put a number on what manual work is costing your business each year, and how much of it could come back.', 'index.html#calculator', 'Open calculator'),
 ('Live', 'Painful Process Checker', 'Spot the manual processes costing your business most, and get a short read-out of where to start.', '/check', 'Take the check'),
 ('Live', 'AI Use Case Gameplan', 'Pressure-test an AI or technology idea before time, money and political capital are committed.', '/usecasegameplan', 'Open assessment'),
 ('Live', 'AI Cost Validator', 'Model the full running cost of an AI use case, including seats, usage, review time and overhead.', '/aicost', 'Open calculator'),
 ('Live', 'Cost of Inaction Diagnostic', 'Work out the financial case for acting now, before the drag of doing nothing becomes unavoidable.', '/costofinaction', 'Open diagnostic'),
 ('Live', 'Magnetic Leadership', 'Assess how your leadership presence is experienced: where it creates pull, and where it creates drag.', '/magneticleadership', 'Open assessment'),
 ('Launching next', 'Clarity Engine', 'Turn high-stakes choices into decision memos, review loops and pattern analysis over time.', '/clarity-engine', 'View product'),
 ('Paid diagnostic', 'The 12-Minute Read', "Corbelle's paid diagnostic: a short, structured outside read on your business.", 'https://12minsread.com', 'Find out more'),
]
th = ''.join(f'''
      <a class="card tool" href="{u}"{' target="_blank" rel="noopener"' if u.startswith('http') else ''}><span class="status">{s}</span><h3>{t}</h3><p>{d}</p><span class="more">{l} →</span></a>''' for s, t, d, u, l in tools)
tl = f'''<header class="page-hero" style="padding-bottom:80px">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / Insights / Tools</p>
    <h1>Tools</h1>
    <p class="sub">Free and paid tools to help you put a number on a problem, test an idea or start a better conversation before you spend anything.</p>
  </div>
</header>

<section>
  <div class="wrap">
    <div class="stack-head"><p class="eyebrow">Available now</p><h2>Start with the tool closest to the question you have.</h2></div>
    <div class="grid3">{th}
    </div>
  </div>
</section>

''' + closing('Want a human read instead?', "Book a free 30-minute time audit and we'll go through it together.")
write('tools.html', 'Tools — Corbelle', tl)
