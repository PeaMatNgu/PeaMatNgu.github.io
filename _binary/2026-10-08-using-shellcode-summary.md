---
title: "Using Shellcode — Summary"
date: 2026-10-08
summary: "A concise overview of the exploitation flow and where shellcode fits into a compromise."
platform: "pwn.college"
type: "summary"
tags:
  - binary-exploitation
  - shellcode
  - exploitation-flow
---

> **Summary notes.** This article contains the theory notes for this topic. The companion practice article contains the hands-on exercises.

[Practice article](/binary-exploitation/2026-10-08-using-shellcode-practice/)

## Exploitation Flow

Shellcode is one part of a larger exploitation process. The following flow helps place a payload in context—from understanding the target to gaining enough control to complete the challenge.

<figure class="flow-figure">
  <img src="/assets/images/binary/using-shellcode-summary/figure-01.png" alt="Six stages of the exploitation flow">
  <figcaption>Six stages of a typical exploitation workflow.</figcaption>
</figure>

### 1. External Reconnaissance

Quan sát chương trình và cách nó xử lý dữ liệu. Mục tiêu của bước này là hiểu chương trình hoạt động ra sao và xác định những chức năng có khả năng chứa lỗ hổng.

### 2. Gaining a Foothold

Tìm một điểm yếu có thể khai thác để tạo quyền kiểm soát ban đầu. Đây có thể là lỗi memory corruption, input validation hoặc một vị trí cho phép chuyển hướng luồng thực thi.

### 3. Internal Reconnaissance

Sau khi có foothold, kiểm tra xem lỗ hổng đã thay đổi trạng thái chương trình như thế nào: thanh ghi nào kiểm soát được, vùng nhớ nào có thể đọc hoặc ghi, và còn cơ chế bảo vệ nào đang hoạt động.

### 4. Gaining Influence

Tận dụng quyền kiểm soát ban đầu để mở rộng ảnh hưởng. Trong giai đoạn này, shellcode có thể được đặt vào vùng nhớ thực thi và luồng điều khiển được chuyển tới payload đó.

### 5. Total Compromise

Lặp lại quá trình quan sát và mở rộng quyền kiểm soát cho đến khi đạt được mục tiêu cuối cùng, chẳng hạn đọc file flag, tạo shell hoặc thực thi một hành động tùy ý.

### 6. Gloating

Xác nhận kết quả khai thác, lấy flag và lưu lại payload cùng các bước thực hiện để có thể tái hiện lời giải.

## Where Shellcode Fits

Shellcode thường xuất hiện ở giai đoạn **Gaining Influence**: một lỗ hổng đã cho phép kiểm soát bộ nhớ hoặc instruction pointer, còn shellcode cung cấp chuỗi lệnh mà CPU sẽ thực thi. Tùy challenge, payload có thể mở shell, đọc trực tiếp `/flag`, hoặc gọi các system call cần thiết mà không cần tạo shell tương tác.
