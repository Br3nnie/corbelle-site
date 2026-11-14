"""The single list of www.corbelle.ai pages: public (sitemap + structured data) or hidden (noindex).
Add every new page here; build_seo.py fails if a page is missing."""

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
