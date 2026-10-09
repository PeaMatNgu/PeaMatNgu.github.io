---
title: "XML Injection"
date: 2026-09-02
platform: "PortSwigger Web Security Academy"
tags:
  - xxe
  - xml
  - web-security
---

## Bản chất và khái niệm chung

- XML Injection là lỗ hổng web liên quan đến việc server nhận dữ liệu XML, XML parser có tính năng đọc tài nguyên bên ngoài  attacker lợi dụng tính năng đó để để bắt server đọc thứ mà attacker muốn.

- Có rất nhiều mục đích để khai thác lỗ hổng này: XXE to retrieve files, XXE to perform SSRF attacks, blind XXE exfiltrate data out-of-band, blind XXE to retrieve data via error messages.

## Các loại XXE (Mục đích)

### Exploiting XXE to retrieve files

- Mục đích lấy nội dung của một file bất kỳ từ hệ thống file của server, có hai cách để thực hiện. Cách 1 là thêm hoặc chỉnh sửa 1 phần tử DOCTYPE để định nghĩa một external entity (trong đó chứa đường dẫn file cần đọc).

- Chỉnh sửa một giá trị dữ liệu trong XML — cụ thể là giá trị mà ứng dụng sẽ đưa vào response — để sử dụng external entity vừa định nghĩa.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/01-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/01-code-table.png" alt="Code example 1 from XML Injection" loading="lazy">
  </a>
</figure>

- SYSTEM: thông báo cho parser rằng giá trị của entity phải lấy được từ 1 tài nguyên bên ngoài, thay vì chuỗi được khai báo trực tiếp trong ENTITY.

- Trong các lỗ hổng XXE ngoài thực tế, XML gửi lên thường chứa rất nhiều trường dữ liệu. Bất kỳ trường nào trong số đó cũng có thể được ứng dụng sử dụng và đưa vào response. Vì vậy cần thử từng trường 1 và xem response trả về như nào.

### Exploiting XXE to perform SSRF attacks

- Khác với mục đích là đọc file nhạy cảm của loại trên, với kiểu tấn công này chúng hướng đến việc thực thi SSRF, lỗ hổng này nghiêm trọng vì server có thể tạo HTTP requests đến bất kì URL nào mà server có thể truy cập.

- Kĩ thuật để thực hiện kiểu tấn công này là định nghĩa 1 “external entity” có giá trị là URL target, rồi đặt entity đó vào một thẻ XML mà máy chủ xử lý.

- Nếu response trả về hiển thị toàn bộ nội dung truy vấn thì đây là kết nối hai chiều với hệ thống backend. Còn nếu kết quả trả về không rõ ràng, cần phải sử dụng tấn công Blind SSRF để tấn công.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/02-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/02-code-table.png" alt="Code example 2 from XML Injection" loading="lazy">
  </a>
</figure>

### XInclude attacks

- Trong trường hợp không kiểm soát được toàn bộ XML, cụ thể là không thể tạo DOCTYPE external entity mới, ta không thể khai thác lỗ hổng XML Injection bình thường lúc này ta sử dụng Xinclude. Đây là tính năng của XML cho phép một XML nhúng nội dung từ tài nguyên khác.

- Giao diện HTTP request sẽ khác đi, vì ta không còn host được toàn bộ XML nữa nên mặc dù ở Backend vẫn xử lý logic theo kiểu parser XML nhưng ta chỉ có thể thay đổi giá trị truyền vào, chứ không định nghĩa được thuộc tính mới nữa.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/03-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/03-code-table.png" alt="Code example 3 from XML Injection" loading="lazy">
  </a>
</figure>

- “xmlns:xi="http://www.w3.org/2001/XInclude”: Cấu trúc mẫu để kích hoạt tính năng XML Inclusions (Xinclude).

- “xi:include”: Ra lệnh cho XML parser lấy nội dung từ một tài nguyên bên ngoài và chèn nó vào đây.

- “parse = text”: Ép parser lấy nội dung dưới dạng text

- “href=…”: Chỉ ra tài nguyên cần đọc.

### Blind XXE with out-of-band interaction

- Bản chất của việc sử dụng phương pháp out-of-band là vì XML parser vẫn xử lý file XML, server vẫn có thể đọc nhưng response không hiển thị giá trị đó. Vì vậy ta phải khiến XML parser trên server kết nối đến một địa chỉ do attacker host. Nếu như thấy trong log có DNS request và HTTP request thì có thể chứng minh XML parser đã xử lý external entity.

- External Entity = http://Burp_collaborator_subdomain.

- Trong trường hợp Entity thông thường bị chặn, tức là “&amp;xxe;” không được dùng thì sử dụng đến XML parameter entity, nó được sử dụng ngay trong DOCTYPE, không cần chèn vào node như &lt;productID&gt;.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/04-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/04-code-table.png" alt="Code example 4 from XML Injection" loading="lazy">
  </a>
</figure>

### Exploiting blind XXE to exfiltrate data out-of-band

- Tuy có thể chứng minh là server có gửi HTTP request đến server bên ngoài, tuy nhiên mục đích chính của lỗ hổng vẫn là đọc các file nhạy cảm. Ý tưởng là attacker triển khai 1 DTD độc hại trên hệ thống chúng điều khiển  gửi XML tới server victim và yêu cầu victim tải DTD đó  victim gửi nội dung file nhạy cảm tới attacker server.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/05-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/05-code-table.png" alt="Code example 5 from XML Injection" loading="lazy">
  </a>
