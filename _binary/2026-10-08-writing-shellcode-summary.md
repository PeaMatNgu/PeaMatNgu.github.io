---
title: "Writing Shellcode — Summary"
date: 2026-10-08
summary: "Theory notes on writing, building, debugging, and adapting shellcode under common constraints."
platform: "pwn.college"
type: "summary"
tags:
  - binary-exploitation
  - shellcode
  - assembly
  - syscalls
---

> **Summary notes.** This article contains the theory notes for this topic. The companion practice article contains the hands-on exercises.

[Practice article](/binary-exploitation/2026-10-08-writing-shellcode-practice/)

## Definition and Overview

Shellcode là một đoạn mã máy nhỏ được thiết kế để thực thi trực tiếp trong bộ nhớ của tiến trình, thường sau khi khai thác lỗi bảo mật.

Shellcode có thể mở command shell, tạo reverse shell kết nối về máy của người kiểm thử, đọc hoặc ghi dữ liệu, gọi một hàm có sẵn trong chương trình, thực hiện các thao tác khác trong tiến trình.

### Shellcode Injection Example

![Writing Shellcode — Summary figure 1](/assets/images/binary/writing-shellcode-summary/figure-01.png)

Nhìn qua thì có thể đây là hai hàm rất bình thường, sẽ in ra hello cùng tên người dùng sau đó random chạy 1 trong 2 lời chào tạm biệt “Farewell” hoặc “Goodbye”.

Hàm hello() nhận hai tham số đầu vào là “*name”, bản chất đây là một “pointer” (con trỏ) hướng đến chuỗi kí tự, “*(bye_func)()” là một “function pointer”, nó chỉ trỏ đến địa chỉ của một hàm ( hàm đó không có tham số đầu vào, và không có kiểu giá trị trả về).

Trường hợp truyền đúng, khi địa chỉ buffer name được truyền cùng với địa chỉ của hàm bye2, còn trường hợp truyền sai “hello(bye1,name)”, tham số thứ nhất lúc này lại nhận địa chỉ của hàm bye1, tham số thứ hai lại nhận địa chỉ buffer name.

Flow hoạt động lúc này sẽ là “bye_func()” lúc này đang chứa địa chỉ của buffer name, tức là nó coi đây là địa chỉ của 1 hàm nhảy tới địa chỉ này Thực thi các byte đang nằm trong buffer, vậy nếu input được truyền vào “name” là shellcode CPU sẽ bắt đầu thực thi Shellcode đó

Trong hình vẽ bên cạnh ta có thể thấy, “.text” là nơi chứa mã máy của chương trình, địa chỉ của các hàm. “stack” chứa dữ liệu của các hàm đang chạy, đó là lí do tại sao lại có dấu mũi tên, đáng nhẽ ra “bye_func()” phải trỏ đến “.text”, trường hợp lỗi lại trỏ đến “stack”.

Mục tiêu cuối cùng của khai thác là triển khai được 1 shell. Ví dụ như: execve(“/bin/sh”, NULL, NULL).

![Writing Shellcode — Summary figure 2](/assets/images/binary/writing-shellcode-summary/figure-02.png)

“mov rax, 59”: Nạp lệnh “execve” cho “systemcall”

“lea rdi, [rip+binsh]: Đặt địa chỉ của “/bin/sh” vào rdi, rdi tham số thứ nhất của execve

“mov rsi,0”: Đặt tham số thứ 2 bằng 0, tương ứng với “argv”

“mov rdx,0”: Đặt tham số thứ 3 bằng 0, tương ứng với “envp”

“syscall”: Gọi execve(“/bin/sh”, NULL, NULL)

“binsh: .string “/bin/sh””: Nhãn đánh dấu vị trí chuỗi, “.string” sẽ thêm 1 byte “null terminator \x00” vào cuối chuỗi.

### Non-Shell Shellcode

![Writing Shellcode — Summary figure 3](/assets/images/binary/writing-shellcode-summary/figure-03.png)

Dòng đầu tiên là đặt chuỗi “/flag\0” trên stack

Dòng thứ hai, đưa chuỗi “/flag” lên đỉnh của stack

Dòng 3, nạp systemcall open, 2 = open(pathname, flags)

Dòng 4, đặt tham số thứ nhất = rsp, tương ứng với địa chỉ là “/flag\0”

Dòng 5, đặt tham số thứ 2 = 0, tương ứng là chế độ only read

Dòng 6, gọi systemcall, lưu “file descriptor” vào rax

Dòng 7, rdi =1, nghĩa là gửi nội dung file ra màn hình (stdout)

Dòng 8, nạp rsi = rax, vì sendFile cần file descriptor ở tham số thứ 2 (rsi)

Dòng 9, nạp tham số thứ 3 = 0, con trỏ tới offset đầu tiên trong file

Dòng 10, tham số tứ tư =1000, nghĩa là gửi tối đa 1000 bytes

Dòng 11, nạp systemcall sendFile (40) cho rax

Dòng 12, gọi sendFile tương ứng sendFile(1, fd, 0, 1000)

Dòng 13, nạp rax = 60, kết thúc, exit (60)

Dòng 14, gọi systemcall

## Building Shellcode

### Building with GCC

![Writing Shellcode — Summary figure 4](/assets/images/binary/writing-shellcode-summary/figure-04.png)

