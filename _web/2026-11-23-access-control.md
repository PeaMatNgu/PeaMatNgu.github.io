---
title: "Access Control — Learning Notes"
date: 2026-11-23
summary: "Ghi chú về các loại Access Control và hướng kiểm thử quyền truy cập."
platform: "PortSwigger Web Security Academy"
learning_topic: "Web Vulnerabilities"
tags:
  - web-vulnerability
  - access-control
  - idor
  - bola
---

## Bản chất và khái niệm

Lỗ hổng Access Control liên quan đến việc xử lý người dùng nào được truy cập dữ liệu, endpoint, chức năng nào.

### Vertical access control

Kiểm soát quyền theo cấp bậc vai trò, nếu user bình thường có thể truy cập, sử dụng chức năng của người quản trị  leo thang đặc quyền theo chiều dọc.

Lỗi này xảy ra do không verify role người dùng mà chỉ ẩn endpoint của người quản trị, người dùng vẫn có thể đoán ra và truy cập.

### Horizontal access control

Kiểm soát quyền giữa người cùng cấp, liên quan đến các lỗ hổng như IDOR/BOLA, người dùng A có thể xem, sửa được tài nguyên, dữ liệu của người dùng B.

### Context-dependent access control

Phụ thuộc vào trạng thái hoặc thứ tự thao tác, người dùng có thể thực hiện các hành động đáng nhẽ ra không thể xuất hiện trong chuỗi ban đầu. Ví dụ: Thanh toán đơn hàng rồi nhưng vẫn sửa được giỏ hàng, hay hủy đơn khi đơn đã được giao…

Một số website làm lộ URL trong robots.txt, tuy nhiên phát hiện URL không đồng nghĩa với có lỗ hổng, cần kiểm thử lại.

## Cách khai thác

### Khai thác vertical access control

Kiểm tra robots.txt xem có thông tin gì nhạy cảm lọt ra không.

Kiểm tra mã nguồn html, mở Dev Tools và tìm các chuỗi nhạy cảm thường liên quan đến quản trị viên.

Nếu như server hoạt động kiểu, chặn method POST kèm theo endpoint nguy hiểm như xóa user, ví dụ attacker vẫn gửi request đến endpoint bình thường như `POST / HTTP/1.1`, nhưng họ có thể thêm HTTP Headers X-Original-URL hay X-Rewrite-URL để viết lại URL thực sự muốn gửi request đến. Khi này frontend pass điều kiện vì không thấy endpoint nhạy cảm trong request, nhưng backend xử lý thì hiểu endpoint được định tuyến  Thực hiện hành vi vượt quá quyền.

Cấu hình sai ở Backend, xử lý 1 endpoint nhưng hỗ trợ nhiều kiểu HTTP method (GET, POST, PATCH) nhưng chỉ verify 1 loại method  attacker lợi dụng method khác vẫn khiến server thực thi hành động mong muốn.

### Khai thác horizontal access control

Server xử lý lỗi chỉ lấy query parameter từ request mà không kiểm tra tài nguyên đó thuộc về ai  người dùng A có thể xem tài nguyên của người dùng B  Chỉ cần truyền tham số tài nguyên của B là xem được

Server phức tạp hóa GUID, nhưng giá trị này vẫn bị lộ và không có cơ chế verify  Vẫn xảy ra Insecure Direct Object Reference (IDOR) bình thường.

Server xử lý bằng cách verify giá trị Referer (URL trước đó dẫn người dùng đến trang hiện tại), giả sử server so khớp Referer trước đó là “/admin”, thì thực hiện request, nhưng tham số này phía client có thể sửa tùy ý nên không đáng tin cậy.

Nếu như server verify theo vị trí địa lý, địa chỉ IP thì attacker có thể sử dụng VPN hay Proxy hoặc Tor để bypass.
