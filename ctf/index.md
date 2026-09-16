---
layout: default
title: CTF Write-ups
permalink: /ctf/
description: Các bài phân tích và write-up thử thách Capture The Flag.
---
<section class="page-hero shell"><p class="eyebrow">Collection / CTF</p><h1>CTF Write-ups</h1><p>Quy trình giải, kỹ thuật khai thác và những bài học có thể tái sử dụng từ các thử thách CTF.</p></section>
<section class="listing shell" aria-label="Danh sách CTF write-up">
{% assign entries = site.ctf | sort: 'date' | reverse %}
{% if entries.size > 0 %}<div class="post-grid">{% for post in entries %}{% include post-card.html post=post %}{% endfor %}</div>{% else %}<div class="empty-state"><p class="empty-code">_ctf/</p><h2>Chưa có CTF write-up</h2><p>Thêm file Markdown vào <code>_ctf</code>; bài viết sẽ tự động xuất hiện tại đây.</p></div>{% endif %}
</section>