“.global _start”: Khai báo _start là symbol toàn cục và là điểm bắt đầu của chương trình

“_start:”: Đây là label đánh dấu vị trí instruction đầu tiên của shellcode, khi CPU bắt đầu thực thi file ELF, nó sẽ bắt đầu từ địa chỉ “_start”

“.intel_syntax noprefix”: Yêu cầu assembler sử dụng cú pháp Intel

Đoạn ở dưới giống ở trên, là shellcode để gọi execve(“/bin/sh”, NULL, NULL)

Đặt chuỗi /bin/sh ngay sau phần instruction, binsh chỉ là label để instruction “lea rdi, [rip+binsh]” tìm được địa chỉ của chuỗi.

“gcc -nostdlib -static shellcode.s -o shellcode-elf”: Lệnh này tạo file ELF tên là shellcode-elf đây là 1 chương trình ELF hoàn chỉnh, có header, section table, entry point và section “.text”.

Trong exploit, ta thường cần đưa trực tiếp các byte instruction vào buffer, ta chỉ cần phần “.text”, nơi chứa mã máy của shellcode:

[padding][shellcode bytes][địa chỉ nhảy tới shellcode]

“objcopy --dump-section .text=shellcode-raw shellcode-elf”: “.text” là tên section cần lấy, “shellcode-elf” tên file input, “shellcode-raw” là file đầu ra chứa các byte thô.

### Building with C

Flow: cấp phát vùng nhớ thực thi đọc shellcode vào vùng nhớ đó nhảy tới vùng nhớ Thực thi shellcode.

![Writing Shellcode — Summary figure 5](/assets/images/binary/writing-shellcode-summary/figure-05.png)

## Debugging with strace

strace là công cụ theo dõi các system call mà một chương trình gọi tới kernel. Vì shellcode chủ yếu hoạt động bằng system call, strace rất hữu ích để kiểm tra shellcode có đi đúng hướng hay không.

![Writing Shellcode — Summary figure 6](/assets/images/binary/writing-shellcode-summary/figure-06.png)

Mỗi dòng strace thường có dạng “system_call(arguments) = return_values”, sẽ có cái nhìn tổng quan xem lệnh systemcall này với các tham số đó thì kết quả đã đúng chưa, nếu chưa đúng thì sẽ biết lỗi từ phần nào để tìm ra lỗi.

## Debugging with GDB

![Writing Shellcode — Summary figure 7](/assets/images/binary/writing-shellcode-summary/figure-07.png)

Shellcode thường không có source code C, nên chủ yếu quan sát instruction, thanh ghi và bộ nhớ.

“x/5i $rip”: Xem 5 instruction tiếp theo, “$rip” là địa chỉ instruction hiện tại

Xem dữ liệu trên stack, “$rsp” là stack pointer, chứa địa chỉ vùng stack hiện tại

x/gx $rsp # 8 byte<br>x/2dx $rsp # 2 dword<br>x/4hx $rsp # 4 halfword<br>x/8b $rsp # 8 byte

“si”: Thực thi từng instruction, nhưng đi vào bên trong “call”, “ni” thì không.

“break *0x400000”: Đặt breakpoint tại địa chỉ cụ thể, “int3” có thể giúp để chèn breakpoint trực tiếp vào shellcode.

## Common Challenges in Shellcoding

### Memory Access Width

![Writing Shellcode — Summary figure 8](/assets/images/binary/writing-shellcode-summary/figure-08.png)

Ghi sai kích thước có thể ghi đè các byte lân cận, làm hỏng shellcode, địa chỉ, chuỗi hoặc dữ liệu khác.

### Forbidden Bytes

![Writing Shellcode — Summary figure 9](/assets/images/binary/writing-shellcode-summary/figure-09.png)

Những byte có thể làm payload hoặc shellcode bị cắt, biến đổi hoặc hiểu sai tùy theo cách chương trình nhận input.

Đây không phải các byte CPU cấm thực thi; chúng bị “cấm” bởi hàm nhập dữ liệu hoặc giao thức truyền.

Trên hình là một số byte cấm tương ứng với các hàm, vì vậy khi viết shellcode cần phải kiểm tra xem các byte trong payload có phù hợp với phương thức input hay không.

Hai đoạn assembly có thể cho cùng kết quả nhưng tạo ra chuỗi machine code khác nhau, vì vậy nên chọn cách mã hóa tốt hơn để loại bỏ byte “0x00”.

![Writing Shellcode — Summary figure 10](/assets/images/binary/writing-shellcode-summary/figure-10.png)

Nếu một byte như “0xcc” bị cấm, không ghi trực tiếp byte đó vào shellcode. Có thể tạo byte bị cấm trong lúc chương trình đang chạy bằng self-modifying code.

[rip] trỏ đến byte kế tiếp, tức 0xcb. Inc tăng “0xcb” lên 1 = “0xcc” là mã lệnh của “int3”

Vì mã lệnh cũng chỉ là dữ liệu dạng byte nên chương trình có thể sửa byte trong vùng “.text”, nhưng để “.text” có quyền ghi, cần phải có tùy chọn “-wl, -N”.

![Writing Shellcode — Summary figure 11](/assets/images/binary/writing-shellcode-summary/figure-11.png)
