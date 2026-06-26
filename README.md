# 🤖 Trí Tuệ Nhân Tạo (Artificial Intelligence)

## 📝 Giới thiệu

Repository này lưu trữ mã nguồn và các bài tập về nhà trong quá trình học môn Trí Tuệ Nhân Tạo (252ARIN330585_06).

Mục tiêu chính của repository là chuyển hóa các kiến thức lý thuyết về tìm kiếm, tối ưu hóa, lập luận logic và học máy cơ bản thành các hiện thực cụ thể trong mã nguồn.

---

## 👤 Thông tin cá nhân

* **Họ và tên:** Nguyễn Trần Anh Quốc (@anhquoc11)
* **Mã số sinh viên:** 24110314
* **Ngôn ngữ lập trình:** Python 3.11.9
* **Môi trường phát triển:** Jupyter Notebook, VS Code, v.v.

---

## 🧹 Project cá nhân: Bài toán máy hút bụi

### ✨ Tính năng nổi bật

* **Hệ thống đa dạng thuật toán:** Hiện thực nhiều giải thuật AI kinh điển, bao gồm các thuật toán tìm kiếm mù, tìm kiếm có thông tin, tìm kiếm cục bộ, giải bài toán thỏa mãn ràng buộc (CSP), tìm kiếm trong môi trường không chắc chắn và tìm kiếm trong trò chơi.
* **Trực quan hóa quá trình tìm kiếm:** Giao diện mô phỏng trực quan giúp quan sát rõ từng bước hoạt động của thuật toán.
* **Theo dõi thời gian thực:** Hiển thị log chi tiết, trạng thái từng bước và tiến trình xử lý của tác nhân trong quá trình tìm kiếm.

🔗 **Liên kết:** [Project cá nhân của tôi]https://github.com/anhquoc11/TriTueNhanTao/tree/6aae8781a398aa291b4a009a13f6d664ca8e3162/project_ca_nhan

## 🧠 Các thuật toán đã hiện thực
### 1. Tìm kiếm mù (Uninformed Search)

#### 🟩 Breadth-First Search (BFS)
Thuật toán tìm kiếm theo chiều rộng, mở rộng toàn bộ các nút ở mức độ sâu hiện tại trước khi chuyển sang mức tiếp theo. BFS đảm bảo tìm được lời giải có số bước ngắn nhất trong không gian trạng thái không trọng số.

Thuật toán sử dụng hàng đợi (Queue - FIFO) để quản lý danh sách các trạng thái biên (frontier), giúp duy trì thứ tự khám phá theo từng lớp.

---

#### 🟩 Depth-First Search (DFS)
Thuật toán tìm kiếm theo chiều sâu, luôn mở rộng trạng thái con sâu nhất trước khi quay lui. DFS có ưu điểm tiết kiệm bộ nhớ do chỉ lưu trữ đường đi hiện tại.

Tuy nhiên, DFS không đảm bảo tìm được lời giải tối ưu và có thể rơi vào vòng lặp vô hạn nếu không kiểm soát trạng thái đã thăm.

---

#### 🟩 Iterative Deepening Search (IDS)
IDS là sự kết hợp giữa BFS và DFS, thực hiện DFS với giới hạn độ sâu tăng dần qua từng vòng lặp.

Thuật toán đảm bảo:
- Tính đầy đủ (complete) giống BFS
- Tối ưu bộ nhớ giống DFS

IDS đặc biệt hiệu quả trong không gian trạng thái lớn khi không biết trước độ sâu của lời giải.

---

#### 🟩 Uniform Cost Search (UCS)
UCS mở rộng các nút dựa trên chi phí đường đi từ trạng thái ban đầu, luôn ưu tiên mở rộng nút có chi phí thấp nhất:

$$f(n) = g(n)$$

Trong đó:
- $g(n)$ là tổng chi phí từ trạng thái gốc đến nút hiện tại

Thuật toán sử dụng hàng đợi ưu tiên (Priority Queue) để đảm bảo luôn chọn đường đi tối ưu nhất tại mỗi bước mở rộng.

UCS đảm bảo tìm được lời giải tối ưu nếu tất cả chi phí đều không âm.

---

### 2. Tìm kiếm có thông tin (Informed Search)

#### 🟩 Greedy Best-First Search
Thuật toán tìm kiếm tham lam (greedy) lựa chọn mở rộng nút có giá trị heuristic tốt nhất tại thời điểm hiện tại, dựa trên ước lượng khoảng cách đến đích:

