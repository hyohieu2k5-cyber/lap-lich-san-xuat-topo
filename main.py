
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from cauhinh import *
from logic import *
from logic import calculate_topo, save_data, load_data, export_to_excel, export_to_word, import_from_file, update_task, delete_task
from datetime import datetime

tasks = []
edges = []
# ==========
# GIAO DIỆN
# ==========
def show_scheduler():
    """Chuyển từ Trang chủ sang giao diện Lập lịch"""
    home_frame.pack_forget()
    main_interface()

def show_contact():
    messagebox.showinfo("Thông tin liên hệ", 
                        "Người tạo: Lâm Bảo Ngọc Hiếu\n"
                        "MSSV: 0023410958\n\n"
                        "Đồ án: Cài đặt chương trình Lập lịch sản xuất trong nhà máy, ứng dụng giải thuật sắp xếp Tôpô\n"
                        "Sản phẩm: Phần mềm Lập lịch Sản xuất v1.0\n\n"
                        "Email: 0023410958@student.dthu.edu.vn\n"
                        "Hotline: 0969 8345 18\n")

def back_to_home(sidebar, main_content):
    """Quay lại trang chủ"""
    sidebar.pack_forget()
    main_content.pack_forget()
    home_frame.pack(expand=True, fill="both")
# ======================
# LOGIC XỬ LÝ TRONG APP
# ======================
def handle_add_task():
    try:
        t_id = int(entry_id.get())
        t_name = entry_name.get()
        t_time = int(entry_time.get())
        t_priority = int(entry_priority.get())   # 🔥 thêm dòng này
        t_date = cal.get_date().strftime("%d/%m/%Y")

        if any(t['id'] == t_id for t in tasks):
            messagebox.showwarning("Lỗi", "ID đã tồn tại!")
            return

        tasks.append({
            "id": t_id,
            "name": t_name,
            "duration": t_time,
            "date": t_date,
            "priority": t_priority   # 🔥 thêm
        })

        refresh_table()
        clear_form()

    except ValueError:
        messagebox.showerror("Lỗi", "Dữ liệu phải là số!")

def handle_add_relation():
    try:
        u, v = int(entry_id.get()), int(entry_time.get())
        ids = [t['id'] for t in tasks]
        if u in ids and v in ids:
            edges.append((u, v))
            messagebox.showinfo("OK", f"Đã thêm: {u} -> {v}")
        else:
            messagebox.showerror("Lỗi", "ID không tồn tại!")
    except ValueError:
        messagebox.showerror("Lỗi", "Nhập ID trước vào 'ID' và ID sau vào 'Thời gian'")

def handle_topo():
    result = calculate_topo(tasks, edges)

    topo_text.delete("1.0", tk.END)

    if result is None:
        topo_text.insert(tk.END, "LỖI: Có chu trình!")
    else:
        topo_text.insert(tk.END, "THỨ TỰ:\n" + str(result))

def refresh_table():
    for item in tree.get_children(): tree.delete(item)
    for t in tasks: tree.insert("", tk.END, values=(t["id"], t["name"], f"{t['duration']} h", t["date"], t.get("priority", 0)))

def clear_form():
    entry_id.delete(0, tk.END); entry_name.delete(0, tk.END); entry_time.delete(0, tk.END)


def handle_import():
    global tasks
    new_data = import_from_file() # Gọi hàm từ logic.py
    if new_data:
        try:
            standardized_tasks = []
            for item in new_data:
                # Chuẩn hóa: Tự động tìm cột dù viết hoa hay viết thường
                # Lấy ID (chấp nhận cả 'id' hoặc 'ID')
                t_id = item.get('id') if item.get('id') is not None else item.get('ID')
                # Lấy Tên (chấp nhận 'name', 'Name', 'Tên công đoạn'...)
                t_name = item.get('name') or item.get('Name') or item.get('Tên công đoạn')
                # Lấy Thời gian
                t_dur = item.get('duration') or item.get('Duration') or item.get('Thời gian (h)')
                # Lấy Ngày
                t_date = item.get('date') or item.get('Date') or item.get('Ngày thực hiện')
                # Chỉ thêm nếu có ít nhất ID và Tên
                if t_id is not None and t_name:
                    standardized_tasks.append({
                        "id": int(t_id),
                        "name": str(t_name),
                        "duration": int(t_dur) if t_dur else 0,
                        "date": str(t_date) if t_date else "01/01/2026",
                        "priority": int(item.get("priority", 0))
                    })
            if standardized_tasks:
                tasks = standardized_tasks
                refresh_table()
                messagebox.showinfo("Thành công", f"Đã nhập {len(tasks)} công đoạn!")
            else:
                messagebox.showwarning("Lỗi", "Không tìm thấy dữ liệu hợp lệ trong file!")
        except Exception as e:
            messagebox.showerror("Lỗi dữ liệu", f"File không đúng định dạng: {e}")

