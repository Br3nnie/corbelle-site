"""Builds insights.html and the article pages.
Usage: python3 tools/build_articles.py <site dir>; then run tools/build_nav.py."""
import re, os, sys, html
os.chdir(sys.argv[1])
about = open('about.html').read()
HEAD = about[:about.index('<nav>')]
FOOT = about[about.index('<footer>'):]
BOOK = 'https://cal.com/brennie/30min'
IMG = re.search(r'src="([^"]*)bren-headshot\.jpg"', open('strategy-leadership.html').read()).group(1)

PHOTOS = {
 'five-manual-jobs': ('Bills, a calculator and paperwork spread across a desk', 'Giorgio Tomassetti', 'https://unsplash.com/photos/bills-calculator-and-a-laptop-financial-tasks-underway-LtU_A0NHHtU'),
 'tuesday-strategy': ('Two people planning on a whiteboard', 'Kaleidico', 'https://unsplash.com/photos/two-people-drawing-on-whiteboard-26MJGnCM0Wc'),
 'busy-is-a-symptom': ('A man with his head in his hands at a laptop', 'Vitaly Gariev', 'https://unsplash.com/photos/man-holding-head-in-frustration-at-desk-with-laptop-bu5LEzvtAKY'),
 'chatgpt-padded-quote': ('Two people reviewing a document at a table', 'Olena Kholina', 'https://unsplash.com/photos/two-people-reviewing-documents-at-a-table-MhqUBTxQ3Hw'),
 'who-sees-the-ai-bill': ('Someone reviewing paperwork with a calculator and laptop', 'Kelly Sikkema', 'https://unsplash.com/photos/person-reviewing-documents-with-calculator-and-laptop-0oZpRxG5Hkk'),
}