$$f(n) = h(n)$$

Trong đó:
- $h(n)$ là hàm heuristic ước lượng chi phí từ trạng thái hiện tại đến trạng thái đích

Thuật toán có xu hướng dẫn hướng nhanh về phía mục tiêu, giúp giảm thời gian tìm kiếm. Tuy nhiên, do chỉ dựa trên thông tin ước lượng mà bỏ qua chi phí đã đi, Greedy Best-First Search không đảm bảo tìm được lời giải tối ưu và có thể bị kẹt trong các nhánh không tối ưu.

---

#### 🟩 A* Search
A* là thuật toán tìm kiếm có thông tin tối ưu, kết hợp giữa chi phí đã đi và chi phí ước lượng còn lại:

$$f(n) = g(n) + h(n)$$

Trong đó:
- $g(n)$: chi phí thực tế từ trạng thái bắt đầu đến nút hiện tại  
- $h(n)$: chi phí ước lượng từ nút hiện tại đến đích

A* luôn mở rộng nút có giá trị $f(n)$ nhỏ nhất, đảm bảo vừa hiệu quả vừa tối ưu nếu hàm heuristic $h(n)$ thỏa mãn tính chất admissible (không đánh giá quá cao chi phí thực tế).

---

#### 🟩 Iterative Deepening A* (IDA*)
IDA* kết hợp giữa ý tưởng tìm kiếm theo độ sâu tăng dần của IDS và hàm đánh giá của A*:

$$f(n) = g(n) + h(n)$$

Thay vì lưu toàn bộ tập frontier như A*, IDA* sử dụng cơ chế giới hạn ngưỡng $f(n)$ và thực hiện tìm kiếm DFS có cắt tỉa theo ngưỡng này.

Mỗi vòng lặp sẽ tăng dần ngưỡng giới hạn $f(n)$, giúp:
- Giảm đáng kể bộ nhớ sử dụng so với A*
- Vẫn đảm bảo khả năng tìm được lời giải tối ưu

Tuy nhiên, nhược điểm của IDA* là có thể phải duyệt lại nhiều trạng thái nhiều lần, làm tăng thời gian tính toán trong không gian tìm kiếm lớn.
---

### 3. Tìm kiếm cục bộ (Local Search)

#### 🟩 Simple Hill Climbing
Thuật toán leo đồi đơn giản hoạt động bằng cách liên tục chọn trạng thái kế tiếp đầu tiên có giá trị heuristic tốt hơn trạng thái hiện tại. Hàm đánh giá sử dụng:

$$f(n) = h(n)$$

trong đó $h(n)$ biểu diễn mức độ “xấu” của trạng thái.

Thuật toán có ưu điểm là đơn giản, dễ cài đặt và tốc độ nhanh. Tuy nhiên, nó dễ rơi vào các điểm tối ưu cục bộ (Local Optimum), vùng bằng phẳng (Plateau) hoặc các đường dốc không rõ ràng (Ridge), dẫn đến không đảm bảo tìm được lời giải tốt nhất.

---

#### 🟩 Steepest Ascent Hill Climbing
Đây là phiên bản cải tiến của Hill Climbing, trong đó thuật toán không chọn trạng thái đầu tiên tốt hơn mà đánh giá toàn bộ tập trạng thái lân cận và chọn trạng thái có giá trị heuristic tốt nhất.

$$f(n) = h(n)$$

Phương pháp này giúp cải thiện chất lượng nghiệm so với Simple Hill Climbing, nhưng đổi lại chi phí tính toán mỗi bước tăng lên do phải duyệt toàn bộ không gian láng giềng.

---

#### 🟩 Stochastic Hill Climbing
Thuật toán lựa chọn ngẫu nhiên một trạng thái tốt hơn trong tập các trạng thái lân cận thay vì luôn chọn trạng thái tốt nhất. Cách tiếp cận này giúp tăng tính đa dạng trong quá trình tìm kiếm và giảm nguy cơ mắc kẹt tại cực trị cục bộ.

---

#### 🟩 Random-Restart Hill Climbing
Thuật toán thực hiện nhiều lần chạy Hill Climbing từ các trạng thái khởi tạo ngẫu nhiên khác nhau. Khi một lần chạy bị kẹt tại cực trị cục bộ, hệ thống sẽ khởi động lại từ đầu với trạng thái mới.

