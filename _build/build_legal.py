"""Builds privacy.html, terms.html and cookies.html (drafts — have them checked before relying on them).
Usage: python3 tools/build_legal.py <site dir>; then run tools/build_nav.py."""
import re, os, sys, html
os.chdir(sys.argv[1])
about = open('about.html').read()
HEAD = about[:about.index('<nav>')]
FOOT = about[about.index('<footer>'):]

ENTITY = 'Corbelle Limited'
NUMBER = '08106968'
ADDRESS = '21 Seely Road, London, England, SW17 9QP'
ICO_NUMBER = ''  # add once the ICO confirms it, then rerun this script
UPDATED = 'November 2026'
EMAIL = 'hello@corbelle.ai'

def page(fn, title, h1, desc, body):
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', HEAD)
    head = re.sub(r'\s*<meta name="description"[^>]*>', '', head)
    head = head.replace('</title>', f'</title>\n<meta name="description" content="{html.escape(desc, quote=True)}" />', 1)
    b = f'''<header class="page-hero" style="padding-bottom:64px">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / {h1}</p>
    <h1>{h1}</h1>
    <p class="sub">Last updated: {UPDATED}</p>
  </div>
</header>

<section style="padding-top:56px">
  <div class="wrap">
    <article class="article legal">{body}</article>
  </div>
</section>

'''
    open(fn, 'w').write(head + '<nav></nav>\n\n' + b + FOOT)
    print('wrote', fn)

WHO = f'<p>This website is run by {ENTITY}, a company registered in England and Wales (company number {NUMBER}) with its registered office at {ADDRESS}. On this page, "Corbelle", "we" and "us" mean that company.</p>'

privacy = f'''
<h2>Who we are</h2>
{WHO}
<p>We are the controller of the personal data described here{' and are registered with the Information Commissioner&#x27;s Office (registration number ' + ICO_NUMBER + ')' if ICO_NUMBER else ''}. If you have any questions, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

<h2>What we collect and why</h2>
<p><strong>When you send an enquiry.</strong> Your name, business name, work email, team size and anything you tell us in your message. Your message is delivered to our inbox by FormSubmit, a form-to-email service. We use it to reply to you and, if we work together, to manage that relationship. Our lawful basis is legitimate interests (responding to people who contact us) or taking steps at your request before entering a contract.</p>
<p><strong>When you book a call.</strong> Bookings are handled by Cal.com. They collect your name, email and the details you choose to share, and pass them to us so we can hold the meeting. Lawful basis: taking steps at your request before entering a contract.</p>
<p><strong>When you subscribe to our newsletter.</strong> Your first name, last name and email address, held by our email provider, Kit. We use them to send you our newsletter. Lawful basis: your consent, which you can withdraw at any time using the unsubscribe link in every email.</p>
<p><strong>When you use our tools.</strong> Calculators such as the cost of busywork calculator run in your browser. We don't store what you enter unless you choose to send it to us.</p>
<p><strong>When you visit the site.</strong> Our hosting provider keeps standard server logs (such as IP address, browser type and pages requested) for security and to keep the site running. We don't use analytics or advertising tracking.</p>

<h2>Who we share it with</h2>
<p>We don't sell your data. We share it only with providers who help us run Corbelle, under contracts that require them to protect it:</p>
<ul>
<li>Vercel (website hosting)</li>
<li>FormSubmit (delivers contact form messages to our inbox)</li>
<li>Cal.com (meeting bookings)</li>
<li>Kit (newsletter)</li>
<li>Google (web fonts, which means your browser requests font files from Google's servers)</li>
<li>Our email, CRM and file storage providers</li>
</ul>
<p>If we bring in a specialist partner on a project, we only share what they need for that work, and we'll tell you first.</p>

<h2>International transfers</h2>
<p>Some of these providers process data outside the UK, including in the United States. Where they do, we rely on approved safeguards such as the UK International Data Transfer Agreement or Addendum, or the UK–US data bridge.</p>

<h2>How long we keep it</h2>
<ul>
<li>Enquiries that don't lead to work: up to 2 years after our last contact.</li>
<li>Client records: for the length of our relationship and up to 6 years afterwards, for legal and accounting reasons.</li>
<li>Newsletter: until you unsubscribe.</li>
</ul>

<h2>Your rights</h2>
<p>Under UK data protection law you can ask to see the personal data we hold about you, correct it, delete it, restrict or object to how we use it, or receive a copy to take elsewhere. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll respond within one month.</p>
<p>If you're unhappy with how we've handled your data, you can complain to the Information Commissioner's Office at <a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a>. We'd appreciate the chance to put it right first.</p>

<h2>Changes</h2>
<p>We'll update this page if anything changes, and change the date at the top.</p>
'''