</figure>

- &lt;!ENTITY % file SYSTEM "file:///etc/passwd"&gt;: Khai báo 1 XML parameter entity, đây là file mà ta muốn đọc

- “%eval”: Định nghĩa 1 parameter entity “eval”, chứa 1 dynamic declaration entity (Thực thể khai báo động) paramater entity khác “exfiltrate”.

- “%exfiltrate”: Có mục đích gửi dữ liệu từ “%file” đến server của attacker.

- “&amp;#x25”: Là kí hiệu “%”, mục đích là “trì hoãn” việc xử lý ký tự % cho đến khi entity eval được mở rộng. Nếu viết % trực tiếp, parser có thể cố xử lý nó quá sớm và gây lỗi cú pháp.

- Phải sử dụng “%eval” vì không phải parser nào cũng cho phép dùng “%file” trực tiếp khai báo trong “%exfiltrate”.

- Sau đó cho file .dtd này lên server attacker host, rồi submit payload XXE bình thường để victim server gửi request đến attacker server.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/06-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/06-code-table.png" alt="Code example 6 from XML Injection" loading="lazy">
  </a>
</figure>

- Đôi khi sẽ không đọc được 1 số file như “/etc/passwd” vì chúng có các kí tự như cách, dòng mới,… Ở trường hợp này nên lấy dữ liệu từ file “/etc/hostname”.

### Exploiting blind XXE to retrieve data via error messages

- Ý tưởng của cách khai thác này là lợi dụng error message để làm kênh trả dữ liệu. Ta cố tình yêu cầu XML parser mở một file không tồn tại, nhưng chèn nội dung của file nhạy cảm vào tên của file không tồn tại.

- Khi parser báo lỗi, nó sẽ in ra đường dẫn đó. Nếu ứng dụng trả lỗi về response, nội dung file sẽ xuất hiện trong response.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/07-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/07-code-table.png" alt="Code example 7 from XML Injection" loading="lazy">
  </a>
</figure>

- “%file”: Đại diện cho nội dung của file /etc/passwd

- “%eval”: Chứa thực thể khai báo động, ở đây là “%error”.

- “%error”: Là 1 parameter entity cố gắng truy cập đường dẫn file không tồn tại kia. Khi đấy server báo lỗi, trả về đường dẫn chứa cả nội dung của “%file”.

### Exploiting blind XXE by repurposing a local DTD

- Ý tưởng: Tận dụng 1 file DTD đã tồn tại trên server victim thay vì tải DTD từ server attacker, cần phải dùng kỹ thuật này nếu server victim bị chặn kết nối outbound  Không thể tải 	DTD từ xa

- Với ví dụ này, giả sử có 1 file DTD được lưu ở “/usr/local/app/schema.dtd”, trong file này định nghĩa thực thể “custom_entity”, attacker sẽ lợi dụng để đánh lừa XML parser gửi tin nhắn lỗi cùng nội dung file /etc/passwd bằng các submit 1 hybrid DTD.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/08-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/08-code-table.png" alt="Code example 8 from XML Injection" loading="lazy">
  </a>
</figure>

- Nạp DTD cục bộ, khai báo “%local_dtd” trỏ tới nội dung file “/usr/local/app/schema.dtd”.

- Định nghĩa “%custom_entity”: Là một chuỗi chứa DTD khác, trong đó chứa payload tương tự như “Blind XEE to retrieve error messages”, khi schema.dtd được nạp và có chỗ sử dụng %custom_entity thì payload này sẽ có tác dụng.

- “%local_dtd;”: Đây là nạp schema.dtd, và %custom_entity đã được gọi sẵn trong file schema.dtd.

- Để tìm được file DTD có sẵn trên server thì gửi payload kèm đường dẫn vào, nếu không tồn tại sẽ trả về “FileNotFoundException:…”. Nếu tồn tại sẽ có thể xử lý tiếp bình thường hoặc phát sinh lỗi cú pháp liên quan đến nội dung DTD.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/09-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/09-code-table.png" alt="Code example 9 from XML Injection" loading="lazy">
  </a>
</figure>

### XXE attacks via file upload

- Ứng dụng tưởng đang xử lý ảnh SVG, nhưng SVG thực chất là XML. XML parser trên server được cấu hình cho phép đọc external entity.

<figure class="code-figure">
  <a href="/assets/images/web-security/xml-injection/10-code-table.png" target="_blank">
    <img src="/assets/images/web-security/xml-injection/10-code-table.png" alt="Code example 10 from XML Injection" loading="lazy">
  </a>
</figure>

- “&lt;!ENTITY xxe SYSTEM "file:///etc/hostname"&gt;”: Trỏ đến nội dung của file /etc/hostname

- “xmlns="http://www.w3.org/2000/svg"”: Khai báo namespac chuẩn của svg.

- “xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"&gt;”: Khai báo namespace cho các tính năng liên kết của SVG.

- “&lt;text font-size="16" x="0" y="16"&gt;&amp;xxe;&lt;/text&gt;”: Tạo 1 đoạn text trong ảnh nhưng mục đích chính là kích hoạt entity xxe.
