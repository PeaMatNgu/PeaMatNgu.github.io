---
title: "Fortune Teller — FortID CTF 2026"
date: 2026-10-13
summary: "A format-string exploitation write-up using PIE address leakage and an arbitrary write."
platform: "FortID CTF 2026"
tags:
  - binary-exploitation
  - format-string
---
**Fortune Teller**
- Category: Binary Exploitation
- Rating: Easy
- Flag: `FortID{Fortun3_Fav0r5_Th3_b0ld_bu7_al50_Th05e_Th4t_C4n_Expl0i7_F0rma7_Str1ng_VulnZZ_aecdfe8f03}`

Khi đọc các file mà thử thách cho, ta thấy có 2 file chính để test local trước là `chall.c` và `fortune` ngoài ra còn có 1 file mô tả `readme.md`. Sau khi đọc file mô tả ta biết được bài này có các cơ chế bảo mật bao gồm: `Full RELRO, stack canary, NX, PIE`.

Dựa vào mã nguồn của `chall.c`, mục tiêu của bài này sẽ là khiến giá trị biến toàn cục `blessing` --> Khi này điều kiện đúng, hàm `win()` được gọi và in flag.
![Screenshot 2026-10-10 111900](https://hackmd.io/_uploads/HkTCnEviMl.png)

Lỗ hổng chính của bài này là **Format String**, trong `ask_oracle()` ta thấy biến question do người dùng truyền vào lại được truyền trực tiếp vào `printf`.
:::info
Format String Vulnerability (lỗ hổng chuỗi định dạng) là một lỗi bảo mật xảy ra khi ứng dụng sử dụng dữ liệu đầu vào do người dùng cung cấp trực tiếp làm chuỗi định dạng cho các hàm xử lý chuỗi (chẳng hạn như printf(), fprintf(), sprintf() trong ngôn ngữ C/C++) mà không qua kiểm tra.
:::
![Screenshot 2026-10-10 112325](https://hackmd.io/_uploads/Hkc0aVDsze.png)

Cụ thể với bài này ta sẽ lợi dụng `%p` để leak địa chỉ của hàm main để tính được giá trị **PIE Base** bằng cách trừ địa chỉ runtime của hàm main và địa chỉ offset tĩnh của main. Dựa vào **PIE Base** ta sẽ tính được địa chỉ runtime cần ghi của `blessing`.
:::info
PIE cho phép chương trình được nạp vào một địa chỉ bộ nhớ ngẫu nhiên mỗi lần chạy (kết hợp với cơ chế ASLR của hệ điều hành).
:::
Dùng `%n`, hoặc công cụ `fmtstr_payload()`, để ghi dữ liệu vào địa chỉ tùy ý.
Lấy các offset tĩnh quan trong bằng `nm`, nó sẽ liệt kê các symbol trong binary, tham số `-a` để hiển thị toàn bộ, `-n` để sắp xếp theo địa chỉ tăng dần và `fortune` là file binary cần giải thích.
`nm -an fortune | grep -E 'main$|blessing|win$|ask_oracle$|receive_blessing$'`
![Screenshot 2026-10-10 120922](https://hackmd.io/_uploads/BJBj_Swofe.png)

Ta sẽ lợi dụng tham số `question` để `printf` đọc các argument thứ 1,2,3,... từ vùng register/stack. Khi đọc đến vị trí thứ 6, các byte được lấy ra chính là giá trị của các bytes ta vừa nhập.
![Screenshot 2026-10-10 121258](https://hackmd.io/_uploads/SyWvsHPsMl.png)

Khi nhìn tiếp ở giá trị số 48, ta thấy một chuỗi `0x5ab1fe853570`, đặc biệt ở chỗ là **PIE** có một cơ chế rất hay là thông thường 3 bit đầu tiên (Theo dạng Little-Endian) của 1 hàm sẽ giống nhau, hiểu đơn giản là **PIE** làm thay đổi địa chỉ của 1 hàm đi ngẫu nhiên nhưng 3 bit đầu tiên này luôn không thay đổi. Vì vậy, ta có thể đoán được vị trí số 49 này là địa chỉ runtime của hàm main mà ta biết trước đó `0x1570`. Sau khi tính được giá trị `PIE_Base` thì ta cộng với địa chỉ `blessing` tĩnh để tính được địa chỉ `blessing_runtime`.
>`PIE_Base = main_runtime - main`

Sau khi biết được địa chỉ cần ghi, việc tiếp theo là sử dụng `fmtstr_payload` để ghi giá trị `0x1337` vào `blessing`.
![Screenshot 2026-10-10 123321](https://hackmd.io/_uploads/SyxrCHDoGl.png)

- 6: Vị trí argument
- target: Mục tiêu cần ghi
- 0x1337 là giá trị cần ghi
- write_size: Kích thước mỗi lần ghi (%hn).

:::success
Ý tưởng script của chúng ta sẽ là: Mở kết nối với instance, gửi byte `1` để chọn `1. Ask the oracle` sau đó gửi `%49$p` để yêu cầu `printf` in giá trị runtime của `main`. Đợi trả về kết qủa thì dùng nó để tính giá trị `PIE_Base` --> Tính giá trị `blessing_runtime` và tạo format-string payload. Chọn `1.Ask the oracle` với payload đã được tạo, sau đó chọn `2.Receive blessing` sẽ kích hoạt điều kiện đúng, `win()` chạy --> Nhận được flag.
:::
Sau khi chạy thử local thì thu được flag thử nghiệm, ta tiến hành chạy script `exploit_pwn1.py` với instance của thử thách và thu được flag `FortID{Fortun3_Fav0r5_Th3_b0ld_bu7_al50_Th05e_Th4t_C4n_Expl0i7_F0rma7_Str1ng_VulnZZ_aecdfe8f03}`
![Screenshot 2026-10-10 124846](https://hackmd.io/_uploads/SyQkMUwszx.png)
## Challenge files

- [FortID CTF 2026 challenge files on GitHub](https://github.com/PeaMatNgu/FortID_CTF_2026/tree/main/Fortune_Teller)
