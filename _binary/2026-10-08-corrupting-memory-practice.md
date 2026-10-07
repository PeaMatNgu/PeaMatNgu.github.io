---
title: "Corrupting Memory — Practice"
date: 2026-10-08
summary: "Hands-on memory-corruption exercises covering overflows, variable control, control hijacking, PIE, and string lengths."
platform: "pwn.college"
type: "practice"
tags:
  - binary-exploitation
  - memory-corruption
  - pwn-college
  - practice
---

> **Practice notes.** This article contains the hands-on exercises for this topic. Read the companion summary first if you need the underlying theory.

[Summary article](/binary-exploitation/2026-10-08-corrupting-memory-summary/)

## Exercise 1 — Your first Overflow (Hard)

```c
int challenge(int argc, char **argv, char **envp)
{
struct
{
char input[68];
int win_variable;
} data = {0} ;
unsigned long size = 0;
size = 4096;
printf("Send your payload (up to %lu bytes)!\n", size);
int received = read(0, &data.input, (unsigned long) size);
if (received < 0)
{
printf("ERROR: Failed to read input -- %s!\n", strerror(errno));
exit(1);
}
if (data.win_variable)
{
win();
}
puts("Goodbye!");
```

Khai báo mảng input chỉ có 68 byte, nhưng chương trình lại cho phép đọc tối đa 4096 byte (unsigned long) vào input. Vì vậy khi truyền vào 68 byte ký tự bất kì và thêm 4 byte khác 0 thì lúc này, nó sẽ ghi đè lên giá trị “win_variable”, trả flag.

Read(file_descriptor, buffer, số_byte_max): “số_byte_max” đáng ra phải được khai báo bằng kích thước của “data.input”.

File_descriptor: “0 stdin”, “1 stdout”, “2 stderr”. Buffer là nội dung sẽ được ghi vào input.

Payload: Truyền 68 byte “A” và 4 byte tượng trưng cho “1” làm đầu vào cho chương trình challenge.

```python
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*68 + b"\x01\x00\x00\x00")' \
| /challenge/binary-exploitation-first-overflow
```

## Exercise 2 — Precision (Easy)

Với bài này về lỗi tràn bộ đệm vẫn giống như bài trên, nhưng khác ở chỗ có cài thêm 2 biến là “win_variable” và “lose_variable”, hiểu đơn giản là nếu như ghi đè đủ biến “win_variable” thì sẽ trả về flag còn nếu ghi đè quá ra cả biến “lose_variable” thì sẽ thua.

Nhưng bài này khá dễ vì khi truyền các byte vào thì sẽ có 1 bảng hiện ra các byte đã truyền vào cũng như khoảng cách từ byte win đến byte lose (cụ thể ở bài này là 4 byte), sau 1 vài lần thử mình phát hiện ra từ ngoài 18-byte đầu của input thì có 2-byte là phần padding. Vì vậy, khi ghi đè từ byte 21 đến 24 sẽ thỏa mãn điều kiện biến win khác 0, nếu ghi đè đến byte 25 thì biến lose cũng được ghi đè không trả về flag.

## Exercise 3 — Precision (Hard)

Bài này tương tự bài ở trên về source code, nhưng khác ở chỗ là lần này ta không có source code để đọc, cũng như vị trí cụ thể khoảng cách giữa hai biến win và lose hay cái nhìn trực quan các byte đã bị ghi đè. Vì vậy ta cần sử dụng reverse engineering để debug.

Mở binary bằng GBD “gdb -q /challenge/binary-exploitation-lose-variable”, chọn cú pháp assembly intel “set disassembly-flavor intel”.

Xem danh sách hàm “info functions”: sẽ thấy các hàm có trong bài mà ta không thấy được bình thường do thiếu file mã nguồn. Trọng tâm của bài này sẽ là hàm challenge vì nó chứa thông tin về biến cũng như khoảng cách từ buffer đến biến win, lose,… “disassemble challenge”.

![Corrupting Memory — Practice figure 1](/assets/images/binary/corrupting-memory-practice/figure-01.png)

Hàm tạo stack frame mới và dành 0x60 byte trên stack cho biến cục bộ, các biến được truy cập bằng địa chỉ dạng “[rbp - offset]”.