ARTICLES = [
dict(slug='five-manual-jobs', tag='Process', month='Nov 2026', num='01',
 title='The 5 manual jobs every growing business is still doing',
 dek='And the cheapest way to stop each one.',
 desc='Five manual jobs quietly eating hours in growing UK businesses, and the cheapest way to stop each one, usually with tools you already own.',
 related=[('time-process-audit.html', 'Time &amp; Process Audit'), ('automation-ai.html', 'Automation &amp; AI Quick Wins')],
 body='''
<p>Every business I walk into thinks it's unusual.</p>
<p>It isn't.</p>
<p>The industry changes. The software changes. The same five manual jobs turn up almost every time, quietly eating hours nobody has ever added up.</p>
<p>Here they are, and the cheapest way to stop each one.</p>

<h2>1. Typing the same thing in twice</h2>
<p>An order comes in by email. Someone types it into the system. Then into a spreadsheet. Then into the invoice.</p>
<p>Three places. Three chances to get it wrong.</p>
<p><strong>The fix:</strong> decide where that information lives, once. Then connect everything else to it. Most of the time the systems you already pay for can talk to each other. Nobody has switched it on.</p>

<h2>2. Chasing</h2>
<p>Chasing invoices. Chasing timesheets. Chasing approvals. Chasing the person who was meant to chase.</p>
<p>Chasing feels like work. It isn't. It's a reminder a computer could send.</p>
<p><strong>The fix:</strong> automatic reminders, with a named person who only steps in when the reminder doesn't work.</p>

<h2>3. The report that takes a morning</h2>
<p>Every Monday someone pulls numbers from four places, pastes them into a spreadsheet, tidies the formatting and emails it round.</p>
<p>Ask who reads it. Really reads it.</p>
<p>In one business I worked in, half the "urgent" reports hadn't been opened in six months.</p>
<p><strong>The fix:</strong> retire anything nobody reads. Automate what's left, straight from the source.</p>

<h2>4. Quotes written in the evening</h2>
<p>The owner visits the job, then goes home and writes the quote at the kitchen table.</p>
<p>Meanwhile the customer is getting prices from two competitors.</p>
<p><strong>The fix:</strong> a standard pricing template, and capturing the details while you're still on site. For one trade business we built a phone app where the surveyor says the job out loud and gets a priced quote in seconds.</p>

<h2>5. "Where's the latest version?"</h2>
<p>Five copies of the same spreadsheet. Names like FINAL_v3_USE_THIS_ONE.</p>
<p>Nobody trusts the numbers, so everybody keeps their own.</p>
<p><strong>The fix:</strong> one shared file or system, one owner, and switch the old copies off on day one. Not day thirty.</p>

<h2>What these five have in common</h2>
<p>None of them needs a big transformation programme. Most don't need new software.</p>
<p>They need someone to notice, put a number on the cost, and fix the process before automating it.</p>
<p>Because automating a bad process just makes the mistakes happen faster.</p>
<p>Start by counting. Ask each team: what do you do every week that a computer, or a better process, should be doing? Then multiply the hours by what those people cost.</p>
<p>The number is usually bigger than anyone expected.</p>
'''),
dict(slug='tuesday-strategy', tag='AI', month='Nov 2026', num='02',
 title="You don't need an AI strategy. You need a Tuesday strategy.",
 dek='Why the boring wins pay for the shiny ones.',
 desc="Most owner-led businesses don't need an AI strategy deck. They need to know what AI should do on a normal Tuesday. Here's how to find it.",
 related=[('ai-adoption.html', 'AI Adoption'), ('automation-ai.html', 'Automation &amp; AI Quick Wins')],
 body='''
<p>"We need an AI strategy."</p>
<p>I hear it every week. From boards. From investors. From owners who've just come back from a conference.</p>
<p>Here's my honest answer: <strong>you probably don't.</strong></p>
<p>Not yet.</p>

<h2>Strategies are written for a Monday</h2>
<p>A strategy deck gets presented on a Monday. Big ambitions. Transformation. A roadmap with arrows.</p>
<p>Then Tuesday arrives.</p>
<p>Someone is still re-typing orders. Someone is still chasing invoices. Someone is still writing the weekly report by hand.</p>
<p>The deck didn't touch any of it.</p>

<h2>What a Tuesday strategy looks like</h2>
<p>A Tuesday strategy asks one question:</p>
<p><strong>On a normal day, what are our people doing that they shouldn't have to?</strong></p>
<p>Then it picks the three answers that cost the most, and fixes those first.</p>
<ul>
<li>Drafting the same email twenty times a week</li>
<li>Summarising meetings nobody remembers</li>
<li>Turning site notes into quotes</li>
<li>Pulling numbers from three places into one report</li>
</ul>
<p>Boring? Absolutely.</p>
<p>Valuable? More than most "AI strategies" I've seen.</p>

<h2>Why boring wins first</h2>
<p>Most AI projects never pay back. It's not a technology problem. It's a people and process problem.</p>
<p>Big, shiny projects fail because nobody changed how the work actually gets done. Small, boring wins succeed because the people doing the work can see the difference by Friday.</p>
<p>And when they can see it, they want more. That's how adoption actually happens. Not through a launch email. Through relief.</p>

<h2>Three steps for this week</h2>
<p><strong>1. Ask, don't tell.</strong> Sit with the people doing the work and ask what eats their week.</p>
<p><strong>2. Fix the process first.</strong> If a job shouldn't exist, don't automate it. Delete it.</p>
<p><strong>3. Set one simple rule.</strong> What data can go into AI tools and what can't. One page. Not a policy nobody reads.</p>
<p>Then pick one job and make it disappear.</p>
<p>Do that a few times, and you'll have something better than an AI strategy.</p>
<p>You'll have proof.</p>
'''),
dict(slug='busy-is-a-symptom', tag='People', month='Nov 2026', num='03',
 title="Busy isn't a badge. It's a symptom.",
 dek="What your team's overtime is really telling you.",
 desc="When everyone is busy, it's tempting to hire. But busy is usually a symptom of broken processes, not a shortage of people.",
 related=[('change-management.html', 'Change Management'), ('time-process-audit.html', 'Time &amp; Process Audit')],
 body='''
<p>"How's the team?"</p>
<p>"Busy."</p>
<p>Said with a little pride, isn't it? Busy sounds like growth. Busy sounds like demand.</p>
<p>Sometimes it is.</p>
<p>More often, busy is a symptom.</p>

<h2>What busy usually means</h2>
<p>When I map how a team spends its week, the pattern is nearly always the same. The real work, the thing you hired them for, is squeezed into the gaps between everything else.</p>
<p>Re-keying. Chasing. Checking someone else's spreadsheet. Fixing the mistakes that re-keying created.</p>
<p>That isn't a capacity problem. It's a process problem wearing a capacity problem's clothes.</p>

<h2>The expensive response</h2>
<p>The natural answer to "we're too busy" is to hire.</p>
<p>So you hire. The new person learns the same broken process. Six months later, they're busy too.</p>
<p>I spoke to one business that had to employ one and a half extra people just to work around a new system that didn't do what they needed. The system was meant to save time. It created a job.</p>

<h2>The cost nobody counts</h2>
<p>There's a human cost too.</p>
<p>Good people don't leave because they're busy. They leave because they're busy doing work that doesn't matter, and nobody seems to notice.</p>
<p>Overtime spent on genuine growth feels like progress. Overtime spent on copy-and-paste feels like a trap.</p>

<h2>What to do instead</h2>
<p><strong>Ask a different question.</strong> Not "how busy are you?" but "what are you busy WITH?"</p>
<p><strong>Count it.</strong> Hours per week on manual, repeated tasks, multiplied by what those people cost. Put a pound sign on it.</p>
<p><strong>Fix before you hire.</strong> Remove the steps that shouldn't exist. Automate the ones that must. Then see if you still need the extra person.</p>
<p>Sometimes you will. That's fine. At least you'll be hiring for growth, not for workarounds.</p>
<p>Busy isn't a badge.</p>
<p>It's your business telling you something. Worth listening.</p>
'''),
dict(slug='chatgpt-padded-quote', tag='Buying', month='Nov 2026', num='04',
 title='Before you approve a ChatGPT-padded tech quote',
 dek='What to check when an AI-written proposal suddenly costs a quarter more.',
 desc='Suppliers and buyers are using AI to write and review tech proposals, and scope is creeping up. Five checks before you sign.',
 related=[('strategy-leadership.html', 'Strategy &amp; Fractional Leadership'), ('joined-up-systems.html', 'Joined-Up Systems')],
 body='''
<p>A business owner told me recently about a technology proposal they'd been sent.</p>
<p>Before signing, they ran it through ChatGPT to check it.</p>
<p>ChatGPT suggested extra features, extra security, extra integrations.</p>
<p>The price went up by a quarter.</p>
<p>Not one of those additions was needed.</p>

<h2>AI is very good at "more"</h2>
<p>Ask an AI tool to review a proposal and it will rarely say "this is too much". It will tell you what's missing. It will think of edge cases. It will make everything sound important.</p>
<p>That's useful for spotting gaps. It's dangerous for deciding scope.</p>
<p>Because the AI doesn't know your business. It doesn't know your budget, your team, or that you have 60 staff, not 6,000.</p>

<h2>And suppliers use it too</h2>
<p>Proposals are now easier to write than ever. Longer documents, more options, more polish.</p>
<p>A long, polished proposal looks thorough. It isn't always right.</p>

<h2>Five checks before you sign</h2>
<p><strong>1. What problem does each line solve?</strong> If nobody can name the problem in one sentence, it's a nice-to-have.</p>
<p><strong>2. What do we already own?</strong> Most businesses pay for software that already does half of what's being proposed.</p>
<p><strong>3. What happens if we leave it out?</strong> If the answer is "nothing much, for a year", leave it out for a year.</p>
<p><strong>4. Who will actually use it?</strong> Features nobody uses still cost licences and maintenance.</p>
<p><strong>5. What does it cost to run, not just to build?</strong> Support, licences, AI usage and the time your team spends looking after it.</p>

<h2>Use AI, but keep the judgement</h2>
<p>I'm not saying don't use AI to review proposals. Use it. It's a great second pair of eyes.</p>
<p>But treat its suggestions as questions, not answers.</p>
<p>The decision needs someone who understands your business, your people and your numbers. Ideally someone with no reason to make the project bigger.</p>
<p>If you'd like a second opinion on a proposal before you sign, that's exactly the kind of conversation a free time audit is for.</p>
'''),
dict(slug='who-sees-the-ai-bill', tag='Guide', month='Nov 2026', num='05',
 title='Who sees the AI bill?',
 dek='Usage costs, who owns them, and when AI in a core process gets expensive.',
 desc='AI tools are cheap to try and easy to forget. Once they sit inside core processes, usage costs grow quietly. Who owns the bill in your business?',
 related=[('ai-adoption.html', 'AI Adoption'), ('/aicost', 'AI Cost Validator')],
 body='''
<p>I asked a senior executive a simple question recently.</p>
<p>"When AI is built into your critical processes and the usage costs go up, who sees the bill?"</p>
<p>There was a pause.</p>
<p>"I don't."</p>
<p>They're not alone.</p>

<h2>Cheap to try. Easy to forget.</h2>
<p>Most AI tools start small. A few licences. A free tier. A card on someone's expenses.</p>
<p>Then it works. People use it more. Someone connects it to a process. Then another.</p>
<p>And usage-based pricing means the bill grows with every task, every document and every question.</p>
<p>Nobody decided to spend more. It just happened.</p>

<h2>Three costs people miss</h2>
<p><strong>1. Usage, not seats.</strong> Many AI tools charge by how much you use them, not just how many people have access. Busy month, bigger bill.</p>
<p><strong>2. Review time.</strong> AI output still needs checking. If someone spends twenty minutes checking what took the AI two, count the twenty.</p>
<p><strong>3. Duplication.</strong> Three teams, three different AI tools, three subscriptions doing the same job.</p>

<h2>When it gets expensive</h2>
<p>Experimenting is cheap. The cost changes when AI moves from "helpful extra" to "the process doesn't work without it".</p>
<p>At that point you're exposed. Prices change. Usage grows. And switching off isn't an option anymore.</p>
<p>That's not a reason to avoid AI. It's a reason to know what you're signing up for.</p>

<h2>Four simple rules</h2>
<p><strong>Name an owner.</strong> One person sees every AI bill, every month.</p>
<p><strong>Know the unit cost.</strong> What does one quote, one summary or one report cost to produce with AI, including review time?</p>
<p><strong>Set a standard.</strong> Agree which tools are approved. Teams can choose freely, within the list.</p>
<p><strong>Check quarterly.</strong> Is each tool still earning its place?</p>
<p>AI can save a lot of time. Just make sure someone is watching what the time costs.</p>
<p>Our AI Cost Validator models the full running cost of an AI use case, including review time and overhead, before you commit.</p>
'''),
]

