---
layout: default
title: CTF Write-ups
permalink: /ctf/
description: Analysis and write-ups for Capture The Flag challenges.
---
<section class="page-hero shell"><p class="eyebrow">Collection / CTF</p><h1>CTF Write-ups</h1><p>Solution processes, exploitation techniques, and reusable lessons from CTF challenges.</p></section>
<section class="listing shell" aria-label="CTF write-up list">
{% assign entries = site.ctf | sort: 'date' | reverse %}
{% if entries.size > 0 %}<div class="post-grid">{% for post in entries %}{% include post-card.html post=post %}{% endfor %}</div>{% else %}<div class="empty-state"><p class="empty-code">_ctf/</p><h2>No CTF write-ups yet</h2><p>Add a Markdown file to <code>_ctf</code>; it will appear here automatically.</p></div>{% endif %}
</section>