terms = f'''
<h2>About these terms</h2>
{WHO}
<p>These terms cover your use of this website. By using it, you agree to them. They don't cover paid work. Any engagement with Corbelle is governed by a separate written agreement.</p>

<h2>Using the site</h2>
<p>You may use this site for your own information and to get in touch with us. Please don't misuse it: no attempts to break, overload or gain unauthorised access to the site, and no copying of its content for commercial use without our permission.</p>

<h2>Our content</h2>
<p>The text, articles, tools, designs and images on this site belong to Corbelle or are used with permission. You're welcome to share links and short quotes with credit.</p>

<h2>Not professional advice</h2>
<p>Our articles, examples and case studies are general information. They aren't advice for your specific situation. Results described in case studies reflect those clients' circumstances and aren't a promise of future results.</p>
<p>Our calculators and tools give estimates based on the figures you enter and the assumptions shown. Use them as a starting point for a conversation, not as the basis for a financial decision on their own.</p>

<h2>Recommendations and partners</h2>
<p>We sometimes recommend software, suppliers or specialist partners. Some of them pay us a revenue share. Where they do, we'll tell you before you decide. Any contract you sign with a third party is between you and them.</p>

<h2>Links to other sites</h2>
<p>We link to other websites, including our booking and newsletter providers. We're not responsible for their content or how they handle your data. Please read their own terms and privacy policies.</p>

<h2>Liability</h2>
<p>We work hard to keep this site accurate and available, but we can't guarantee it will always be complete, current or uninterrupted. To the extent the law allows, we're not liable for any loss arising from your use of the site or reliance on its content. Nothing in these terms limits liability that can't be limited by law, such as for death or personal injury caused by negligence, or fraud.</p>

<h2>Law</h2>
<p>These terms are governed by the law of England and Wales, and the courts of England and Wales have jurisdiction.</p>

<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
'''

cookies = f'''
<h2>The short version</h2>
<p>This website doesn't set any cookies of its own, and we don't use analytics, advertising or tracking cookies. That's why you won't see a cookie banner.</p>

<h2>What does happen</h2>
<p><strong>Fonts.</strong> Our typefaces are loaded from Google Fonts. Your browser connects to Google's servers to download them, which shares your IP address with Google. Google Fonts doesn't set cookies.</p>
<p><strong>Hosting.</strong> Our hosting provider, Vercel, may use strictly necessary technical measures to deliver the site securely. These don't track you.</p>
<p><strong>Third-party sites.</strong> When you click through to book a call (Cal.com), subscribe to the newsletter (Kit), visit LinkedIn or open one of our separately hosted tools, you're on their site and their cookie policies apply.</p>

<h2>If this changes</h2>
<p>If we ever add analytics or other non-essential cookies, we'll ask for your consent first and update this page.</p>

<h2>Managing cookies</h2>
<p>You can block or delete cookies through your browser settings at any time. Blocking cookies won't affect how this site works.</p>

<h2>Contact</h2>
<p>Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>. See also our <a href="privacy.html">privacy policy</a>.</p>
'''

page('privacy.html', 'Privacy policy — Corbelle', 'Privacy policy', 'How Corbelle collects, uses and protects your personal data, and your rights under UK data protection law.', privacy)
page('terms.html', 'Website terms — Corbelle', 'Website terms', 'The terms for using the Corbelle website, its articles and tools.', terms)
page('cookies.html', 'Cookie policy — Corbelle', 'Cookie policy', 'Corbelle does not use analytics, advertising or tracking cookies. Here is what happens when you visit.', cookies)
