# Bai-tap-Co-Caro-9x9
Bài tập giữa kỳ môn Trí tuệ Nhân tạo - UET

## Tổng quát
Bài tập này là Cờ Caro với diện tích bàn cờ 9x9 với 2 người chơi hoặc là 1 người chơi với AI. Mục tiêu của trò chơi là đạt được 4 quân của mình theo chiều bất kỳ (Ngang/Dọc/Chéo) để thắng. Thuật toán AI trong bài toán này là Minimax kết hợp với cắt tỉa Alpha-Beta

## Yêu cầu
Để có thể chạy chương trình, cần phải tải thư viện Pygame về

## Cấu trúc file

├── src/
│   ├── ai.py           # Chứa thuật toán Minimax, Alpha-Beta và hàm Heuristic
│   ├── config.py       # Config của game
│   └── game.py         # Chứa class CaroGame xử lý luật chơi
├── main.py             # Vòng lặp của trò chơi và vẽ giao diện UI
├── report.pdf          # File báo cáo tài liệu
├── report.docx         # File báo cáo tài liệu
└── README.md           # Tổng quát về dự án

## Cách mở trò chơi
Mở file main.py lên và chạy code thì chương trình sẽ mở lên
<img width="1002" height="915" alt="image" src="https://github.com/user-attachments/assets/4bd13541-3eae-4d44-9978-1fc082119efd" />
