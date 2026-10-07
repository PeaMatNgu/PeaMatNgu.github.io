---
title: "Space Explorer Write-Up"
date: 2026-10-08
summary: "A lost space mission control system suffers from flawed authentication logic between its Sender and Receiver services."
difficulty: "Very Easy"
platform: "Hack The Box"
tags:
  - web
  - go
  - python
  - json
---

## Challenge information

| Field | Details |
| --- | --- |
| Category | Web |
| Rating | Very Easy |
| Flag | `HTB{C0SM1C-BYP4SS}` |
| Description | A lost space mission control system suffers from flawed authentication logic between its Sender and Receiver services. |

Thử thách Web này có vấn đề ở cách xử lý giữa hai dịch vụ Sender(Go) và Receiver(Python). Trong mã nguồn ta có thể thấy `Go` sử dụng encoding/json để `Unmarshal Json` để chuyển đổi dữ liệu từ dạng json thành cấu trúc dữ liệu trong ngôn ngữ lập trình. `Go` đọc từng cặp key-value trong json, so sánh với tên các trường có trong **RequestData**, ở đây chỉ có 1 trường là `Action string`.

Tuy `Go` có cơ chế validate dữ liệu, nhưng nó sẽ lấy giá trị cuối cùng được truyền vào, cũng như không phân biệt giá trị viết hoa hay thường. Nếu như giá trị cuối cùng hợp lệ, được duyệt thì sẽ gửi nguyên toàn bộ dữ liệu thô của request sang cho receiver xử lý.

Phía Sender không phân biệt ký tự hoa thường, Python thì có, nó phân biệt các key này cộng thêm việc không có cơ chế validate ở backend. Vì vậy, ý tưởng của bài này sẽ là truyền thêm 1 trường `"Action": "getcosmic"` trong request, trước đó là `"action": "GetSecureCode"`, request này vượt qua cơ chế kiểm tra của `Go` và sẽ trả về flag trong Response.

<img src="https://hackmd.io/_uploads/BkdZ70tUGg.png" alt="Space Explorer exploit response">

Flag: `HTB{C0SM1C-BYP4SS}`