```asm
0x401fc2 <+110>: mov rdx, QWORD PTR [rbp-0x38]
0x401fc6 <+114>: lea rax, [rbp-0x30]
0x401fca <+118>: mov rsi, rax
0x401fcd <+121>: mov edi, 0x0
0x401fd2 <+126>: call 0x401140 <read@plt>
```

Nạp địa chỉ “rax = rbp-0x30” sau đó copy giá trị trong thanh ghi rax sang rsi, trong Linux 64-bit, rsi tương ứng với tham số thứ 2 của hàm read()

“mov edi,0x0”: Tham số thứ nhất = 0 chính là stdin (tham số thứ nhất là rdi).

“mov rdx, QWORD PTR [rbp-0x38]”: Trước đấy tham số thứ 3 rdx đã được nạp giá trị tại [rbp-0x38] ở trên “mov QWORD PTR [rbp-0x38], 0x1000”, hiểu đơn giản là “rdx=4096”. Suy ra được buffer sẽ bắt đầu tại “rbp-0x30”.

![Corrupting Memory — Practice figure 2](/assets/images/binary/corrupting-memory-practice/figure-02.png)

“0x40200c: mov eax, DWORD PTR [rbp-0x14]”: Biến “lose_variable” có giá trị 4 byte tại “rbp-0x14”.

“0x402029: mov eax, DWORD PTR [rbp-0x18]”: Biến “win_variable” thì được đọc giá trị tại “rbp-0x18”. Sau khi kiểm tra nếu biến lose=0 và win khác 0 đồng thời thì trả flag.

“0x40204b: mov rcx, QWORD PTR [rbp-0x8]”: Đọc canary đã lưu trong stack frame vào rcx. “0x40204f: xor rcx, QWORD PTR fs:0x28”: So sánh canary đã lưu với canary gốc trong vùng “fs:0x28”, nếu giá trị giống nhau thì tiếp tục chương trình, nếu không thì dừng lại để tránh ghi đè đến return address.

buffer: rbp - 0x30<br>win: rbp - 0x18<br>lose: rbp - 0x14<br>canary: rbp - 0x08

Khoảng cách từ buffer đến canary là: 0x30-0x08=0x28=40 byte. Tương tự khoảng cách từ buffer đến “win_variable” là 24 byte, nền từ byte 2528 sẽ là 4 byte của biến win, sau đó sẽ là 4 byte của biến lose. Ta cần ghi đè vừa đủ để nhận được flag.

## Exercise 4 — Variable Control (Easy)

Bài này về logic vẫn giống như các bài trước, tuy nhiên điểm khác ở đây là chương trình yêu cầu ghi giá trị “win_variable” 1 giá trị xác định, nếu kiểm tra điều kiện thấy “win_variable” khác 0 nhưng không đúng với yêu cầu thì cũng không nhận được flag.

Mảng input có kích thước 27 byte, vì vậy ngoài 27 ban đầu thường sẽ cần thêm 1 byte đệm vì int thường được căn chỉnh tại địa chỉ chia hết cho 4. Nên bắt đầu ghi từ offset thứ 28 31 giá trị “0x679b4be5” tương ứng với “\xe5\x4b\x9b\x67” thì sẽ nhận được flag.

```python
python3 -c 'import sys;sys.stdout.buffer.write(b"A"*28+b"\xe5\x4b\x9b\x67")'| /challenge/binary-exploitation-var-control-w
```

## Exercise 5 — Variable Control (Hard)

Bài này là phiên bản khó hơn của bài vừa rồi, nó không cung cấp mã nguồn, vì vậy nếu theo cách thông thường ta không thể biết được giá trị cần ghi cho “win_variable” là gì, cũng như kích thước của buffer và padding là bao nhiêu trước khi đến biến “win_variable” và “lose_variable”. Vì vậy ta cần dùng kỹ thuật “reverse engineering” để khai thác.

Sau ghi dùng gdb và xem function “challenge” thì thấy địa chỉ bắt đầu của buffer là [rbp-0x80], biến win là [rbp-0x1c] và biến lose là [rbp-0x18]. Và giá trị cần ghi xuất hiện ở “cmp eax,0x7e9f68f”, khi ghi trong linux little-endian reverse sẽ là “\x8f\xf6\xe9\x07”.