# ======================
# CHỌN DÒNG TRONG BẢNG
# ======================
def get_selected_task():
    selected = tree.focus()
    if not selected:
        return None
    values = tree.item(selected, "values")
    return int(values[0])

def on_select(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")

    entry_id.delete(0, tk.END)
    entry_id.insert(0, values[0])

    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[1])

    entry_time.delete(0, tk.END)
    entry_time.insert(0, values[2].replace(" h",""))

    entry_priority.delete(0, tk.END)
    if len(values) > 4:
        entry_priority.insert(0, values[4])
    else:
        entry_priority.insert(0, "0")


# ======================
# SỬA
# ======================
def handle_update():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Lỗi", "Chọn công đoạn trước!")
        return

    try:
        values = tree.item(selected, "values")
        selected_id = int(values[0])

        for t in tasks:
            if t["id"] == selected_id:
                if entry_name.get().strip():
                    t["name"] = entry_name.get()

                if entry_time.get().strip():
                    t["duration"] = int(entry_time.get())
                
                if entry_priority.get().strip():
                    t["priority"] = int(entry_priority.get())

                t["date"] = cal.get_date().strftime("%d/%m/%Y")

                # 🔥 UPDATE TRỰC TIẾP TREE
                tree.item(selected, values=(
                    t["id"],
                    t["name"],
                    f"{t['duration']} h",
                    t["date"],
                    t["priority"]
                ))

        messagebox.showinfo("OK", "Đã cập nhật!")

    except ValueError:
        messagebox.showerror("Lỗi", "Thời gian phải là số!")


# ======================
# XÓA
# ======================
def handle_delete():
    selected_id = get_selected_task()
    if selected_id is None:
        messagebox.showwarning("Lỗi", "Chọn công đoạn trước!")
        return

    global tasks

    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?"):
        tasks = [t for t in tasks if t["id"] != selected_id]
        refresh_table()
        clear_form()
        messagebox.showinfo("OK", "Đã xóa!")
          
def show_welcome_screen():
    for widget in root.winfo_children():
        widget.pack_forget()
    home_frame.pack(expand=True, fill="both")


