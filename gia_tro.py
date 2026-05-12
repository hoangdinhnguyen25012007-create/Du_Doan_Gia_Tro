import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import os
import folium
from folium.plugins import HeatMap
import numpy as np

class LinearRegressionModel:
    def __init__(self):
        self.intercept = 0.5
        self.coef_dien_tich = 0.08
        self.coef_kc_truong = -0.05
        self.coef_so_nguoi = 0.15
        
        self.coef_phuong = {
            "Linh Trung (Thủ Đức)": 0.0,
            "Linh Chiểu (Thủ Đức)": 0.1,
            "Hiệp Bình Chánh (Thủ Đức)": -0.1,
            "Tam Bình (Thủ Đức)": 0.05,
            "Bình Thọ (Thủ Đức)": 0.2,
            "Phường 14 (Bình Thạnh)": 0.3,
            "Phường 25 (Bình Thạnh)": 0.25,
            "Phường 12 (Gò Vấp)": 0.15,
            "Phường 9 (Phú Nhuận)": 0.4,
        }
        
        self.coef_tien_ich = {
            "may_lanh": 0.35,
            "wc_rieng": 0.25,
            "co_bep": 0.15,
            "gio_giac": 0.10,
            "cho_de_xe": 0.10,
            "gan_tien_ich": 0.20,
        }

    def predict(self, dien_tich, kc_truong, so_nguoi, phuong, tien_ich_dict):
        gia = self.intercept
        gia += self.coef_dien_tich * dien_tich
        gia += self.coef_kc_truong * kc_truong
        gia += self.coef_so_nguoi * so_nguoi
        gia += self.coef_phuong.get(phuong, 0.0)

        for ten, co_hay_khong in tien_ich_dict.items():
            if co_hay_khong:
                gia += self.coef_tien_ich.get(ten, 0)

        return max(0.5, round(gia, 2))