Phương pháp này giúp tăng xác suất tìm được nghiệm toàn cục trong không gian trạng thái lớn, đặc biệt hiệu quả khi không gian tìm kiếm có nhiều cực trị cục bộ.

---

#### 🟩 Local Beam Search
Thuật toán duy trì đồng thời $k$ trạng thái thay vì chỉ một trạng thái đơn lẻ. Tại mỗi bước:

1. Khởi tạo $k$ trạng thái ngẫu nhiên
2. Sinh toàn bộ trạng thái kế cận của tất cả $k$ trạng thái hiện tại
3. Đánh giá và chọn ra $k$ trạng thái tốt nhất làm tập trạng thái tiếp theo

Hàm đánh giá sử dụng:
$$f(n) = h(n)$$

Phương pháp này giúp mở rộng phạm vi tìm kiếm, giảm nguy cơ mắc kẹt nhưng vẫn giữ được tính tập trung vào các vùng tiềm năng của không gian trạng thái.

---

#### 🟩 Simulated Annealing
Thuật toán mô phỏng quá trình luyện kim, kết hợp giữa tìm kiếm leo đồi và yếu tố ngẫu nhiên nhằm tránh mắc kẹt tại cực trị cục bộ.

Độ thay đổi giá trị được tính:

$$\Delta = h(\text{next state}) - h(\text{current state})$$

Quy tắc chấp nhận:
- Nếu $\Delta < 0$: luôn chấp nhận trạng thái mới
- Nếu $\Delta \ge 0$: chấp nhận với xác suất:

$$p = e^{-\frac{\Delta}{T}}$$

Trong đó:
- $T$ là nhiệt độ hệ thống
- $T$ giảm dần theo hệ số làm nguội $\alpha$: $T = \alpha T$

Thuật toán có khả năng thoát khỏi cực trị cục bộ rất tốt, nhưng quỹ đạo tìm kiếm có thể không ổn định và kéo dài khi nhiệt độ còn cao.

---

### 4. Tìm kiếm trong môi trường không nhìn thấy (Search in Unobservable Environments)

Trong môi trường không quan sát được trực tiếp, tác nhân (agent) không thể xác định chính xác trạng thái hiện tại do thiếu thông tin từ cảm biến (camera, GPS, radar,...). Thay vào đó, agent phải duy trì một tập hợp các trạng thái có thể xảy ra, gọi là **Belief State**.

Belief State được cập nhật liên tục dựa trên:
- Hành động đã thực hiện
- Mô hình chuyển trạng thái của môi trường

Mục tiêu của bài toán là tìm một chiến lược hành động giúp đạt được trạng thái đích từ **tập trạng thái ban đầu không chắc chắn**.

---

### 🟩 AND-OR Search

AND-OR Search dùng trong môi trường không xác định hoặc không quan sát đầy đủ, nơi kết quả hành động không chắc chắn.

- **OR nodes:** lựa chọn hành động
- **AND nodes:** tất cả kết quả có thể xảy ra

✔ Tìm kiếm dạng cây kế hoạch (plan tree) thay vì đường đi đơn  
✔ Đảm bảo lời giải đúng trong môi trường không chắc chắn  
✔ Ứng dụng trong AI Planning và robot

---

### 🟩 BFS_MTPT (Multi-State BFS)

BFS_MTPT là biến thể BFS áp dụng cho nhiều trạng thái khởi đầu (belief state).

- Bắt đầu từ tập trạng thái $S_0 = \{s_1, s_2, ..., s_n\}$
- Thực hiện BFS đồng thời trên toàn bộ tập trạng thái
- Gộp trạng thái trùng để tránh lặp

✔ Xử lý tốt môi trường không quan sát đầy đủ  
✔ Mở rộng theo tập trạng thái thay vì một trạng thái  
✘ Chi phí cao hơn BFS thường

---

## Constraint Satisfaction Problem (CSP)

Trong CSP, mục tiêu là tìm một tập giá trị cho các biến sao cho thỏa mãn tất cả ràng buộc, thay vì chỉ tìm một đường đi như các bài toán tìm kiếm thông thường.

---

### 🟩 Backtracking Search

Backtracking là thuật toán tìm kiếm theo chiều sâu kết hợp quay lui khi vi phạm ràng buộc.

- Gán giá trị cho từng biến
- Nếu vi phạm → quay lui
- Thử giá trị khác

