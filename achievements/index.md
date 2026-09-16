---
layout: default
title: Achievements
permalink: /achievements/
description: Chứng chỉ, cuộc thi và các cột mốc an toàn thông tin.
---
<section class="page-hero shell"><p class="eyebrow">Verified milestones</p><h1>Achievements</h1><p>Chứng chỉ, kết quả cuộc thi và các cột mốc được lưu cùng thông tin xác minh khi có.</p></section>
<section class="listing shell" aria-label="Thư viện thành tích">
{% if site.data.achievements and site.data.achievements.size > 0 %}
<div class="achievement-grid">
{% for item in site.data.achievements %}
  <article class="achievement-card">
    <a class="achievement-image" href="{{ item.image | relative_url }}" target="_blank" aria-label="Xem ảnh lớn: {{ item.title }}"><img src="{{ item.image | relative_url }}" alt="{{ item.alt | default: item.title }}" loading="lazy"></a>
    <div class="achievement-body"><p class="achievement-date">{{ item.date }}</p><h2>{{ item.title }}</h2>{% if item.result %}<p class="achievement-result">{{ item.result }}</p>{% endif %}<p>{{ item.description }}</p>{% if item.verification %}<a href="{{ item.verification }}" target="_blank" rel="noopener">Xem xác minh <span aria-hidden="true">↗</span></a>{% endif %}</div>
  </article>
{% endfor %}
</div>
{% else %}
<div class="empty-state"><p class="empty-code">_data/achievements.yml</p><h2>Chưa có thành tích được thêm</h2><p>Khu vực này đang để trống để không hiển thị chứng chỉ hoặc kết quả chưa được cung cấp.</p></div>
{% endif %}
</section>

