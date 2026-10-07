---
title: "Writing Shellcode — Practice"
date: 2026-10-08
summary: "Hands-on exercises for basic shellcode, NOP sleds, and NULL-free payloads."
platform: "pwn.college"
type: "practice"
tags:
  - binary-exploitation
  - shellcode
  - assembly
  - practice
---

> **Practice notes.** This article contains the hands-on exercises for this topic. Read the companion summary first if you need the underlying theory.

[Summary article](/binary-exploitation/2026-10-08-writing-shellcode-summary/)

## Exercise 1 — Basic Shellcode

Đây là bài đầu tiên và viết Shellcode, như trong video đã được học, thông thường sẽ có 2 nhiệm vụ chính mà challenge trên pwn.college yêu cầu bạn làm. Một có thể là kích hoạt execve(“/bin/sh”,0,0”) để có thể tạo ra 1 shell. Mình có viết thử vào đường dẫn của folder challenge, nhưng vấn đề là folder này không cho quyền write vì vậy mình lưu vào đường dẫn “/tmp/shellcode.s”.

![Writing Shellcode — Practice figure 1](/assets/images/binary/writing-shellcode-practice/figure-01.png)

Sau khi assemble thành 1 file “.elf” và cắt bỏ đi những phần dữ liệu dư thừa bằng “objcopy –dump” thì chạy thành công và mình tạo được 1 shell.

![Writing Shellcode — Practice figure 2](/assets/images/binary/writing-shellcode-practice/figure-02.png)

Chạy bằng “cat /tmp/shellcode-raw - | /challenge/binary-exploitation-basic-shellcode”, tuy nhiên sau khi kiểm tra thì mình thấy với shell này mình vẫn không thể đọc được file flag vì nó chỉ có duy nhất quyền read cho user tạo ra (cụ thể là root)

![Writing Shellcode — Practice figure 3](/assets/images/binary/writing-shellcode-practice/figure-03.png)

Vì vậy, lúc này mình nghĩ đến flow viết hai hàm systemcall trong cùng 1 file, hàm systemcall đầu tiên có vai trò mở file flag và lưu giá file descriptor làm tham số đầu vào cho hàm sendFile() đằng sau

Hàm sendFile() này sẽ có mục tiêu là lấy nội dung từ file flag và trả về màn hình cho mình.

![Writing Shellcode — Practice figure 4](/assets/images/binary/writing-shellcode-practice/figure-04.png)

![Writing Shellcode — Practice figure 5](/assets/images/binary/writing-shellcode-practice/figure-05.png)

## Exercise 2 — NOP Sleds

![Writing Shellcode — Practice figure 6](/assets/images/binary/writing-shellcode-practice/figure-06.png)

Bài này có một cơ chế là sẽ bỏ qua ngẫu nhiên từ 0x100 đến 0x7ff byte đầu tiên, sau khi tìm hiểu mình biết đến cách xử lý sẽ là thêm NOP Sleds vào đầu chương trình

Nói dễ hiểu thì NOP là một chuỗi lệnh máy tính mà không làm gì cả, cụ thể khi chương trình nhảy vào bất kỳ địa chỉ nào nằm trong vùng “NOP Sled” thì sẽ trượt tiếp cho đến khi tới phần Shellcode thực sự.

.rept 2048<br>nop<br>.endr

Khi thêm phần này vào file shellcode.s thì sẽ chèn 2048 bytes nop ở đằng trước phần shellcode thực sự, cơ chế random skip bytes của chương trình chỉ có range từ 256 đến 2047 bytes đầu tiên.

Assemble file .elf rồi loại bỏ phần dữ liệu thừa bằng “object --dump”, sau khi chạy xong “cat /tmp/shellcode-raw - | /challenge/binary-exploitation-basic-shellcode” sẽ lấy được flag ở ngay phía dưới.

![Writing Shellcode — Practice figure 7](/assets/images/binary/writing-shellcode-practice/figure-07.png)

## Exercise 3 — NULL-Free Shellcode

Bài này là bài cuối cùng trong phần bài tập này, thử thách lần này không còn nằm ở việc xử lý các bytes bị skip mà nó muốn người học viết shellcode mà không được có byte “\0x00”.

![Writing Shellcode — Practice figure 8](/assets/images/binary/writing-shellcode-practice/figure-08.png)

Như trong bài học ta đã được học “mov rbx, 0x67616c662f” là lệnh tạo chuỗi “/flag”, tuy nhiên lệnh này dính 3 byte cuối là “00”, vì vậy ta xây dựng giá trị theo:

```asm
mov ebx, 0x67616c66
shl rbx, 8
mov bl, 0x2f
```

Các lệnh nạp tham số 2 và tham số 3 bằng 0, thì ta chỉ cần sử dụng lệnh xor để thay thế, có thể xem sự thay thế giữa 2 cột để thấy sự khác biệt.

![Writing Shellcode — Practice figure 9](/assets/images/binary/writing-shellcode-practice/figure-09.png)

![Writing Shellcode — Practice figure 10](/assets/images/binary/writing-shellcode-practice/figure-10.png)