## Exercise 6 — Control Hijack (Easy)

Bài này mô tả không có gì hết, vẫn tiến hành đọc mã nguồn như bình thường, ta thấy nhiệm vụ bây giờ không còn là ghi đè giá trị vào biến “win_variable” mà giờ đây ta cần ghi đè địa chỉ của hàm win() vào “saved return address”. Thông thường khi kết thúc hàm challenge() thì lệnh ret được gọi để lấy 1 giá trị trong stack rồi nhảy đến địa chỉ mới đó. Vậy nếu như ta ghi đè được địa chỉ mới này là địa chỉ của hàm win(), là ta lấy được flag rồi.

![Corrupting Memory — Practice figure 3](/assets/images/binary/corrupting-memory-practice/figure-03.png)

Thử ghi đè một số bất kỳ các byte, output cho ta biết địa chỉ bắt đầu của buffer, địa chỉ của địa chỉ trả về cần được ghi đè và giá trị địa chỉ của hàm win() cần được trỏ đến. Lấy địa chỉ trả về trừ đi địa chỉ bắt đầu buffer là tính được 136 byte thuộc phần buffer sau đó là 4 byte cần được ghi đè chính xác giá trị “\xc0\x1e\x40\x00” của hàm win() nhận được flag.

## Exercise 7 — Control Hijack (Hard)

![Corrupting Memory — Practice figure 4](/assets/images/binary/corrupting-memory-practice/figure-04.png)

Dựa vào “info functions” để biết được địa chỉ của hàm win(), giá trị mà ta ghi đè để save return address trỏ đến. Giá trị win_address là “0x0000000000401bb0”.

![Corrupting Memory — Practice figure 5](/assets/images/binary/corrupting-memory-practice/figure-05.png)

Vì bài có format “push rbp; mov rbp,rsp” nên địa chỉ save return address mặc định sẽ là [rbp+0x08], trên hình có thể thấy tham số thứ 2 “rsi” được nạp giá trị của rax mà “rax = rbp-0x50”. Nên khoảng cách byte cần được ghi đè sẽ là [rbp+0x08]-[rbp-0x50]= 88 bytes.

Sau đó ghi đè 88 byte bất kì và thêm 4 byte của địa chỉ hàm win() là sẽ lấy được flag.

## Exercise 8 — Tricky Control Hijack (Easy)

Bài này vì đang ở mức độ Easy nên nó dễ hơn so với bài toán thực tế, mục tiêu của ta vẫn là ghi đủ 40 byte padding tính từ “0x7ffda2cf0600” đến “0x7ffda2cf0628”. Sau đó đáng nhẽ ra phải ghi đè ret về địa chỉ bắt đầu của hàm “win_authed” nhưng trong hàm có đoạn kiểm tra token với giá trị “0x1337”, nếu đúng mới trả về flag. Tuy nhiên bài yêu cầu ta sẽ thực hiện bước đó ở phần sau, việc của ta chỉ cần cho ret trả về địa chỉ sau khi đã validate xong giá trị token và gọi đến phần in flag, cụ thể là “0x0000000000401c70”.

![Corrupting Memory — Practice figure 6](/assets/images/binary/corrupting-memory-practice/figure-06.png)

## Exercise 9 — Tricky Control Hijack (Hard)

Bài này về ý tưởng vẫn như bài độ khó Easy, tuy nhiên vẫn như vậy, ta không có file mã nguồn để đọc trực tiếp địa chỉ bắt đầu của buffer, địa chỉ ret trả về hay mục tiêu cần được ghi đè. Vì vậy cần dịch ngược, đọc chức năng của các function và tìm ra địa chỉ dựa trên các tham số có sẵn.

Như ở đây, thanh ghi “rsi” tương ứng với tham số thứ 2 trong hàm read(), cụ thể đây là con trỏ tới bộ đệm dữ liệu hoặc dễ hiểu hơn là địa chỉ bắt đầu buffer. Địa chỉ trả về (ret) là [rbp-0x08], kết hợp ta tính được số byte cần được ghi đè ở phần pading sẽ là 104 bytes.

