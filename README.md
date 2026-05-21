# PROJECT : MULTI-AGENT SEARCH PACMAN 
## Giới thiệu project
  Dự án này thuộc khuôn khổ môn học Trí tuệ Nhân tạo (dựa trên học liệu CS188 của UC Berkeley). Mục tiêu của dự án là xây dựng các thuật toán tìm kiếm đa tác nhân (Multi-Agent Search) để điều khiển Pacman sinh tồn, ăn thức ăn và né tránh bầy ma trong các môi trường từ tĩnh đến động, từ đối kháng tuyệt đối đến ngẫu nhiên.

Tệp mã nguồn được lập trình và chỉnh sửa chính trong dự án này là: multiAgents.py.

## Các thuật toán triển 
Dự án bao gồm 5 cấu phần chính, nâng cấp dần mức độ thông minh của Pacman:
  1. Reflex Agent (Q1): Tác nhân phản xạ đánh giá trạng thái tức thời dựa trên nghịch đảo khoảng cách đến thức ăn và bầy ma.
  2. Minimax Agent (Q2): Tác nhân mô hình hóa trò chơi dưới dạng cây tìm kiếm đối kháng. Pacman tối đa hóa điểm số (MAX), trong khi bầy ma tối thiểu hóa điểm số (MIN).
  3. Alpha-Beta Pruning Agent (Q3): Tối ưu hóa Minimax bằng cơ chế cắt tỉa các nhánh thừa (alpha - beta).
  4. Expectimax Agent (Q4): Tác nhân ra quyết định dựa trên xác suất, phù hợp với môi trường bầy ma di chuyển ngẫu nhiên. Pacman trở nên thực dụng hơn, biết chấp nhận rủi ro thấp để ăn điểm cao thay vì bỏ chạy mù quáng.
  5. Better Evaluation Function (Q5): Hàm lượng giá trạng thái tối ưu, kết hợp các trọng số thực nghiệm (khoảng cách thức ăn, số lượng viên năng lượng, trạng thái ma hoảng sợ).

## Cài đặt và môi trường
  Dự án yêu cầu cài đặt Python 3.6 trở lên. Không yêu cầu cài đặt thêm thư viện bên ngoài.

  Tải mã nguồn về và di chuyển vào thư mục dự án:
  
    git clone https://github.com/Duonglt1812/Pacman-Multi-Agent-Search.git

  ## Hướng dẫn chạy thử nghiệm 
  Bạn có thể tự do kiểm thử các tác nhân bằng các lệnh command-line dưới đây:
  1. Chạy Reflex Agent:
     
    python pacman.py -p ReflexAgent -l testClassic
  2. Chạy Minimax Agent (độ sâu = 2):
  
    python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=2
  3. Chạy Alpha-Beta Agent (chơi với 2 con ma):

    python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
  4. Chạy Expectimax Agent:
     
    python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
  5. Chạy Custom Evaluation Function (Q5):
     
    python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 10

  ## Đánh giá tự động
  Để kiểm tra điểm số và tính hợp lệ của mã nguồn, chạy trình chấm điểm tự động tích hợp sẵn:
  - Chấm toàn bộ dự án
    
        python autograder.py

  - Chấm từng câu cụ thể (Ví dụ Q3)
    
        python autograder.py -q q3

## Kết quả thực nghiệm và tổng kết
| Agent | Hiệu năng | Tỉ lệ thắng | Nhận xét hành vi |
| :--- | :--- | :--- | :--- |
| **Minimax (Q2)** | Chậm (Dễ Timeout nếu depth > 2) | ~60% | Quá thận trọng, luôn nghĩ ma đi nước đi hoàn hảo. |
| **Alpha-Beta (Q3)** | **Nhanh** (Giảm > 50% số nút duyệt) | ~60% | Giữ nguyên logic đối kháng nhưng tối ưu tốc độ vượt trội. |
| **Expectimax + Eval (Q4, Q5)** | Nhanh & Ổn định | **> 80% (> 1000 điểm)** | Chấp nhận rủi ro thông minh, đạt kết quả xuất sắc nhất. |
