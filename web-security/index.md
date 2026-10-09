---
layout: default
title: Learning Notes
permalink: /web-security/
description: Notes about web vulnerabilities, exploitation techniques, and defensive concepts.
---
<section class="page-hero shell"><p class="eyebrow">Collection / Learning Notes</p><h1>Learning Notes</h1><p>Personal study notes covering web vulnerability concepts, exploitation flows, payloads, and defensive techniques.</p></section>
<section class="listing shell" aria-label="Learning Notes article list">
{% assign entries = site.web | sort: 'date' | reverse %}
{% if entries.size > 0 %}<div class="post-grid">{% for post in entries %}{% include post-card.html post=post %}{% endfor %}</div>{% else %}<div class="empty-state"><p class="empty-code">_web/</p><h2>No learning notes yet</h2><p>Add a Markdown file to <code>_web</code>; it will appear here automatically.</p></div>{% endif %}
</section>
