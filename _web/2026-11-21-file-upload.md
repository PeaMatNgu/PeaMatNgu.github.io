---
title: "File Upload — Learning Notes"
date: 2026-11-21
summary: "Ghi chú về bản chất, cách khai thác và cơ chế phòng chống lỗ hổng File Upload."
platform: "PortSwigger Web Security Academy"
tags:
  - web-vulnerability
  - file-upload
  - rce
---

## Bản chất và khái niệm

Lỗ hổng File Upload là lỗ hổng gây ra do chức năng upload 1 file, 1 tệp hay 1 ảnh lên một trang web. Thông thường server chỉ mong muốn nhận được những loại tiệp được phép. Tuy nhiên, nếu như server không verify kĩ tên tệp, loại tệp, nội dung tệp, kích thước tệp được phép upload lên thì lỗ hổng có thể xảy ra.

Đây có thể là nguyên nhân chính để thực thi mã từ xa (RCE).

Để kích hoạt tệp độc hại này thì có thể sẽ cần tạo 1 HTTP request GET đến địa chỉ nơi lưu tệp để kích hoạt tệp đó trên server.

Để hiểu được cách khai thác lỗ hổng này cần phải hiểu cách web server xử lý yêu cầu truy cập tệp tĩnh. Nếu như file được tải lên là loại có thể thực thi và server có thể chạy tệp này thì response trả về sẽ là kết quả của lệnh ghi trong file đó. Ngược lại, nếu vẫn là file có thể thực thi nhưng server không có khả năng chạy nó thì response trả về sẽ lỗi hoặc sẽ là dạng text nội dung của file upload lên.

## Cơ chế ngăn chặn

Sử dụng allow-list thay vì blacklist

Phân loại và xác định loại tệp được upload lên bằng magic bytes thay vì phần mở rộng trong request được gửi lên hay Content-Type (MIME Type) do người dùng gửi lên.

## Cách khai thác

Tạo 1 file php bình thường sử dụng “echo file_get_contents()” để lấy nội dung 1 file muốn.

Lấy nội dung trả về lệnh hệ thống bằng “ echo system($_GET[‘command’]);”, khi tạo HTTP request thì thêm tham số query string tương ứng ví dụ command = id.

Dùng Burp Repeater thay đổi trường Content-Type để bypass qua cơ chế validate dựa trên so sánh MIME Type của server.

Nếu như server vẫn cho upload các tệp, nhưng nó lại không cho server thực thi files thì ta cần thử ghi file ra đường dẫn khác ví dụ như lùi về thư mục lớn hơn bằng path traversal. Nói dễ hiểu flow khai thác sẽ là ghi file ở 1 đường dẫn khác, sau đó vẫn gửi request đến đường dẫn lưu file này để nó thực thi bình thường.

Server bật AllowOverride với 1 thư mục, attacker sẽ tải lên 1 tệp tin cấu hình thư mục con để cho phép server xử lý file php. Ý tưởng sẽ là ta upload file cấu hình ví dụ “.htaccess” với nội dung “AddType application/x-httpd-php .l33t” để khi ta upload 1 tệp với đuôi “.l33t” thì server sử dụng module mod_php để xử lý.

Server sử dụng hàm validate phân biệt chữ hoa, thường ví dụ như “str_ends_with()” để ánh xạ phần mở rộng tệp sang MIME Type  file với đuôi ví dụ như “pHp, Php,…” có thể vượt qua, nếu thêm 1 điều kiện là phần xử lý phía sau coi các file với đuôi này đều file php.

Nếu server sử dụng hàm pathinfo không cẩn thận, chỉ check đuôi mở rộng cuối tên file thì có thể bị bypass ví dụ “test.php.jpg”, hàm gây lỗi có thể có dạng như “pathinfo("exploit.php.jpg", PATHINFO_EXTENSION)”.

API có hành vi chuẩn hóa tên file ví dụ “test.php.” sẽ có thể được chuẩn hóa dấu chấm hoặc khoảng trắng cuối tên tệp  file sẽ được hiểu là file php và thực thi.

Dùng URL encoding hoặc Unicode normalization để làm phức tạp đuôi file.

Thêm dấu chấm phẩy hoặc null byte được URL encode trước phần mở rộng tệp ví dụ “exploit.asp;.jpg”, “exploit.asp\0.jpg”, điều kiện xảy ra là server xử lý tệp bằng các hàm cấp thấp trong C/C++.

Nếu server xử lý chặn file php bằng cách xóa đuôi file, nhưng cơ chế không đầy đủ thì ta có thể lợi dụng truyền 1 payload như “test.p.phphp”.