![Corrupting Memory — Practice figure 7](/assets/images/binary/corrupting-memory-practice/figure-07.png)

Vì bài lab chỉ yêu cầu ta ghi đè đến phần địa chỉ đã kiểm tra xong token và trả về flag, vì vậy “disassemble win_authed” cho ta biết vị trí cần được ghi đè là “0x0000000000401a95”. Sau đó chỉ cần truyền payload vào là sẽ lấy được flag từ hàm “python3 -c 'import sys;sys.stdout.buffer.write(b"A"*104+b"\x95\x1a\x40\x00")'| /challenge/binary-exploitation-control-hijack-2”.

![Corrupting Memory — Practice figure 8](/assets/images/binary/corrupting-memory-practice/figure-08.png)

## Exercise 10 — PIES (EASY)

Bài này là bài đầu tiên có cơ chế ASLR và PIES, nói dễ hiểu là sau mỗi lần chạy nếu chương trình crash sẽ thay đổi ngẫu nhiên các bit cao của địa chỉ cần được ghi đè. (địa chỉ buffer, địa chỉ ret,…)

Tuy nhiên, sau một vài lần chạy thử dù địa chỉ bắt đầu ghi buffer và địa chỉ ret có thay đổi nhưng khoảng cách của chúng luôn bằng 104 bytes phần buffer sẽ chứa 104 bytes.

Ngoài ra, khi nhìn vào địa chỉ ret cần nhắm đến là địa chỉ hàm “win_authed”, mọi bit cao đều được giữ nguyên, tương tự là 3 bit thấp, chỉ có 1 bit bị thay đổi, vì vậy vấn đề cần giải quyết ở đây là 2 bytes đầu tiên theo little-endia, cụ thể ở đây là “?b8f”.

Sau một vài lần thử thì thấy địa chỉ ret trả về đã đúng với địa chỉ của hàm “win_authed”, nhưng vì trong hàm có cơ chế validate bằng token. Đối với bài hiện tại ta chưa có cơ chế bypass nên mục tiêu chuyển đến câu lệnh sau khi đã xác thực token thành công.

![Corrupting Memory — Practice figure 9](/assets/images/binary/corrupting-memory-practice/figure-09.png)

Để có thể chắc chắn với giả thuyết địa chỉ bị thay đổi sau mỗi lần chạy, ta sử dụng cụm dòng lệnh sau trong gdb để có thể xem thử sự thay đổi của địa chỉ trong 5 lần thay đổi (Nhập từng dòng lệnh):

set pagination off<br>set disable-randomization off<br>set $i = 0<br>while $i < 5<br>run < /dev/null<br>disassemble win_authed<br>set $i = $i + 1<br>end

“set pagination off”: Tắt chức năng phân trang kết quả của gdb

“set disable-randomization off”: Cho phép ASLR hoạt động, nếu tắt đi không thể xem được sự thay đổi.

Đoạn sau là đặt biến “i=0” chạy hết 5 lần vòng lặp, “< /dev/null” dùng để chuyển dữ liệu đầu vào của chương trình.

Vì /dev/null không có dữ liệu, lệnh read() trong chương trình sẽ nhận EOF và chương trình thường kết thúc nhanh, không bị chờ nhập.

“disassemble win_authed”: Dịch ngược và hiển thị mã máy của “win_authed”.

Sau những lần chạy ta rút ra việc ghi đè sẽ nhắm đến là 2 byte cuối của câu lệnh “lea rdi,[rip+0x153e]” trong hàm “win_authed”, vì bài nào giá trị random là bất kì của kí tự “?”, vì vậy cứ lặp đi lặp lại 1 payload đến khi nó đúng là nhận được flag như bên dưới.

![Corrupting Memory — Practice figure 10](/assets/images/binary/corrupting-memory-practice/figure-10.png)

## Exercise 11 — PIES (HARD)

Bài này về ý tưởng vẫn như bài trên thôi, vẫn như cũ là chúng ta sẽ không có file mã nguồn “.c”, tuy nhiên về cách làm lúc này chỉ khác một chút, giờ đây ta sẽ chạy 3 lần và debug hàm “challenge” để xem khoảng cách từ buffer đến ret là bao nhiêu bytes, cụ thể ở bài này là 56 bytes.

