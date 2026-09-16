---
layout: default
title: Achievements
permalink: /achievements/
description: Certificates, competitions, and cybersecurity milestones.
---
<section class="page-hero shell"><p class="eyebrow">Verified milestones</p><h1>Achievements</h1><p>Certificates, competition results, and milestones, with verification details whenever available.</p></section>
<section class="listing shell" aria-label="Achievement gallery">
{% if site.data.achievements and site.data.achievements.size > 0 %}
<div class="achievement-grid">
{% for item in site.data.achievements %}
  <article class="achievement-card">
    <a class="achievement-image" href="{{ item.image | relative_url }}" target="_blank" aria-label="View full-size image: {{ item.title }}"><img src="{{ item.image | relative_url }}" alt="{{ item.alt | default: item.title }}" loading="lazy"></a>
    <div class="achievement-body"><p class="achievement-date">{{ item.date }}</p><h2>{{ item.title }}</h2>{% if item.result %}<p class="achievement-result">{{ item.result }}</p>{% endif %}<p>{{ item.description }}</p>{% if item.verification %}<a href="{{ item.verification }}" target="_blank" rel="noopener">View verification <span aria-hidden="true">↗</span></a>{% endif %}</div>
  </article>
{% endfor %}
</div>
{% else %}
<div class="empty-state"><p class="empty-code">_data/achievements.yml</p><h2>No achievements added yet</h2><p>This section stays empty until verified certificates or results are provided.</p></div>
{% endif %}
</section>