Sử dụng exiftool để chỉnh sửa metadata của 1 hình ảnh, khi server check thì vẫn thấy là ảnh bình thường nhưng trong metadata có chứa nội dung php, nhưng điều kiện xảy ra vẫn phải do cấu hình sai để tệp được hiểu là php thì mới chạy được. (Xem chi tiết cách làm vào lại portswigger).

Cách khai thác bằng race condition, bản chất của cách này là khi tải 1 tệp lên, server bình thường sẽ cô lập trong môi trường sandbox, đặt tên tmp và kiểm tra nếu hợp lệ mới công khai. Nhưng, dev làm cách khác lưu vào file thực tế xong kiểm tra nếu không hợp lệ thì xóa, trong khoảng thời gian ngắn đấy nếu tạo HTTP request truy cập file đó thì có thể kích hoạt thành công.

Cách này sử dụng extension Turbo Intruder của Burp nhưng mà cũng éo hiểu gì lắm, nếu cần lên portswigger đọc lại :D

## Notes

### Cơ chế xử lý của 1 trang web với request bình thường

Khi gửi dữ liệu thông qua form HTML thì cần gửi 1 POST request trong đó có tham số Content-Type. Nếu như request gửi chỉ có dữ liệu văn bản thì cần khai báo application/x-www-form-urlencoded, nhưng nếu upload tệp hay ảnh,… thì cần sử dụng multipart/form-data.

Hãy xem thử 1 request này, để hiểu cơ chế hoạt động nếu dữ liệu được gửi lên bao gồm nhiều kiểu dữ liệu, thành phần khác nhau.

```http
POST /images HTTP/1.1
Host: normal-website.com
Content-Length: 12345
Content-Type: multipart/form-data; boundary=---------------------------012345678901234567890123456

-----------------------------012345678901234567890123456
Content-Disposition: form-data; name="image"; filename="example.jpg"
Content-Type: image/jpeg

[...binary content of example.jpg...]

-----------------------------012345678901234567890123456
Content-Disposition: form-data; name="description"

This is an interesting description of my image.

-----------------------------012345678901234567890123456
Content-Disposition: form-data; name="username"

wiener

-----------------------------012345678901234567890123456--
```

Mỗi trường trong form được chia thành các phần riêng biệt, mỗi phần đều chứa Content-Disposition, chứa thông tin cơ bản cho trường dữ liệu tương ứng.

Các phần có thể có header Content-Type riêng, vẫn là để cho biết MIME Type của dữ liệu được gửi thông qua trường đó.

### Tệp cấu hình của 1 trang web và điều kiện cho phép ghi đè

Ta cần biết khái niệm này ví nó khá quan trọng cũng như ảnh hưởng đến kết quả khai thác lỗ hổng File Upload. Trên 1 trang web thông thường có 2 loại file cấu hình là file cấu hình chính (toàn cục) và file cấu hình theo thư mục.

Có 2 loại Web server chính là Apache và IIS, file cấu hình chính trên Apache sẽ là “httpd.conf hoặc apache2.conf”, IIS sẽ là “applicationHost.config”.

Ở cấp thư mục sẽ là “.htaccess” với Apache và “web.config” với IIS, bản chất ta cần biết vì các file cấu hình này nếu được cho phép ghi đè bởi người dùng thì ta có thể sửa đổi để server gọi PHP handler và xử lý file ta upload.

Tuy nhiên, điều kiện tiên quyết là trong tệp cấu hình cha phải cho phép ghi đè ở tệp cấu hình con, cụ thể là ở tham số AllowOverride. Không phải thư mục nào cũng được cấu hình để ghi đè nên cần đọc kĩ điều kiện.

Server có thể sử dụng cách xác thực 1 số đặc điểm của nội dung file được upload lên để xác minh xem tệp vừa được tải lên có đúng định dạng mong muốn không. Cụ thể nếu như tệp cần là hình ảnh mà khi kiểm tra chiều dài, chiều rộng mà không thấy có kích thước thì suy ra file được tải lên không phải ảnh.

Ngoài ra cách hiệu quả hơn là kiểm tra bằng Magic bytes của tệp, ví dụ như hình ảnh jpeg có các byte đặc trưng “FF D8 FF”.

Trên kia là những cách khai thác cho những framework cũ, đối với framework hiện đại cách làm việc của chúng mạnh hơn rất nhiều:

Đầu tiên, tải tệp vào một thư mục tạm thời được cách ly (sandboxed directory).

Đặt tên ngẫu nhiên cho tệp để tránh ghi đè những tệp đã tồn tại.

Thực hiện xác thực và kiểm tra tệp ngay trong thư mục tạm.

Chỉ chuyển tệp đến vị trí lưu trữ cuối cùng sau khi đã xác định tệp đó an toàn.
