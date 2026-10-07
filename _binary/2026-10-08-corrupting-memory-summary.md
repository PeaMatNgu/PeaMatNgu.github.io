---
title: "Corrupting Memory — Summary"
date: 2026-10-08
summary: "Theory notes on memory corruption, stack smashing, stack canaries, and ASLR."
platform: "pwn.college"
type: "summary"
tags:
  - binary-exploitation
  - memory-corruption
  - stack-canary
  - aslr
---

> **Summary notes.** This article contains the theory notes for this topic. The companion practice article contains the hands-on exercises.

[Practice article](/binary-exploitation/2026-10-08-corrupting-memory-practice/)

## Memory Errors: High-Level Problems

## Memory Errors: Smashing The Stack

## Memory Errors: Cause Of Corruption

## Memory Errors: Stack Canaries

### Stack Canary Definition

Canary trong stack canary là một giá trị bí mật/ngẫu nhiên được đặt trên stack, thường nằm giữa các biến cục bộ như buffer và dữ liệu điều khiển quan trọng như saved RBP / return address.

Nó dùng để phát hiện stack buffer overflow. Ý tưởng là: nếu bạn ghi tràn buffer để cố ghi đè return address, gần như chắc chắn bạn phải ghi đè qua canary trước. Trước khi hàm return, chương trình sẽ kiểm tra canary có còn đúng giá trị ban đầu không. Nếu bị thay đổi, chương trình coi như stack đã bị phá và thường gọi “__stack_chk_fail()” rồi dừng.

![Corrupting Memory — Summary figure 1](/assets/images/binary/corrupting-memory-summary/figure-01.png)

FS → dùng để truy cập TLS<br>FS:0x28 → thường chứa stack canary gốc<br>RAX → thường chỉ được dùng tạm để copy/so sánh canary

Mẹo khi debug mà thấy xuất hiện “fs:0x28” thì khả năng cao có cơ chế stack canary protection ở đây.

Ngoài ra có thể sử dụng câu lệnh “checksec --file=<binary>” để kiểm tra các cơ chế bảo vệ bảo mật được bật trên một file thực thi ELF.

### Exploiting Stack Canaries

Làm lộ ra giá trị canary bằng một lỗ hổng khác, tuy nhiên cách này không khả quan và khá phức tạp

Sử dụng brute-force:

Thông thường canary thường có kích thước 8 bytes, nhưng byte thấp nhất của nó thường là “0x00”, nên thực tế chỉ có 7 bytes cần phải đoán. Nếu như đoán đúng được byte thứ nhất chương trình không crash ngay tại điểm canary đó Chuyển sang byte kế tiếp (Mỗi byte có 2^64 khả năng xảy ra).

Tuy nhiên cách này chỉ khả thi nếu như server dùng mô hình process cha “fork()” tạo ra các process child. Process child kế thừa cùng giá trị stack canary, hiểu đơn giản là nếu brute-force thử child1 bị crash thì tiếp tục thử sang child2,…

Điều quan trọng ở đây là việc crash child1 không làm ảnh hưởng đến process cha, nhưng nếu mô hình làm logic kiểu mỗi lần crash reset và sinh canary mới thì không thể dùng cách này.

### Useful GDB Commands

Đặt “break main” “disp/4i $rip”: Hiển thị 4 instructions bắt đầu tại địa chỉ rip đang trỏ tới mỗi khi chương trình dừng.

“ni”: Thực thi instruction hiện tại rồi chuyển sang instruction kế tiếp tự động in ra 4 instructions tiếp theo.

Cứ tiếp tục cho đến đoạn thanh ghi chứa giá trị của stack canary đọc giá trị hiện tại đang lưu trên thanh ghi [rbp-8] “x/gx $rbp-8” (Xem 8 byte dạng big-endian tại địa chỉ rbp-8) “x/bx $rbp-8” (Xem dạng little-endian, lấy được giá trị canary).

