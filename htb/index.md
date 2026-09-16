---
layout: default
title: HackTheBox Machine Labs
permalink: /htb/
description: Write-ups for Hack The Box machines.
---
<section class="page-hero shell"><p class="eyebrow">Collection / HTB</p><h1>HackTheBox Machine Labs</h1><p>Structured notes covering enumeration, exploitation, and privilege escalation in lab environments.</p></section>
<section class="listing shell" aria-label="Hack The Box write-up list">
{% assign entries = site.htb | sort: 'date' | reverse %}
{% if entries.size > 0 %}<div class="post-grid">{% for post in entries %}{% include post-card.html post=post %}{% endfor %}</div>{% else %}<div class="empty-state"><p class="empty-code">_htb/</p><h2>No machine write-ups yet</h2><p>Add a Markdown file to <code>_htb</code>; it will appear here automatically.</p></div>{% endif %}
</section>