![Corrupting Memory — Practice figure 11](/assets/images/binary/corrupting-memory-practice/figure-11.png)

Sau đó tiếp tục lặp lại nhưng lần này mục tiêu là debug hàm “win_authed”, sau một vài lần chạy thì xác định ra được mục tiêu lần này là 2 bytes “?c42”, lúc này đã có đủ payload, chỉ cần brute-force lặp đi lặp lại là sẽ lấy được flag (Có thể hơi lâu).

![Corrupting Memory — Practice figure 12](/assets/images/binary/corrupting-memory-practice/figure-12.png)

Sau một số lần thử thì nhận được flag, bypass được cơ chế randomization của ASLR và PIES.

![Corrupting Memory — Practice figure 13](/assets/images/binary/corrupting-memory-practice/figure-13.png)

## Exercise 12 — String Lengths (Easy)

Bài này về ý tưởng chung vẫn giống như 2 bài ở phần trên, đều cần chạy brute-force câu lệnh sau khi validate token trong “win_authed”, tuy nhiên điểm mới là trong bài có logic là ta cần 72 bytes buffer như bình thường và 2 bytes cần được ghi đè đến địa chỉ để lấy flag.

Tuy nhiên, điểm đổi mới là nó có cơ chế validate bằng string_length, nếu như string_length >= 28 thì chương trình sẽ bị crash, vì vậy ta bypass bằng cách truyền 26 bytes A như bình thường sau đó thêm 1 byte “\x00” để đánh lừa bộ lọc độ dài chuỗi, sau đó tiếp tục gửi 45 bytes đệm còn lại và 2 bytes cần được ghi đè.

Sở dĩ chuyện này xảy ra vì byte “\x00” được gọi là byte “null terminator”, với các hàm xử lý chuỗi, phần sau \x00 bị xem như không tồn tại. Nhưng nếu chương trình copy theo số byte thực tế bằng memcpy, các byte sau \x00 vẫn được copy.

Sau khi debug hàm “win_authed” thì ta xác định 2 bytes cần xử lý ở đây là “?11f”, truyền payload sau 1 vài lần gambel thì thu được flag.

![Corrupting Memory — Practice figure 14](/assets/images/binary/corrupting-memory-practice/figure-14.png)

## Exercise 13 — String Lengths (Hard)

Bài này hơi khác một chút là ngoài tìm vị trí để brute-force, ta còn phải tìm cách số bytes buffer và số bytes để thỏa mãn “string_length”. Đối với số bytes buffer cần truyền vào ở đây sẽ là: 0x8+0xa0=168 bytes

![Corrupting Memory — Practice figure 15](/assets/images/binary/corrupting-memory-practice/figure-15.png)

![Corrupting Memory — Practice figure 16](/assets/images/binary/corrupting-memory-practice/figure-16.png)

Tiếp theo là điều kiện của “string_length”, ta thấy ở đây số lượng bytes cần xử lý sẽ là ta thấy nó sẽ lấy giá trị của ô nhớ [rbp-0x20] trong stack so sánh với 0x70 = 112 bytes. Nếu validate qua thì chương trình mới chạy được, đó là lý do ta sẽ truyền vào 110 bytes và thêm 1 byte “\x00”.

![Corrupting Memory — Practice figure 17](/assets/images/binary/corrupting-memory-practice/figure-17.png)

Nội dung của hàm “memcpy” sẽ đưa tất cả các bytes đươch truyền từ payload đến hết ô nhớ [rbp-0xa0], chứ không dừng lại ở kí tự “\x00”.

![Corrupting Memory — Practice figure 18](/assets/images/binary/corrupting-memory-practice/figure-18.png)

Vậy tóm lại payload lúc này sẽ là 110 bytes kí tự bất kì + 1 byte “\x00” + 57 bytes kí tự bất kì tiếp + 2 bytes ghi đè Cứ tiếp tục brute-force cho đến khi nhận được flag.

![Corrupting Memory — Practice figure 19](/assets/images/binary/corrupting-memory-practice/figure-19.png)
