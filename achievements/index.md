---
layout: default
title: Achievements
permalink: /achievements/
description: Verified certificates and competition results for Lighth0use.
---
<section class="page-hero shell">
  <p class="eyebrow">Verified milestones</p>
  <h1>Achievements</h1>
  <p>Certificates and public competition results earned with team Lighth0use.</p>
</section>

{% assign ctftime = site.data.ctftime %}
{% if ctftime.team %}
<section class="achievement-overview shell" aria-labelledby="ctftime-heading">
  <div class="achievement-heading-row">
    <div>
      <p class="eyebrow">CTFtime profile</p>
      <h2 id="ctftime-heading">{{ ctftime.team.name }}</h2>
    </div>
    <a class="button" href="{{ ctftime.team.url }}" target="_blank" rel="noopener">View on CTFtime <span aria-hidden="true">↗</span></a>
  </div>
  <div class="achievement-stats">
    <div><strong>#{{ ctftime.team.rating_place }}</strong><span>Global rank · {{ ctftime.team.rating_year }}</span></div>
    <div><strong>#{{ ctftime.team.country_place }}</strong><span>Vietnam rank</span></div>
    <div><strong>{{ ctftime.team.rating_points }}</strong><span>Rating points</span></div>
    <div><strong>{{ ctftime.team.event_count }}</strong><span>Recorded events</span></div>
  </div>
  <p class="achievement-updated">Automatically synchronized from CTFtime · Last data change: {{ ctftime.updated_at | date: "%d %B %Y" }}</p>
</section>
{% endif %}

<section class="listing shell" aria-labelledby="certificates-heading">
  <div class="achievement-section-heading">
    <p class="eyebrow">Certificate gallery</p>
    <h2 id="certificates-heading">Certified results</h2>
  </div>
  {% if site.data.achievements and site.data.achievements.size > 0 %}
  <div class="achievement-grid">
  {% for item in site.data.achievements %}
    <article class="achievement-card">
      <a class="achievement-image" href="{{ item.certificate | default: item.image | relative_url }}" target="_blank" aria-label="View certificate: {{ item.title }}">
        <img src="{{ item.image | relative_url }}" alt="{{ item.alt | default: item.title }}" loading="lazy">
      </a>
      <div class="achievement-body">
        <p class="achievement-date">{{ item.date }}</p>
        <h3>{{ item.title }}</h3>
        {% if item.result %}<p class="achievement-result">{{ item.result }}</p>{% endif %}
        <p>{{ item.description }}</p>
        <div class="achievement-links">
          {% if item.certificate %}<a href="{{ item.certificate | relative_url }}" target="_blank">View certificate <span aria-hidden="true">↗</span></a>{% endif %}
          {% if item.verification %}<a href="{{ item.verification }}" target="_blank" rel="noopener">CTFtime result <span aria-hidden="true">↗</span></a>{% endif %}
        </div>
      </div>
    </article>
  {% endfor %}
  </div>
  {% else %}
  <div class="empty-state"><h3>No certificates added yet</h3></div>
  {% endif %}
</section>

{% if ctftime.events and ctftime.events.size > 0 %}
<section class="achievement-results shell" aria-labelledby="results-heading">
  <div class="achievement-section-heading">
    <p class="eyebrow">Competition history</p>
    <h2 id="results-heading">CTFtime results</h2>
    <p>Public team results are refreshed every Monday. Rankings shown here follow CTFtime and may use a different division or scoring scope from an organizer-issued certificate.</p>
  </div>
  <div class="achievement-table-wrap">
    <table class="achievement-table">
      <thead><tr><th scope="col">Date</th><th scope="col">Event</th><th scope="col">Rank</th><th scope="col">CTF points</th></tr></thead>
      <tbody>
      {% for event in ctftime.events %}
        <tr>
          <td><time datetime="{{ event.date }}">{{ event.date | date: "%d %b %Y" }}</time></td>
          <td><a href="{{ event.url }}" target="_blank" rel="noopener">{{ event.title }} <span aria-hidden="true">↗</span></a></td>
          <td>#{{ event.place }}</td>
          <td>{{ event.points }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</section>
{% endif %}