def words(h):
    return len(re.sub(r'<[^>]+>', ' ', h).split())

def write(fn, title, desc, body):
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', HEAD)
    head = re.sub(r'\s*<meta name="description"[^>]*>', '', head)
    head = head.replace('</title>', f'</title>\n<meta name="description" content="{html.escape(desc, quote=True)}" />', 1)
    open(fn, 'w').write(head + '<nav></nav>\n\n' + body + FOOT)
    print('wrote', fn)

def card(a, cls='post'):
    return f'''<a class="{cls}" href="{a['slug']}.html"><div class="thumb"><img src="{IMG}insights/{a['slug']}.jpg" alt="{PHOTOS[a['slug']][0]}" loading="lazy" /></div><div class="b"><div class="meta"><span class="tag">{a['tag']}</span>{a['month']} · {max(2, round(words(a['body'])/220))} min</div><h3>{a['title']}</h3><p>{a['dek']}</p></div></a>'''

for i, a in enumerate(ARTICLES):
    mins = max(2, round(words(a['body']) / 220))
    rel = ''.join(f'<a class="row" href="{h}">{t}<span>→</span></a>' for h, t in a['related'])
    others = [x for x in ARTICLES if x is not a][:2]
    more = ''.join(card(x) for x in others)
    body = f'''<header class="page-hero" style="padding-bottom:72px">
  <div class="wrap">
    <p class="crumbs"><a href="/">Home</a> / <a href="insights.html">Insights</a> / {a['tag']}</p>
    <p class="eyebrow" style="margin-top:18px">{a['tag']}</p>
    <h1 style="margin-top:6px;max-width:860px">{a['title']}</h1>
    <p class="sub">{a['dek']}</p>
    <div class="byline"><img src="{IMG}bren-headshot.jpg" alt="Brendan Ellis" /><span><b>Brendan Ellis</b>{a['month']} · {mins} min read</span></div>
  </div>
</header>

<section style="padding-top:64px">
  <div class="wrap article-wrap">
    <article class="article"><figure class="article-figure"><img src="{IMG}insights/{a['slug']}.jpg" alt="{PHOTOS[a['slug']][0]}" /><figcaption>Photo: <a href="{PHOTOS[a['slug']][2]}?utm_source=corbelle&amp;utm_medium=referral" target="_blank" rel="noopener">{PHOTOS[a['slug']][1]}</a> on <a href="https://unsplash.com/?utm_source=corbelle&amp;utm_medium=referral" target="_blank" rel="noopener">Unsplash</a></figcaption></figure>{a['body']}</article>
    <aside class="article-side">
      <div class="start-box">
        <span class="lab">Where Corbelle helps</span>
        <h3>Want this fixed, not just read about?</h3>
        {rel}
        <a class="btn btn-light" href="{BOOK}" target="_blank" rel="noopener">Book a free time audit</a>
      </div>
    </aside>
  </div>
</section>

<section class="sand">
  <div class="wrap">
    <div class="stack-head"><p class="eyebrow">More insights</p><h2>Keep reading</h2></div>
    <div class="grid2">{more}</div>
    <a class="link-arrow" href="insights.html">All articles →</a>
  </div>
</section>

'''
    write(f"{a['slug']}.html", f"{a['title']} — Corbelle", a['desc'], body)

