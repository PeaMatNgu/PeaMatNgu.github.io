---
title: "Using Shellcode — Practice"
date: 2026-10-08
summary: "Hands-on exercises for redirecting execution to mapped and injected shellcode."
platform: "pwn.college"
type: "practice"
tags:
  - binary-exploitation
  - shellcode
  - control-hijacking
  - practice
---

> **Practice notes.** This article contains the hands-on exercises for this topic. Read the companion summary first if you need the underlying theory.

[Summary article](/binary-exploitation/2026-10-08-using-shellcode-summary/)

## Exercise 1 — Hijack to (Mapped) Shellcode (Easy)

Source code cần nghiên cứu challenge

![Using Shellcode — Practice figure 1](/assets/images/binary/using-shellcode-practice/figure-01.png)

Dựa trên gợi ý của bài thì shellcode được lưu tại vùng nhớ “0x24174000”, vì đây là vùng nhớ có quyền read, write, execute Mục tiêu là tạo 1 file shellcode với nội dung đọc file “/flag” và nạp nội dung đó vào RAM tại “0x24174000”.

![Using Shellcode — Practice figure 2](/assets/images/binary/using-shellcode-practice/figure-02.png)

Phần thứ hai của thử thách sẽ là tính toán số bytes buffer để ghi đè địa chỉ ret về địa chỉ chứa shellcode của ta, cụ thể là “0x24174000”.

![Using Shellcode — Practice figure 3](/assets/images/binary/using-shellcode-practice/figure-03.png)

Ta tính được số bytes truyền vào trước khi đến địa chỉ ret là 56 bytes, sau đó là “p64(0x24174000)”, có nghĩa là chuyển địa chỉ thành 8 bytes theo little-endian.

Toàn bộ nội dung (byte machine code) của file “/tmp/shellcode-raw” và lưu vào biến shellcode Gửi shellcode vào stdin của challenge, chờ challenge in tới dòng “Press enter to continue!” “p.sendline()” tương đương với nhấn enter Truyền vào phần dữ liệu để ghi đè địa chỉ ret. Cuối cùng là “p.interactive()” để chuyển terminal sang chế độ tương tác với tiến trình, hiểu đơn giản là nếu shellcode có nội dung tạo 1 shell mới thì ta có thể tương tác.

![Using Shellcode — Practice figure 4](/assets/images/binary/using-shellcode-practice/figure-04.png)

## Exercise 2 — Hijack to (Mapped) Shellcode (Hard)

Bài này không có mã nguồn file “.c” vì vậy ta cần debug hàm challenge để biết số byte cần ghi trong buffer là “0x08+0x30=56 bytes”, nhiệm vụ tiếp theo là viết file “shellcode.s” để tạo thành file sạch “shellcode-raw” và tìm địa chỉ lưu trữ shellcode để truyền nội dung của file này vào đây.

![Using Shellcode — Practice figure 5](/assets/images/binary/using-shellcode-practice/figure-05.png)

Nội dung của file “shellcode.s” vẫn tương tự như những lần trước, chức năng chính là đọc file “/flag” và gửi kết quả ra cho user.

![Using Shellcode — Practice figure 6](/assets/images/binary/using-shellcode-practice/figure-06.png)

Hàm “mmap()” khả năng cao là nơi dùng để lưu nội dung shellcode vì nó nạp địa chỉ vùng nhớ dự kiến “0x178d0000” và kích thước “0x1000 bytes”, sau “call mmap@plt” thì rax = địa chỉ vùng nhớ vừa được mmap. Vì vậy ở đây ta đặt breakpoint và quan sát xem tại lệnh đó thì giá trị trên thanh ghi rax là gì.

![Using Shellcode — Practice figure 7](/assets/images/binary/using-shellcode-practice/figure-07.png)

Mục tiêu tiếp theo là tìm địa chỉ trả về, cụ thể là địa chỉ mà lưu trữ shellcode với các quyền write, read và execute. Để thực hiện trước hết là sử dụng gdb để debug “start” để chạy nhưng dừng lại tại main, đặt breakpoint tại địa chỉ lệnh ngay sau “mmap” “continue để chương trình tiếp tục” “p/x $rax” để xem giá trị trên thanh ghi rax hiện tại

![Using Shellcode — Practice figure 8](/assets/images/binary/using-shellcode-practice/figure-08.png)

