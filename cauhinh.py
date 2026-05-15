# cauhinh.py

# ======================
# BẢNG MÀU CHỦ ĐẠO (LAM - TRẮNG)
# ======================
COLOR_PRIMARY = "#0078D4"    # Xanh lam đậm (Màu thương hiệu Microsoft/Công nghệ)
COLOR_SIDEBAR = "#FFFFFF"    # Trắng tinh khiết cho thanh công cụ bên trái
COLOR_BG = "#C1DCFF"         # Màu nền chính (Trắng hơi xanh nhẹ để dịu mắt)
COLOR_TEXT = "#333333"       # Màu chữ đen xám (Dễ đọc hơn đen thuần)
COLOR_SUCCESS = "#28a745"    # Xanh lá cây cho các nút "Chạy" hoặc "Hoàn thành"
COLOR_DANGER = "#e53935"     # Đỏ cho nút "Thoát" hoặc "Lỗi"

# ======================
# CẤU HÌNH STYLE CHO NÚT BẤM (BUTTONS)
# ======================
# Style dành cho các nút ở Sidebar (nhỏ gọn hơn)
BTN_STYLE = {
    "fg": "white", 
    "font": ("Arial", 10, "bold"), 
    "relief": "flat",         # Làm phẳng nút theo phong cách hiện đại
    "pady": 7, 
    "cursor": "hand2"         # Hiệu ứng bàn tay khi di chuột vào
}

# Style dành cho các nút ở Trang chủ (lớn và nổi bật hơn)
MAIN_BTN_CFG = {
    "width": 30, 
    "font": ("Arial", 12, "bold"), 
    "fg": "white", 
    "pady": 15, 
    "relief": "flat", 
    "cursor": "hand2"
}