grid = ''.join(card(a) for a in ARTICLES)
ins = f'''<header class="page-hero" style="padding-bottom:80px">
  <div class="wrap">
    <p class="crumbs"><a href="/">Home</a> / Insights</p>
    <h1>Latest thinking</h1>
    <p class="sub">Plain-English takes on process, automation, AI and getting your team's time back.</p>
  </div>
</header>

<section>
  <div class="wrap">
    <div class="grid3">{grid}</div>
  </div>
</section>

<section class="tint">
  <div class="wrap two-text">
    <div>
      <span class="lab">Tools</span>
      <h2 style="margin-bottom:14px">Put a number on it.</h2>
      <p>Free tools to work out what busywork costs you, test an AI idea, or model what it would cost to run.</p>
      <a class="link-arrow" href="tools.html">See all tools →</a>
    </div>
    <div class="start-box">
      <span class="lab">Popular</span>
      <h3>Start here</h3>
      <a class="row" href="/#calculator">Cost of busywork calculator<span>→</span></a>
      <a class="row" href="/usecasegameplan">AI Use Case Gameplan<span>→</span></a>
      <a class="row" href="/aicost">AI Cost Validator<span>→</span></a>
    </div>
  </div>
</section>

<section class="closing">
  <div class="wrap">
    <p class="eyebrow">Get started</p>
    <h2>Rather talk it through?</h2>
    <p>Book a free 30-minute time audit and we'll look at your week together.</p>
    <div class="stacked"><a class="btn btn-light" href="{BOOK}" target="_blank" rel="noopener">Book a free time audit</a></div>
  </div>
</section>

'''
write('insights.html', 'Insights — Corbelle', "Plain-English articles from Corbelle on process, automation, AI adoption and getting your team's time back.", ins)

# expose cards for other pages
open('_build/_article_cards.html', 'w').write('\n'.join(card(a) for a in ARTICLES))