def main_interface():
    # Sidebar
    sidebar = tk.Frame(root, bg=COLOR_SIDEBAR, width=280)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="⚙️ ĐIỀU KHIỂN", font=("Arial", 14, "bold"), bg=COLOR_SIDEBAR, fg=COLOR_PRIMARY).pack(pady=30)
    
    global entry_id, entry_name, entry_time, cal, tree, topo_text, entry_priority
    # (Các ô nhập liệu giữ nguyên như cũ...)
    f = tk.Frame(sidebar, bg=COLOR_SIDEBAR); f.pack(pady=10, padx=20, fill="x")
    tk.Label(f, text="ID:", bg=COLOR_SIDEBAR).pack(anchor="w")
    entry_id = tk.Entry(f, bd=1, relief="solid"); entry_id.pack(fill="x", pady=2)
    tk.Label(f, text="Tên:", bg=COLOR_SIDEBAR).pack(anchor="w")
    entry_name = tk.Entry(f, bd=1, relief="solid"); entry_name.pack(fill="x", pady=2)
    tk.Label(f, text="Thời gian:", bg=COLOR_SIDEBAR).pack(anchor="w")
    entry_time = tk.Entry(f, bd=1, relief="solid"); entry_time.pack(fill="x", pady=2)
    tk.Label(f, text="Ưu tiên:", bg=COLOR_SIDEBAR).pack(anchor="w")
    entry_priority = tk.Entry(f, bd=1, relief="solid"); entry_priority.pack(fill="x", pady=2)
    tk.Label(f, text="Ngày thực hiện:", bg=COLOR_SIDEBAR).pack(anchor="w", pady=(5, 0))
    cal = DateEntry(f, width=12, background='darkblue',
                    foreground='white', borderwidth=2, 
                    date_pattern='dd/mm/yyyy') # Định dạng ngày Việt Nam
    cal.pack(fill="x", pady=5)

    tk.Button(sidebar, text="➕ Thêm công đoạn", command=handle_add_task, bg=COLOR_PRIMARY, **BTN_STYLE).pack(fill="x", padx=20, pady=5)
    tk.Button(sidebar, text="🔗 Thêm quan hệ", command=handle_add_relation, bg="#5c6bc0", **BTN_STYLE).pack(fill="x", padx=20, pady=5)
    tk.Button(sidebar, text="🏭 Chạy lập lịch", command=handle_topo, bg=COLOR_SUCCESS, **BTN_STYLE).pack(fill="x", padx=20, pady=5)
    tk.Button(sidebar, text="✏️ Sửa", command=handle_update, bg="#fb8c00", **BTN_STYLE).pack(fill="x", padx=20, pady=5)
    tk.Button(sidebar, text="❌ Xóa", command=handle_delete, bg="#e53935", **BTN_STYLE).pack(fill="x", padx=20, pady=5)
    
    # ======================
    # TOP BAR
    # ======================
    topbar = tk.Frame(root, bg=COLOR_PRIMARY, height=50)
    topbar.pack(side="top", fill="x")

    tk.Label(topbar, text="📊 LẬP LỊCH SẢN XUẤT", 
         bg=COLOR_PRIMARY, fg="white", 
         font=("Arial", 14, "bold")).pack(side="left", padx=20)

    # Nút bên phải
    btn_frame_top = tk.Frame(topbar, bg=COLOR_PRIMARY)
    btn_frame_top.pack(side="right", padx=10)

    tk.Button(btn_frame_top, text="📘 Hướng dẫn", command=show_guide, bg="#8e24aa", fg="white", padx=10).pack(side="left", padx=5)
    tk.Button(btn_frame_top, text="⬅️ Trang chủ", command=show_welcome_screen, bg="#607d8b", fg="white", padx=10).pack(side="left", padx=5)
    
    # Main Content
    main_content = tk.Frame(root, bg=COLOR_BG)
    main_content.pack(side="right", expand=True, fill="both", padx=20, pady=20)
    
    tree = ttk.Treeview(main_content, columns=("id", "name", "time", "date", "priority"), show="headings")
    tree.heading("id", text="ID"); 
    tree.heading("name", text="Tên"); 
    tree.heading("time", text="Thời gian")
    tree.heading("date", text="Ngày thực hiện")
    tree.heading("priority", text="Ưu tiên")

    tree.column("id", width=50, anchor="center")
    tree.column("name", width=200, anchor="w")
    tree.column("time", width=100, anchor="center")
    tree.column("date", width=120, anchor="center")
    tree.column("priority", width=80, anchor="center")

    tree.pack(expand=True, fill="both")
    tree.bind("<<TreeviewSelect>>", on_select)
    
    # Frame chứa kết quả + scrollbar
    topo_frame = tk.Frame(main_content, bg="white")
    topo_frame.pack(fill="x", pady=10)

    scrollbar = tk.Scrollbar(topo_frame)
    scrollbar.pack(side="right", fill="y")

    topo_text = tk.Text(
        topo_frame,
        height=20,   # 🔥 giữ nguyên chiều cao như cũ
        wrap="word",
        yscrollcommand=scrollbar.set
    )
    topo_text.pack(fill="x")

    scrollbar.config(command=topo_text.yview)

    # Xuất/Nhập file
    file_frame = tk.LabelFrame(sidebar, text="📁 TỆP TIN", bg=COLOR_SIDEBAR, padx=10, pady=10)
    file_frame.pack(fill="x", padx=20, pady=10)

    tk.Button(file_frame, text="📥 Nhập từ Excel", 
              command=lambda: handle_import(), 
              bg="#546e7a", **BTN_STYLE).pack(fill="x", pady=2)

    tk.Button(file_frame, text="📊 Xuất Excel", 
              command=lambda: export_to_excel(tasks), 
              bg="#2e7d32", **BTN_STYLE).pack(fill="x", pady=2)

    tk.Button(file_frame, text="📝 Xuất Word", 
              command=lambda: export_to_word(tasks, topo_text.get("1.0", tk.END)), 
              bg="#1565c0", **BTN_STYLE).pack(fill="x", pady=2)
    

root = tk.Tk()
root.title("Quản lý Lập lịch Sản xuất")
root.geometry("1100x650")
root.configure(bg=COLOR_PRIMARY)
# Khung Trang chủ
home_frame = tk.Frame(root, bg=COLOR_BG)
home_frame.pack(expand=True, fill="both")

tk.Label(home_frame, text="PHẦN MỀM LẬP LỊCH SẢN XUẤT V1.0", 
         font=("Arial", 26, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY).pack(pady=(120, 10))
tk.Label(home_frame, text="Giải pháp tối ưu hóa dây chuyền dựa trên Sắp xếp Tôpô", 
         font=("Arial", 13), bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(0, 60))

# Khung nút bấm chính
btn_container = tk.Frame(home_frame, bg=COLOR_BG)
btn_container.pack()

MAIN_BTN_CFG = {"width": 30, "font": ("Arial", 12, "bold"), "fg": "white", "pady": 15, "relief": "flat", "cursor": "hand2"}

tk.Button(btn_container, text="🚀 BẮT ĐẦU LẬP LỊCH", command=show_scheduler, bg=COLOR_PRIMARY, **MAIN_BTN_CFG).pack(pady=10)
tk.Button(btn_container, text="📞 THÔNG TIN LIÊN HỆ", command=show_contact, bg="#5c6bc0", **MAIN_BTN_CFG).pack(pady=10)
tk.Button(btn_container, text="🚪 THOÁT CHƯƠNG TRÌNH", command=root.quit, bg="#e53935", **MAIN_BTN_CFG).pack(pady=10)
root.mainloop()