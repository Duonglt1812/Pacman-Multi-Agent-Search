## BÁO CÁO BÀI TẬP Q5: HÀM ĐÁNH GIÁ PACMAN

### 1. MÔ TẢ BÀI TOÁN

#### 1.1 Mục tiêu
Thiết kế một hàm đánh giá (evaluation function) tốt hơn cho trò chơi Pacman đa tác tử, giúp Pacman đưa ra quyết định chiến lược về hành động khi sử dụng tìm kiếm Expectimax với độ sâu 2.

#### 1.2 Yêu cầu cụ thể
- **Đánh giá trạng thái** (state evaluation), không phải hành động (action evaluation)
- Pacman phải thắng **ít nhất 50% lần** (≥5 lần trên 10 lần chơi) trên layout `smallClassic`
- Đạt **điểm trung bình ≥1000** khi thắng
- Thời gian thực thi trung bình **<30 giây** mỗi ván
- Không timeout trên autograder

#### 1.3 Tiêu chí chấm điểm

| Tiêu Chí | Điểm | Điều Kiện |
|---------|------|----------|
| Chạy không timeout | 1 | Thắng ≥1 lần |
| Tỉ lệ thắng | 3 | Thắng 10/10 lần |
| Điểm trung bình | 2 | ≥1000 điểm |
| Tốc độ | 1 | <30 giây/ván, thắng ≥5 lần |
| **Tổng điểm** | **6** | |

---

### 2. PHƯƠNG PHÁP

#### 2.1 Cách tiếp cận
Hàm đánh giá được thiết kế dựa trên **kết hợp nhiều yếu tố** để đánh giá chất lượng của một trạng thái trò chơi. Mỗi yếu tố được gán một **trọng số (weight)** phù hợp để cân bằng giữa các mục tiêu:

1. **Ăn thức ăn** - Mục tiêu chính
2. **Tránh xa ghost** - An toàn
3. **Đuổi ghost sợ** - Cơ hội kiếm điểm cao
4. **Ưu tiên power pellets** - Tạo cơ hội

#### 2.2 Chi tiết từng thành phần

##### a. Trạng thái đặc biệt
```
- Nếu thắng: return +∞ (vô cùng dương)
- Nếu thua: return -∞ (vô cùng âm)
```
Đảm bảo Pacman ưu tiên tói đá việc thắng hoặc tránh thua

##### b. Yếu tố thức ăn
```python
if food:
    foodDistances = [manhattanDistance(pos, f) for f in food]
    nearestFood = min(foodDistances)
    
    # Khuyến khích ăn thức ăn gần nhất
    score += 15.0 / (nearestFood + 1)
    
    # Penalize khi còn nhiều thức ăn
    score -= 4 * len(food)
```

**Giải thích:**
- `15.0 / (nearestFood + 1)`: Cộng điểm inversely proportional với khoảng cách
  - Nếu thức ăn ở cách 1 bước: +15/(1+1) = +7.5
  - Nếu thức ăn ở cách 5 bước: +15/(5+1) = +2.5
  - +1 tránh chia cho 0
  
- `4 * len(food)`: Mỗi thức ăn còn lại trừ 4 điểm
  - Starvation penalty: khuyến khích dọn sạch bảng

##### c. Yếu tố điểm đặc biệt (Capsules)
```python
score -= 20 * len(capsules)
```
- Penalize cao (20 điểm) để Pacman ưu tiên ăn capsules
- Capsules cho phép ăn được ghost (tạo cơ hội kiếm 200 điểm)

##### d. Yếu tố Ghost
```python
for ghost in ghosts:
    ghostPos = ghost.getPosition()
    dist = manhattanDistance(pos, ghostPos)
    
    if ghost.scaredTimer > 0:
        # Ghost đang sợ - đuổi để ăn!
        score += 25.0 / (dist + 1)
    else:
        # Ghost bình thường - tránh xa
        if dist <= 1:
            score -= 1000  # Rất nguy hiểm
        else:
            score -= 4.0 / dist  # Tránh xa ghost
```

**Giải thích:**
- **Ghost Scared:** `25.0 / (dist + 1)` - Ăn ghost = 200 điểm, nên phải đuổi tích cực
- **Ghost Bình Thường:**
  - Nếu `dist ≤ 1`: Trừ 1000 điểm (cực kỳ nguy hiểm, gần như mất game)
  - Nếu `dist > 1`: `-4.0 / dist` - Tránh xa ghost nhưng không quá cơn đau


#### 2.3 Chiến lược chọn trọng số

| Yếu Tố | Trọng Số | Lý Do |
|--------|---------|-------|
| Thức ăn gần | +15.0 | Ưu tiên chính |
| Số thức ăn | -4x | Starvation penalty |
| Capsules | -20x | Cao để ưu tiên |
| Ghost scared | +25.0 | Cơ hội kiếm điểm cao |
| Ghost gần | -1000 | Cực kỳ nguy hiểm |
| Ghost xa | -4.0/dist | Tránh xa |

---

### 3. KẾT QUẢ

#### 3.1 Kết quả Autograder

```
=== Test Case: test_cases/q5/grade-agent.test ===
✓ PASSED

Chi Tiết Chấm Điểm (trên 10 ván smallClassic):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1] Không Timeout:           1/1 ✓
    → Chạy không timeout

[2] Tỉ Lệ Thắng:             3/3 ✓
    → Thắng 10/10 lần (yêu cầu: ≥5 lần)

[3] Điểm Trung Bình:         2/2 ✓
    → 1167.2 điểm (yêu cầu: ≥1000)

[4] Tốc Độ Thực Thi:         1/1 ✓
    → <30 giây/ván

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TỔNG ĐIỂM:                  6/6 ✓✓✓
```

#### 3.2 Phân tích kết quả

1. **Tỉ Lệ Thắng 100%** 
   - Pacman thắng 10/10 ván liên tiếp
   - Chỉ cần 50% → Đạt 200% yêu cầu
   - Hàm đánh giá rất hiệu quả

2. **Điểm Trung Bình 1167.2**
   - Vượt mục tiêu (1000 điểm)
   - Chứng tỏ Pacman chơi chiến lược tốt
   - Không chỉ thắng mà còn thắng với điểm cao

3. **Tốc Độ Thực Thi Tốt**
   - Mỗi ván <30 giây
   - Hàm đánh giá đơn giản nên tính toán nhanh
   - Phù hợp với Expectimax depth=2

4. **Không Timeout**
   - Autograder chạy mượt mà
   - Không có vấn đề về hiệu suất

#### 3.3 So sánh với yêu cầu

| Yêu Cầu | Kết Quả | Trạng Thái |
|---------|---------|-----------|
| Thắng ≥50% | 100% (10/10) | Đạt |
| Điểm ≥1000 | 1167.2 | Đạt |
| Tốc độ <30s | <30s | Đạt |
| Không timeout | Đạt | Đạt |