class AppDuDoanGiaPhongTro:
    MAU_NEN = "#F0F4F8"
    MAU_HEADER = "#1A237E"
    MAU_FRAME = "#FFFFFF"
    MAU_NUT_DU_DOAN = "#1565C0"
    MAU_NUT_BAN_DO = "#2E7D32"
    MAU_KET_QUA = "#2E7D32"
    MAU_NHAN = "#37474F"
    MAU_VIEN = "#CFD8DC"

    FONT_TIEU_DE = ("Segoe UI", 18, "bold")
    FONT_PHAN = ("Segoe UI", 11, "bold")
    FONT_NHAN = ("Segoe UI", 10)
    FONT_ENTRY = ("Segoe UI", 10)
    FONT_NUT = ("Segoe UI", 11, "bold")
    FONT_KET_QUA = ("Segoe UI", 14, "bold")

    DANH_SACH_PHUONG = [
        "Linh Trung (Thủ Đức)", "Linh Chiểu (Thủ Đức)", "Hiệp Bình Chánh (Thủ Đức)",
        "Tam Bình (Thủ Đức)", "Bình Thọ (Thủ Đức)", "Phường 14 (Bình Thạnh)",
        "Phường 25 (Bình Thạnh)", "Phường 12 (Gò Vấp)", "Phường 9 (Phú Nhuận)",
    ]

    def __init__(self, root):
        self.root = root
        self.mo_hinh = LinearRegressionModel()
        self._cai_dat_cua_so()
        self._tao_giao_dien()

    def _cai_dat_cua_so(self):
        self.root.title("🏠 Dự Đoán Giá Phòng Trọ Sinh Viên")
        self.root.geometry("680x750")
        self.root.resizable(False, False)
        self.root.configure(bg=self.MAU_NEN)
        self.root.eval('tk::PlaceWindow . center')

    def _tao_giao_dien(self):
        frame_tieu_de = tk.Frame(self.root, bg=self.MAU_HEADER, pady=18)
        frame_tieu_de.pack(fill="x")

        tk.Label(frame_tieu_de, text="🏠 Dự Đoán Giá Phòng Trọ Sinh Viên", font=self.FONT_TIEU_DE, bg=self.MAU_HEADER, fg="white").pack()
        tk.Label(frame_tieu_de, text="Nhập thông tin phòng trọ để nhận dự đoán giá thuê hàng tháng", font=("Segoe UI", 9), bg=self.MAU_HEADER, fg="#90CAF9").pack()

        frame_noi_dung = tk.Frame(self.root, bg=self.MAU_NEN, padx=24, pady=16)
        frame_noi_dung.pack(fill="both", expand=True)

        self._tao_khung_thong_tin_co_ban(frame_noi_dung)
        self._tao_khung_tien_ich(frame_noi_dung)
        self._tao_khung_nut(frame_noi_dung)
        self._tao_khung_ket_qua(frame_noi_dung)

    def _tao_khung_thong_tin_co_ban(self, parent):
        khung = self._tao_khung_vien(parent, "📋  Thông Tin Phòng Trọ")
        khung.columnconfigure(0, weight=1)
        khung.columnconfigure(2, weight=1)

        tk.Label(khung, text="Diện tích (m²):", **self._style_nhan()).grid(row=0, column=0, sticky="w", pady=6)
        self.entry_dien_tich = ttk.Entry(khung, font=self.FONT_ENTRY, width=14)
        self.entry_dien_tich.insert(0, "20")
        self.entry_dien_tich.grid(row=0, column=1, sticky="w", padx=(6, 20), pady=6)

        tk.Label(khung, text="Khoảng cách tới trường (km):", **self._style_nhan()).grid(row=0, column=2, sticky="w", pady=6)
        self.entry_kc_truong = ttk.Entry(khung, font=self.FONT_ENTRY, width=14)
        self.entry_kc_truong.insert(0, "1.5")
        self.entry_kc_truong.grid(row=0, column=3, sticky="w", padx=6, pady=6)

        tk.Label(khung, text="Số người ở tối đa:", **self._style_nhan()).grid(row=1, column=0, sticky="w", pady=6)
        self.entry_so_nguoi = ttk.Entry(khung, font=self.FONT_ENTRY, width=14)
        self.entry_so_nguoi.insert(0, "2")
        self.entry_so_nguoi.grid(row=1, column=1, sticky="w", padx=(6, 20), pady=6)

        tk.Label(khung, text="Phường / Khu vực:", **self._style_nhan()).grid(row=1, column=2, sticky="w", pady=6)
        self.combo_phuong = ttk.Combobox(khung, values=self.DANH_SACH_PHUONG, font=self.FONT_ENTRY, width=22, state="readonly")
        self.combo_phuong.current(0)
        self.combo_phuong.grid(row=1, column=3, sticky="w", padx=6, pady=6)

    def _tao_khung_tien_ich(self, parent):
        khung = self._tao_khung_vien(parent, "✅  Tiện Ích Kèm Theo")
        self.tien_ich_vars = {k: tk.BooleanVar() for k in ["may_lanh", "wc_rieng", "co_bep", "gio_giac", "cho_de_xe", "gan_tien_ich"]}

        danh_sach_tien_ich = [
            ("may_lanh", "❄️  Có máy lạnh"), ("wc_rieng", "🚿  WC riêng"),
            ("co_bep", "🍳  Có bếp nấu"), ("gio_giac", "🕐  Giờ giấc tự do"),
            ("cho_de_xe", "🛵  Chỗ để xe"), ("gan_tien_ich", "🚌  Gần Bus / Siêu thị"),
        ]

        for i, (key, nhan) in enumerate(danh_sach_tien_ich):
            cb = tk.Checkbutton(khung, text=nhan, variable=self.tien_ich_vars[key], font=self.FONT_NHAN, bg=self.MAU_FRAME, fg=self.MAU_NHAN, activebackground=self.MAU_FRAME, selectcolor="#E3F2FD", cursor="hand2")
            cb.grid(row=i // 3, column=i % 3, sticky="w", padx=12, pady=5)

    def _tao_khung_nut(self, parent):
        frame_nut = tk.Frame(parent, bg=self.MAU_NEN, pady=10)
        frame_nut.pack(fill="x")

        btn_du_doan = tk.Button(frame_nut, text="🔍  Dự Đoán Giá Thuê", font=self.FONT_NUT, bg=self.MAU_NUT_DU_DOAN, fg="white", relief="flat", padx=20, pady=10, cursor="hand2", command=self._xu_ly_du_doan)
        btn_du_doan.pack(side="left", expand=True, fill="x", padx=(0, 8))

        btn_ban_do = tk.Button(frame_nut, text="🗺️  Xem Bản Đồ Nhiệt Giá Trọ", font=self.FONT_NUT, bg=self.MAU_NUT_BAN_DO, fg="white", relief="flat", padx=20, pady=10, cursor="hand2", command=self._mo_ban_do_nhiet)
        btn_ban_do.pack(side="left", expand=True, fill="x", padx=(8, 0))

        btn_du_doan.bind("<Enter>", lambda e: btn_du_doan.config(bg="#0D47A1"))
        btn_du_doan.bind("<Leave>", lambda e: btn_du_doan.config(bg=self.MAU_NUT_DU_DOAN))
        btn_ban_do.bind("<Enter>", lambda e: btn_ban_do.config(bg="#1B5E20"))
        btn_ban_do.bind("<Leave>", lambda e: btn_ban_do.config(bg=self.MAU_NUT_BAN_DO))
    def _tao_khung_ket_qua(self, parent):
        khung = self._tao_khung_vien(parent, "📊  Kết Quả Dự Đoán")
        self.lbl_ket_qua = tk.Label(khung, text="— Nhập thông tin và nhấn 'Dự Đoán Giá Thuê' —", font=("Segoe UI", 12), bg=self.MAU_FRAME, fg="#90A4AE")
        self.lbl_ket_qua.pack(pady=10)
        self.lbl_chi_tiet = tk.Label(khung, text="", font=("Segoe UI", 9), bg=self.MAU_FRAME, fg="#78909C", justify="center")
        self.lbl_chi_tiet.pack(pady=(0, 8))
    def _xu_ly_du_doan(self):
        try:
            dien_tich = float(self.entry_dien_tich.get())
            kc_truong = float(self.entry_kc_truong.get())
            so_nguoi = int(self.entry_so_nguoi.get())
            if dien_tich <= 0 or kc_truong < 0 or so_nguoi <= 0: raise ValueError
            
            phuong = self.combo_phuong.get()
            tien_ich_dict = {k: v.get() for k, v in self.tien_ich_vars.items()}
            gia_du_doan = self.mo_hinh.predict(dien_tich, kc_truong, so_nguoi, phuong, tien_ich_dict)

            self.lbl_ket_qua.config(text=f"💰  {gia_du_doan:.2f} triệu đồng / tháng", font=self.FONT_KET_QUA, fg=self.MAU_KET_QUA)
            
            ten_map = {"may_lanh": "Máy lạnh", "wc_rieng": "WC riêng", "co_bep": "Bếp nấu", "gio_giac": "Tự do giờ giấc", "cho_de_xe": "Để xe", "gan_tien_ich": "Gần Bus/Siêu thị"}
            tien_ich_co = [ten_map[k] for k, v in tien_ich_dict.items() if v]
            str_ti = ", ".join(tien_ich_co) if tien_ich_co else "Không có"
            self.lbl_chi_tiet.config(text=f"Diện tích: {dien_tich}m² | Cách trường: {kc_truong}km | {so_nguoi} người | {phuong}\nTiện ích: {str_ti}")
        except:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập đúng định dạng số dương!")
    def _mo_ban_do_nhiet(self):
        ten_file = "heatmap_ueh.html"
    
        if not os.path.exists(ten_file):
            m = folium.Map(location=[10.7626, 106.6602], zoom_start=13)

            data_heatmap = [
                [10.7712, 106.6675, 0.9], 
                [10.7541, 106.6625, 0.9],
                [10.7595, 106.6667, 0.6]
            ]
            HeatMap(data_heatmap, radius=60, blur=35).add_to(m)

            campuses = [
                {"name": "UEH - Cơ sở A", "loc": [10.7823, 106.6944]},
                {"name": "UEH - Cơ sở B", "loc": [10.7610, 106.6675]},
                {"name": "UEH - Cơ sở N", "loc": [10.7126, 106.6661]}
            ]           
            for cp in campuses:
                folium.Marker(
                    location=cp["loc"],
                    popup=cp["name"],
                    icon=folium.Icon(color='red', icon='university', prefix='fa')
                ).add_to(m)
            m.save(ten_file)

        webbrowser.open(f"file:///{os.path.abspath(ten_file)}")
    def _tao_heatmap_mau(self, ten_file):
        noi_dung = """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Bản Đồ Nhiệt</title><style>body{font-family:'Segoe UI',sans-serif;background:#1a1a2e;color:white;display:flex;flex-direction:column;align-items:center;padding:30px;}iframe{border-radius:12px;border:2px solid #37474f;width:900px;height:500px;}</style></head><body><h1>🗺️ Bản Đồ Nhiệt Giá Phòng Trọ</h1><iframe src="https://www.openstreetmap.org/export/embed.html?bbox=106.6,10.75,106.85,10.9&amp;layer=mapnik"></iframe></body></html>"""
        with open(ten_file, "w", encoding="utf-8") as f: f.write(noi_dung)

    def _tao_khung_vien(self, parent, tieu_de):
        lf = tk.LabelFrame(parent, text=f"  {tieu_de}  ", font=self.FONT_PHAN, bg=self.MAU_FRAME, fg=self.MAU_HEADER, bd=1, relief="solid", labelanchor="nw", padx=14, pady=10)
        lf.pack(fill="x", pady=(0, 12))
        return lf

    def _style_nhan(self):
        return {"font": self.FONT_NHAN, "bg": self.MAU_FRAME, "fg": self.MAU_NHAN}
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TEntry", fieldbackground="#FAFAFA", bordercolor="#90CAF9", padding=5)
    style.configure("TCombobox", fieldbackground="#FAFAFA", bordercolor="#90CAF9", padding=5)
    app = AppDuDoanGiaPhongTro(root)
    root.mainloop()