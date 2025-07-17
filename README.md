# Game Tic Tac Toe tuỳ biến với chủ đề Ngũ Hành

Một phiên bản mở rộng của trò chơi Tic Tac Toe cổ điển, được phát triển bằng Python và thư viện Kivy, cho phép người chơi tùy chỉnh sâu vào luật chơi và trải nghiệm.

***For the English version, please scroll down.***

---

## ✨ Tính năng nổi bật

* **Lưới chơi tùy biến:** Tự do điều chỉnh số hàng và cột của bàn cờ ngay tại màn hình chính.
* **Luật thắng linh hoạt:** Thiết lập số lượng quân cờ liên tiếp cần có để giành chiến thắng.
* **Vật cản ngẫu nhiên:** Thêm thắt độ khó và tính chiến thuật với các ô vật cản trên bàn cờ, số lượng có thể tùy chỉnh.
* **Chủ đề Ngũ Hành:** Trải nghiệm 5 giao diện độc đáo dựa trên 5 yếu tố: Kim, Mộc, Thủy, Hỏa, và Thổ.
* **Chơi với máy (AI):** Thử thách bản thân với đối thủ máy tính.

## 🛠️ Cài đặt & Chạy game

Để chạy trò chơi trên máy tính, bạn cần cài đặt Python và các thư viện cần thiết.

1.  **Cài đặt các thư viện:**
    ```bash
    pip install kivy pytest pyreadline3
    ```
2.  **Chạy game:**
    ```bash
    python main.py
    ```
3.  **Chạy kiểm thử (Testing):**
    Để chạy các bài kiểm thử tự động, sử dụng lệnh sau trong terminal:
    ```bash
    pytest -v
    ```

## 📱 Cài đặt trên Android

1.  Truy cập thư mục `apk` trong repo này.
2.  Tải file `.apk` về thiết bị Android của bạn.
3.  Mở file và tiến hành cài đặt (bạn có thể cần cho phép cài đặt từ nguồn không xác định trong cài đặt của điện thoại).

## Lưu ý quan trọng:
- Khi chơi game này trên điện thoại, vui lòng `sử dụng bàn phím mặc định` của điện thoại `để tránh gây lỗi không thể xóa giá trị` hiện có trong ô text input. Còn nếu `vẫn muốn sử dụng các bàn phím khác` như Laban Key, vui lòng `trước khi xóa giá trị hiện có` trong ô text input, hãy `nhấn vào 1 phím` ký tự là `chữ bất kỳ` (`không phải số`) để `kích hoạt được nút backspace` của bàn phím điện thoại đó, `khi đó có thể xóa bình thường`, vui lòng `lặp lại` với `mỗi lần ấn vào ô` text input `mà muốn xóa đi giá trị hiện có`.

Để hiểu rõ hơn về quá trình phát triển, thuật toán và các chi tiết kỹ thuật, vui lòng tham khảo [báo cáo đầy đủ tại đây](https://sg.docworkspace.com/d/sIFbMpojLAbWa4sMG?sa=601.1037).

## 👨‍💻 Sinh viên thực hiện

Dự án này được hoàn thành bởi các sinh viên:

* **Hoàng Quốc Duy** - 24520373 - [Github](https://github.com/Rod-HD)
* **Nguyễn Thái Duy** - 24520390 - [Github](https://github.com/thaiduy436)
* **Nguyễn Quốc Khánh** - 24520793 - [Github](https://github.com/nutbred)

---
<br>

# Customizable Tic Tac Toe with a Five Elements Theme

An extended version of the classic Tic Tac Toe game, developed using Python and the Kivy library, allowing for deep customization of game rules and experience.

## ✨ Key Features

* **Customizable Grid:** Freely adjust the number of rows and columns on the game board directly from the home screen.
* **Flexible Winning Condition:** Set the required number of consecutive pieces to achieve victory.
* **Random Obstacles:** Increase difficulty and strategic depth with obstacle cells on the grid, with an adjustable count.
* **Five Elements Theme:** Experience 5 unique themes based on the five elements: Metal (Kim), Wood (Mộc), Water (Thủy), Fire (Hỏa), and Earth (Thổ).
* **Play against AI:** Challenge yourself with a computer opponent.

## 🛠️ Installation & Running the Game

To run the game on your computer, you need Python and the required libraries installed.

1.  **Install Libraries:**
    ```bash
    pip install kivy pytest pyreadline3
    ```
2.  **Run the game:**
    ```bash
    python main.py
    ```
3.  **Run Tests:**
    To run the automated tests, use the following command in your terminal:
    ```bash
    pytest -v
    ```

## 📱 Android Installation

1.  Navigate to the `apk` directory in this repository.
2.  Download the `.apk` file to your Android device.
3.  Open the file and proceed with the installation (you may need to enable "Install from unknown sources" in your phone's settings).

## 📄 Project Report

For a detailed understanding of the development process, algorithms, and technical specifics, please refer to the [full report here](https://your-report-link-here.com).

## 👨‍💻 Developers

This project was completed by the following students:

* **Hoàng Quốc Duy** - 24520373 - [Github](https://github.com/Rod-HD)
* **Nguyễn Thái Duy** - 24520390 - [Github](https://github.com/thaiduy436)
* **Nguyễn Quốc Khánh** - 24520793 - [Github](https://github.com/nutbred)
