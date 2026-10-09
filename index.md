---
layout: default
title: Home
permalink: /
---

<section class="hero">
  <div class="shell hero-inner">
    <p class="eyebrow">Personal cybersecurity blog</p>
    <h1>Learn, practice,<br>and <em>document.</em></h1>
    <p class="hero-bio">CTFs, Hack The Box, Binary Exploitation, Learning Notes, and everything I learn on my cybersecurity journey.</p>
    <div class="hero-links" aria-label="Contact and profiles">
      <a class="button button-light" href="mailto:thanhtrungcaotran@gmail.com">Contact</a>
      <a class="text-link" href="https://github.com/PeaMatNgu" rel="me noopener" target="_blank">GitHub <span aria-hidden="true">↗</span></a>
      {% if site.author.linkedin != empty %}<a class="text-link" href="{{ site.author.linkedin }}" rel="me noopener" target="_blank">LinkedIn <span aria-hidden="true">↗</span></a>{% endif %}
      {% if site.author.cv != empty %}<a class="text-link" href="{{ site.author.cv | relative_url }}">Download CV</a>{% endif %}
    </div>
  </div>
</section>

<section class="intro-band">
  <div class="shell intro-grid">
    <p class="intro-label">Hello, I am</p>
    <div>
      <h2>Cao Trần Thành Trung</h2>
      <p>A Cybersecurity student and CTF player. This is where I organize what I learn, publish write-ups, and document my progress.</p>
    </div>
  </div>
</section>

<section class="section shell" aria-labelledby="focus-title">
  <div class="section-heading editorial-heading">
    <p class="eyebrow">Explore the blog</p>
    <h2 id="focus-title">Five main topics</h2>
  </div>
  <div class="category-grid">
    <a class="category-card" href="{{ '/ctf/' | relative_url }}"><span class="category-index">01</span><h3>CTF Write-ups</h3><p>Challenge analysis, solution processes, and lessons learned.</p><strong>{{ site.ctf | size }} posts <span aria-hidden="true">→</span></strong></a>
    <a class="category-card" href="{{ '/htb/' | relative_url }}"><span class="category-index">02</span><h3>HackTheBox Labs</h3><p>Enumeration, exploitation, and privilege escalation in lab environments.</p><strong>{{ site.htb | size }} posts <span aria-hidden="true">→</span></strong></a>
    <a class="category-card" href="{{ '/binary-exploitation/' | relative_url }}"><span class="category-index">03</span><h3>Binary Exploitation</h3><p>Core concepts, binary analysis, and exploitation techniques.</p><strong>{{ site.binary | size }} posts <span aria-hidden="true">→</span></strong></a>
    <a class="category-card" href="{{ '/web-security/' | relative_url }}"><span class="category-index">04</span><h3>Learning Notes</h3><p>Structured study notes on web security concepts, exploitation techniques, payloads, and defensive approaches.</p><strong>{{ site.web | size }} posts <span aria-hidden="true">→</span></strong></a>
    <a class="category-card" href="{{ '/achievements/' | relative_url }}"><span class="category-index">05</span><h3>Achievements</h3><p>Certificates, competitions, and verified milestones.</p><strong>View achievements <span aria-hidden="true">→</span></strong></a>
  </div>
</section>

{% assign all_posts = site.ctf | concat: site.htb | concat: site.binary | concat: site.web | sort: 'date' | reverse %}
<section class="latest-section">
  <div class="shell">
    <div class="section-heading editorial-heading">
      <p class="eyebrow">Learning journal</p>
      <h2 id="latest-title">Recent posts</h2>
    </div>
    {% if all_posts.size > 0 %}
      <div class="post-grid">{% for post in all_posts limit: 6 %}{% include post-card.html post=post %}{% endfor %}</div>
    {% else %}
      <div class="empty-state"><h3>No posts yet</h3><p>New write-ups will appear here automatically when they are added to a collection.</p></div>
    {% endif %}
  </div>
</section>
