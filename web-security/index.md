---
layout: default
title: Learning Notes
permalink: /web-security/
description: Organized notes from cybersecurity study, grouped by topic.
---
<section class="page-hero shell"><p class="eyebrow">Collection / Learning Notes</p><h1>Learning Notes</h1><p>Organized notes from my cybersecurity studies, grouped by topic for easier navigation.</p></section>
<section class="listing shell" aria-label="Learning Notes article list">
{% assign entries = site.web | sort: 'date' | reverse %}
{% assign topic_groups = entries | group_by: 'learning_topic' %}
{% if entries.size > 0 %}
<div class="learning-groups">
  {% for topic in topic_groups %}
  <section class="learning-group" aria-labelledby="learning-topic-{{ forloop.index }}">
    <div class="learning-group-header">
      <div><p class="eyebrow">Study topic</p><h2 id="learning-topic-{{ forloop.index }}">{{ topic.name | default: 'Other Notes' }}</h2></div>
      <p class="learning-group-count">{{ topic.items | size }} notes</p>
    </div>
    <div class="post-grid">{% for post in topic.items %}{% include post-card.html post=post %}{% endfor %}</div>
  </section>
  {% endfor %}
</div>
{% else %}<div class="empty-state"><p class="empty-code">_web/</p><h2>No learning notes yet</h2><p>Add a Markdown file to <code>_web</code>; it will appear here automatically.</p></div>{% endif %}
</section>
