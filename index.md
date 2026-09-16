---
layout: default
title: Trang chủ
permalink: /
---

<section class="hero shell">
  <div class="hero-copy">
    <p class="eyebrow">Security notes / Labs / Write-ups</p>
    <h1>Cao Trần Thành Trung</h1>
    <p class="hero-role">Cybersecurity Student <span aria-hidden="true">·</span> CTF Player</p>
    <p class="hero-bio">Ghi lại hành trình học an toàn thông tin qua CTF, phòng lab và nghiên cứu Binary Exploitation.</p>
    <div class="hero-links" aria-label="Liên hệ và hồ sơ">
      <a class="button button-primary" href="mailto:thanhtrungcaotran@gmail.com">Email</a>
      <a class="button" href="https://github.com/PeaMatNgu" rel="me noopener" target="_blank">GitHub <span aria-hidden="true">↗</span></a>
      {% if site.author.linkedin != empty %}<a class="button" href="{{ site.author.linkedin }}" rel="me noopener" target="_blank">LinkedIn <span aria-hidden="true">↗</span></a>{% endif %}
      {% if site.author.cv != empty %}<a class="button" href="{{ site.author.cv | relative_url }}">Tải CV</a>{% endif %}
    </div>
  </div>
  <div class="hero-visual">
    <div class="avatar-frame">
      <img src="{{ site.author.avatar | relative_url }}" width="320" height="320" alt="Ảnh đại diện tạm thời của Cao Trần Thành Trung">
    </div>
    <div class="availability"><span aria-hidden="true"></span> Open to learning & collaboration</div>
  </div>
</section>

<section class="section shell" aria-labelledby="focus-title">
  <div class="section-heading">
    <div><p class="eyebrow">Lĩnh vực tập trung</p><h2 id="focus-title">Ghi chú từ quá trình thực hành</h2></div>
  </div>
  <div class="category-grid">
    <a class="category-card" href="{{ '/ctf/' | relative_url }}"><span class="category-index">01</span><h3>CTF Write-ups</h3><p>Phân tích thử thách, quy trình giải và bài học rút ra.</p><strong>{{ site.ctf | size }} bài viết <span aria-hidden="true">→</span></strong></a>
    <a class="category-card" href="{{ '/htb/' | relative_url }}"><span class="category-index">02</span><h3>HackTheBox Labs</h3><p>Enumeration, khai thác và leo thang đặc quyền trên máy lab.</p><strong>{{ site.htb | size }} bài viết <span aria-hidden="true">→</span></strong></a>
    <a class="category-card" href="{{ '/binary-exploitation/' | relative_url }}"><span class="category-index">03</span><h3>Binary Exploitation</h3><p>Ghi chú nền tảng, phân tích binary và kỹ thuật khai thác.</p><strong>{{ site.binary | size }} bài viết <span aria-hidden="true">→</span></strong></a>
    <a class="category-card" href="{{ '/achievements/' | relative_url }}"><span class="category-index">04</span><h3>Achievements</h3><p>Chứng chỉ, cuộc thi và các cột mốc đã được xác minh.</p><strong>Xem thành tích <span aria-hidden="true">→</span></strong></a>
  </div>
</section>

{% assign all_posts = site.ctf | concat: site.htb | concat: site.binary | sort: 'date' | reverse %}
<section class="section shell" aria-labelledby="latest-title">
  <div class="section-heading">
    <div><p class="eyebrow">Mới cập nhật</p><h2 id="latest-title">Bài viết gần đây</h2></div>
  </div>
  {% if all_posts.size > 0 %}
    <div class="post-grid">{% for post in all_posts limit: 6 %}{% include post-card.html post=post %}{% endfor %}</div>
  {% else %}
    <div class="empty-state"><p class="empty-code">// no entries yet</p><h3>Chưa có bài viết công khai</h3><p>Các write-up đầu tiên sẽ xuất hiện tự động tại đây sau khi được thêm vào collection.</p></div>
  {% endif %}
</section>

