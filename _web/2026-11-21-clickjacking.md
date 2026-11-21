---
title: "Clickjacking — Learning Notes"
date: 2026-11-21
summary: "Ghi chú về cơ chế hoạt động, payload, kỹ thuật bypass và phòng chống Clickjacking."
platform: "PortSwigger Web Security Academy"
tags:
  - web-vulnerability
  - clickjacking
  - burp-suite
---

## Bản chất và khái niệm chung

Clickjacking (hay còn gọi là UI Redressing) là một kỹ thuật tấn công web, trong đó kẻ tấn công đánh lừa người dùng nhấp chuột vào một thành phần trên trang web mà họ không hề có ý định nhấp vào.

Cơ chế hoạt động: Kẻ tấn công lợi dụng hai thành phần HTML/CSS là thẻ “iframe”, thuộc tính “opacity” và “opacity”.

Thẻ “iframe” dùng để nhúng một trang web khác vào bên trong trang web hiện tại, điều kiện tiên quyết là trang đích phải cho phép nhúng kết hợp cùng định dạng css  khiến iframe gần như vô hình và điều chỉnh vị trí của nó.

“position: absolute”: Cho phép định vị iframe tại vị trí mong muốn.

“opacity: 0”: Làm iframe hoàn toàn trong suốt, nhưng vẫn có thể nhận thao tác chuột.

“z-index: 10”: Đưa iframe lên lớp phía trên những phần tử có thứ tự xếp lớp thấp hơn.

## Xây dựng payload

### Payload cơ bản thủ công

Viết bằng html bình thường, cần nhớ absolute khiến phần tử thoát khỏi luồng bố cục thông thường (normal document flow). Nghĩa là Decoy không còn chiếm chỗ trong luồng bố cục, nên iframe phía sau có thể xuất hiện tại vùng vị trí tương ứng, tạo điều kiện để hai phần tử chồng lên nhau.

relative giữ iframe trong luồng bố cục bình thường, nhưng cho phép dịch chuyển nó bằng top, left, right, bottom so với vị trí ban đầu.

```html
iframe {
    position: absolute;
    opacity: 0;
    z-index: 10;
}
```

```html
<style>
    iframe {
        position:relative;
        width:500px;
        height:700px;
        opacity: 0.0001;
        z-index: 2;
    }
    div {
        position:absolute;
        top:565px;
        left:60px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0a2a0000039e3f2381653e6100e400be.web-security-academy.net/my-account"></iframe>
```

### Payload tự động bằng ClickBandit

Clickbandit là công cụ của Burp Suite hỗ trợ tự động hóa việc tạo PoC cho quá trình đó.

### Clickjacking with prefilled from input

Một số website cho phép giá trị trong biểu mẫu được tự động điền dựa trên tham số GET nằm trong URL.

“?email=attacker@example.com”: Tham số này giúp form có sẵn nội dung trước khi người dùng nhấp nút xác nhận, nếu website hỗ trợ chức năng đó.

Điều kiện tiên quyết để xảy ra là website cho phép dữ liệu từ URL được đưa vào biểu mẫu để người dùng xác nhận.

Cách sử dụng Burp ClickBandit: Burp  Clickbandit  Copy Bandit to Clipboard  Truy cập URL ví dụ “https://target.com/my-account?email=attacker@example.com”  F12 mở Console rồi dán đoạn nãy copy vào  Nhấn start sau đó nhấp vào nút muốn kiểm tra  Nhấn Finish  Save sẽ thu được 1 file clickbandit.html  Tải file đó lên exploit server và quan sát thử  Deliver to victim.

```html
<style>
    iframe {
        position: relative;
        width: 600px;
        height: 400px;
        opacity: 0.00001;
        z-index: 2;
    }

    div {
        position: absolute;
        top: 200px;
        left: 100px;
        z-index: 1;
    }
</style>

<div>Click me</div>

<iframe src="https://example.com/change-email?email=attacker@example.com">
</iframe>
```

## Frame Busting Scripts

Frame Busting (hay Frame Breaking) là một kỹ thuật phòng chống Clickjacking bằng JavaScript, nhằm ngăn website bị nhúng vào iframe của một website khác.  Ý tưởng là website phát hiện mình đang bị nhúng vào iframe và tự thoát ra.

Ví dụ với mã nguồn sau:

```javascript
if (window.top !== window.self) {
    window.top.location = window.self.location;
}
```

Khi kiểm tra cửa sổ hiện tại và cửa sổ trên cùng trong hệ thống các frame mà không trùng nhau  điều hướng cửa sổ trên cùng đến URL của cửa sổ hiện tại.

Cách bypass có thể sử dụng thuộc tính sandbox, sandbox được thiết kế để hạn chế quyền hoạt động của nội dung bên trong iframe, giúp tăng bảo mật.

Nó có 4 giá trị là: allow-forms (Cho phép gửi biểu mẫu), allow-scripts (Cho phép thực thi JavaScript), allow-top-navigation (Cho phép iframe điều hướng cửa sổ trên cùng) và allow-same-origin (Cho phép iframe giữ origin thực thay vì bị gán origin đặc biệt).

Giả sử Frame Busting Scripts vẫn chạy nhưng nếu có thuộc tính sandbox “allow-forms” trong iframe  cho phép gửi biểu mẫu nhưng không có quyền để Js thực thi, cũng như không điều hướng được cửa sổ chính.

Nếu có cả hai giá trị “allow-forms” và “allow-scripts” cần được sử dụng khi website không gửi form trực tiếp mà dùng Javascript  Nếu không cho phép js chạy thì nút updateEmail cũng không thể hoạt động  Nhưng Frame Busting vẫn chạy nhưng không có quyền để điều hướng cửa sổ vì thiếu “allow-top-navigation”.

## Clickjacking with a DOM XSS attack

Kĩ thuật này kết hợp cả Clickjacking và XSS, điều kiện tiên quyết để có thể xảy ra là trang web phải cho nhúng 1 thẻ iframe và trong tham số của 1 request có tồn tại xử lý logic lỗi  Javascript thực thi  XSS.

Ý tưởng vẫn là tạo ra một thẻ iframe, tạo một giao nút giả và căn chỉnh sao cho khi người dùng nhấn vào nút thật của endpoint thì cũng đồng thời kích hoạt sự kiện mà đã tạo ra khi ấn nút giả, ở đây sẽ là payload XSS ứng với tham số bị lỗi.

Có thể sử dụng Burp ClickBandit để tạo ra Poc kích thước trang chính khác, từ đó tạo nút giả đúng được vị trí mà người dùng sẽ nhấn vào.

## Multistep clickjacking

Multistep Clickjacking là kỹ thuật Clickjacking nhiều bước, trong đó attacker đánh lừa nạn nhân thực hiện một chuỗi thao tác liên tiếp trên website mục tiêu thay vì chỉ một lần nhấp chuột.

Tương tự như Clickjacking thông thường, ta cần lợi dụng các thẻ <div> hoặc thẻ <iframe> để đánh lừa người dùng ấn vào, tuy nhiên mỗi bước có thể sẽ tải trang mới hoặc có bố cục mới vì vậy cần tính toán từ trang đầu cho đến khi trang tiếp theo được load và cả vị trí của các nút cần làm giả sao cho khớp với các nút muốn lợi dụng.

```html
<style>
	iframe {
		position:relative;
		width:1265px;
		height: 597px;
		opacity: 0.1;
		z-index: 2;
	}
   .firstClick, .secondClick {
		position:absolute;
		top:520px;
		left:63px;
		z-index: 1;
	}
   .secondClick {
		top:317px;
		left:230px;
	}
</style>
<div class="firstClick">Test me first</div>
<div class="secondClick">Test me next</div>
<iframe src="https://0a4700d803398828806a45760014001e.web-security-academy.net/my-account"></iframe>
```

## Note

Height và width dùng để xác định vùng iframe hiển thị, top là khoảng cách từ cạnh trên cùng đến vị trí của cạnh trên cùng của khối “Clickjacking”, left là khoảng cách từ lề trái đến cạnh trái của khối đó.

Giá trị opacity ban đầu nên để 0.5 để nhìn rõ, xem thử vị trí đặt ô clickjacking đã chính xác hay chưa rồi mới chuyển về 0.0001.

Cách phòng chống: Sử dụng 1 trong hai thuộc tính có trong HTTP request là: X-Frame-Options và Content-Security-Policy (CSP), với CSP sẽ sử dụng chính sách frame-ancestors, nếu trình duyệt cũ không hỗ trợ thì sử dụng X-Frame-Options.
