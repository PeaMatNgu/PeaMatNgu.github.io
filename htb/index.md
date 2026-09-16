---
layout: default
title: HackTheBox Machine Labs
permalink: /htb/
description: Write-up các máy lab Hack The Box.
---
<section class="page-hero shell"><p class="eyebrow">Collection / HTB</p><h1>HackTheBox Machine Labs</h1><p>Ghi chép có cấu trúc từ enumeration đến khai thác và leo thang đặc quyền trong môi trường lab.</p></section>
<section class="listing shell" aria-label="Danh sách Hack The Box write-up">
{% assign entries = site.htb | sort: 'date' | reverse %}
{% if entries.size > 0 %}<div class="post-grid">{% for post in entries %}{% include post-card.html post=post %}{% endfor %}</div>{% else %}<div class="empty-state"><p class="empty-code">_htb/</p><h2>Chưa có machine write-up</h2><p>Thêm file Markdown vào <code>_htb</code>; bài viết sẽ tự động xuất hiện tại đây.</p></div>{% endif %}
</section>