Sau cùng ghi nội dung file exploit, vì đã biết được mã nguồn từ bài lần trước nên ta viết tương tự chỉ thay địa chỉ ret là được.

![Using Shellcode — Practice figure 9](/assets/images/binary/using-shellcode-practice/figure-09.png)

Flag nhận được cũng như vẫn có thể tương tác tiếp tục do đã mở kết nối

![Using Shellcode — Practice figure 10](/assets/images/binary/using-shellcode-practice/figure-10.png)

## Exercise 3 — Hijack to Shellcode (Easy)

Đây là 1 challenge kết hợp giữa buffer overflow+ shellcode+ ghi đè địa chỉ ret, mục tiêu cuối cùng là làm CPU nhảy tới shellcode do ta đặt trên stack.

Hãy nhìn qua lỗi được tạo ra trong mã nguồn, đầu tiên là buffer overflow:

![Using Shellcode — Practice figure 11](/assets/images/binary/using-shellcode-practice/figure-11.png)

![Using Shellcode — Practice figure 12](/assets/images/binary/using-shellcode-practice/figure-12.png)

Thông thường shellcode không thể chạy trên stack, tuy nhiên bài này tác giả đã tắt cơ chế bảo vệ đó cho ta cũng như tắt “stack canary”, “ASLR” nên khi ghi tràn qua buffer và saved RBP thì chương trình cũng không bị crash.

Có thể thấy trong mã nguồn, chỉ có duy nhất một lần đọc input, vì vậy payload lần này sẽ phải bao gồm: nội dung shellcode-raw + padding + địa chỉ ret.

Khi truyền thử 1 payload chỉ gồm byte padding, ta có thể xác định được cần 56 bytes cho phần buffer và địa chỉ bắt đầu của buffer. Ngoài ra cũng xác định được địa chỉ RET cần 8 bytes.

![Using Shellcode — Practice figure 13](/assets/images/binary/using-shellcode-practice/figure-13.png)

Flow của payload sẽ như hình dưới đây, ta sẽ lưu nội dung đọc từ file “shellcode-raw” vào biến shellcode. Khai báo địa chỉ bắt đầu buffer và truyền 56 bytes ngẫu nhiên vào, tiếp đến là 8 bytes của địa chỉ ret, lúc này trỏ đến địa chỉ của shellcode và cuối cùng là phần nội dung mà đã đọc từ “shellcode-raw”.

![Using Shellcode — Practice figure 14](/assets/images/binary/using-shellcode-practice/figure-14.png)

Bài này cần chèn shellcode ở phía sau thay vì cho luôn vào phần 56 bytes ngẫu nhiên là vì kích thước của shellcode tôi viết là 72 bytes.

![Using Shellcode — Practice figure 15](/assets/images/binary/using-shellcode-practice/figure-15.png)

![Using Shellcode — Practice figure 16](/assets/images/binary/using-shellcode-practice/figure-16.png)

## Exercise 4 — Hijack to Shellcode (Easy)

Kích thước của phần padding sẽ là 88 bytes, và ta cũng cần phải tính được địa chỉ bắt đầu buffer cụ thể là [rbp-0x50].

![Using Shellcode — Practice figure 17](/assets/images/binary/using-shellcode-practice/figure-17.png)

Ta sẽ sử dụng gdb, sử dụng lệnh “start” để bắt đầu và dừng lại ở hàm main, ta sẽ đặt breakpoint sau phần tạo stack frame “break *challenge+8” “continue” tại thời điểm này đã chạy qua đoạn nạp giá trị của “rbp”, ta sẽ xem giá trị của thanh ghi này “info registers rbp” Sau đó tính địa chỉ buffer “p/x $rbp – 0x50” và lấy được kết quả là “0x7fffffffd970”.

![Using Shellcode — Practice figure 18](/assets/images/binary/using-shellcode-practice/figure-18.png)

Sau đó ta viết script python tương tự như ở bài easy, chỉ cần chỉnh sửa địa chỉ cũng như kích thước bytes cần ghi vào là xong.

![Using Shellcode — Practice figure 19](/assets/images/binary/using-shellcode-practice/figure-19.png)

![Using Shellcode — Practice figure 20](/assets/images/binary/using-shellcode-practice/figure-20.png)

![Using Shellcode — Practice figure 21](/assets/images/binary/using-shellcode-practice/figure-21.png)