## Memory Errors – Aslr

### ASLR Definition

Là viết tắt của Address Space Layout Randomization, đây là cơ chế làm ngẫu nhiên địa chỉ bộ nhớ của các vùng quan trọng mỗi lần chương trình chạy. Ý tưởng này được tạo ra để khiến attacker không dễ dàng biết chính xác địa chỉ để nhảy tới.

### Exploiting ASLR

#### Method 1: Address Leak

Đây là cách phổ biến nhất. ASLR chỉ làm địa chỉ ngẫu nhiên, chứ chương trình vẫn phải biết địa chỉ thật của các object/hàm đang được sử dụng.

Địa chỉ thật vẫn tồn tại trong bộ nhớ, cho nên chương trình có thể tìm ra được chúng ví dụ như Flow sau:

Thông thường bạn sẽ cần ghi n byte buffer sau đó ghi địa chỉ muốn nhảy đến thay vào địa chỉ của ret. ASLR có thể làm cả stack dịch đi, tuy nhiên khoảng cách giữa buffer và ret là không đổi.

Vậy vấn đề chính ở đây là gì, đó là ASLR đã làm thay đổi địa chỉ bạn muốn ghi vào ret, giả sử mục tiêu là ghi đè địa chỉ của hàm win(), nhưng thư viện “libc” đã bị thay đổi sau mỗi lần địa chỉ của win() cũng bị thay đổi theo.

Giả sử trong chương trình làm lộ địa chỉ “puts = …”, bạn biết được “win offset” thì tính được “libc base = puts runtime – puts offset) “win runtime = libc base + win offset”. Tìm được địa chỉ cần ghi đè ở lần chạy này.

#### Method 2: Partial Overwrite

ASLR không “giữ nguyên 3 số hex cuối của mọi địa chỉ” một cách tùy ý. Lý do là Linux ánh xạ bộ nhớ theo page. Vì vậy địa chỉ bắt đầu của một vùng được map phải chia hết cho 0x1000, nên base luôn có 12-bit cuối bằng 0.

Giờ giả sử hàm win nằm offset 0x8ab tính từ đầu page/module: win = base + 0x8ab.

Ta sẽ có 12-bit thấp luôn giống nhau = 8ab, nhưng buffer overflow thường được ghi theo byte, vì vậy ta cần ghi đè 16-bit tương đương với 2 bytes thấp.

Nhưng bình thường ta chỉ biết được ?8ab, vì vậy cần đoán cái “?”, còn ret hiện tại đã chứa địa chỉ runtime hợp lệ, tức phần cao đã đúng chỉ cần 2-bytes thấp kia đúng là bypass thành công.

Tuy nhiên cách này cũng khá khó vì nếu đoán sai thì chtrinh crash, ASLR có thể chọn base mới Thử lại từ đầu, thay vì tìm giá trị đúng cứ thử 1 giá trị đến lần chạy nào đúng thì thôi.

#### Method 3: Brute Force (Situational)

Method này được sử dụng khi không leak được địa chỉ, thử được nhiều địa chỉ khả dĩ do có cơ chế “fork()” hoặc dựa vào ASLR/layout giữ nguyên giữa các lần thử.

### Useful Commands

“objdump -M intel -d ten_file”: Chuyển machine code trong binary thành assembly để dễ đọc cả file hơn.

Disable ASLR for local testing:

“p = process("./vulnerable_program", aslr=False)”

Với gdb thì sử dụng “show disable-randomization”

Nếu binary có bit SUID thì nên tạo một bản copy hoặc bỏ SUID trước khi debug bằng GDB.

“setarch x86_64 -R /bin/bash”: Nó mở một shell mới với ASLR bị tắt

Tắt ASLR không có nghĩa là tắt mọi protection. Canary, NX, RELRO vẫn có thể còn nguyên. Nó chỉ làm việc random hóa địa chỉ biến mất hoặc giảm đi.