✔ Đơn giản, dễ cài đặt  
✔ Cắt nhánh sai sớm  
✘ Có thể duyệt nhiều trường hợp không cần thiết  

---

### 🟩 Forward Checking

Forward Checking cải tiến Backtracking bằng cách kiểm tra trước tương lai.

- Sau khi gán giá trị
- Loại bỏ giá trị không hợp lệ trong các biến chưa gán
- Nếu domain rỗng → quay lui ngay

✔ Giảm số nhánh phải duyệt  
✔ Phát hiện lỗi sớm hơn Backtracking  
✘ Tốn thêm chi phí cập nhật domain  

---

### 🟩 AC-3 (Arc Consistency)

AC-3 đảm bảo tính nhất quán giữa các biến bằng cách loại bỏ giá trị không hợp lệ trong miền giá trị.

- Xét các cặp ràng buộc (Xi → Xj)
- Loại bỏ giá trị không thỏa mãn
- Lặp đến khi ổn định

✔ Giảm mạnh không gian tìm kiếm  
✔ Tiền xử lý hiệu quả  
✘ Tốn chi phí ban đầu  

---

### 🟩 Min-Conflicts

Min-Conflicts là thuật toán local search cho CSP.

- Bắt đầu từ trạng thái ngẫu nhiên
- Chọn biến đang vi phạm
- Gán giá trị làm giảm xung đột nhiều nhất

✔ Rất nhanh cho bài toán lớn (N-Queens, scheduling)  
✔ Không cần duyệt toàn bộ không gian  
✘ Có thể kẹt nếu không có ngẫu nhiên  

---

### 🟩 Minimax

Minimax là thuật toán tìm kiếm trong cây trò chơi hai người chơi (Max và Min), trong đó:

- Người chơi MAX: cố gắng **tối đa hóa điểm số**
- Người chơi MIN: cố gắng **tối thiểu hóa điểm số**

Thuật toán giả định đối thủ chơi tối ưu.

✔ Tìm được chiến lược tối ưu  
✔ Phù hợp game đối kháng 2 người  
✘ Tốn thời gian với cây lớn  

---

### 🟩 Alpha-Beta Pruning

Alpha-Beta Pruning là tối ưu của Minimax bằng cách **cắt bỏ các nhánh không cần thiết**.

- α (alpha): giá trị tốt nhất của MAX
- β (beta): giá trị tốt nhất của MIN
- Cắt nhánh khi α ≥ β

✔ Giảm số node phải duyệt đáng kể  
✔ Không ảnh hưởng kết quả Minimax  
✔ Tăng tốc độ tìm kiếm  
✘ Hiệu quả phụ thuộc thứ tự duyệt node  

---

### 🟩 Expectimax

Expectimax mở rộng Minimax cho môi trường có yếu tố ngẫu nhiên (randomness).

- MAX node: chọn giá trị tốt nhất
- CHANCE node: tính giá trị kỳ vọng (expected value)

$$
E(n) = \sum P(s) \cdot Value(s)
$$

✔ Xử lý được yếu tố ngẫu nhiên  
✔ Phù hợp game có random (xúc xắc, bài, AI không chắc chắn)  
✘ Không đảm bảo tối ưu tuyệt đối như Minimax  

## 🎯 Tổng quan hệ thống

Dự án mô phỏng và hiện thực hóa các nhóm thuật toán trong Trí Tuệ Nhân Tạo, được tổ chức thành 6 nhóm chính:

- 🔵 **Tìm kiếm mù (Uninformed Search):** BFS, DFS, IDS, UCS  
- 🟡 **Tìm kiếm có thông tin (Informed Search):** Greedy, A*, IDA*  
- 🟢 **Tìm kiếm cục bộ (Local Search):** Hill Climbing, Beam Search, Simulated Annealing  
- 🔴 **CSP (Constraint Satisfaction Problem):** Backtracking, Forward Checking, AC-3, Min-Conflicts  
- 🟣 **Tìm kiếm trong môi trường không chắc chắn:** AND-OR Search, BFS_MTPT  
- ⚫ **Tìm kiếm trong trò chơi (Game Search):** Minimax, Alpha-Beta Pruning, Expectimax  

---

Mỗi nhóm thuật toán được xây dựng nhằm:
- Hiện thực hóa lý thuyết AI vào code
- So sánh đặc điểm giữa các phương pháp
- Quan sát hành vi của agent qua từng bước thực thi
