import tkinter as tk
from tkinter import messagebox
from math import floor, ceil

# ================= YARDIMCI =================

def kesir_oku(s):
    s = s.strip()
    if "/" not in s:
        return None
    try:
        pay, payda = s.split("/")
        pay = int(pay)
        payda = int(payda)
        if pay > 0 and payda > 0:
            return pay, payda
    except:
        return None
    return None

def gun_para_hesapla(gun, pay, payda, artis):
    ham = gun * pay / payda
    degisim = floor(ham) if artis else ceil(ham)
    sonuc = gun + degisim if artis else gun - degisim
    return max(0, sonuc)

# ================= HESAPLAMA =================

def hesapla(artis):
    global islem_sayaci

    try:
        yil = int(e_yil.get() or 0)
        ay = int(e_ay.get() or 0)
        gun = int(e_gun.get() or 0)
        gun_para = int(e_gun_para.get() or 0)
    except ValueError:
        messagebox.showerror("Hata", "Sayı alanlarına geçerli değer girin.")
        return

    kesir = kesir_oku(e_oran.get())
    if not kesir:
        messagebox.showerror("Hata", "Oran geçersiz (örn: 1/6)")
        return

    pay, payda = kesir

    sonuc_yil = yil
    sonuc_ay = ay
    sonuc_gun = gun

    tam_yil = (yil // payda) * payda
    kalan_yil = yil - tam_yil
    yil_degisim = (tam_yil // payda) * pay
    sonuc_yil += yil_degisim if artis else -yil_degisim

    ay_yildan_ham = kalan_yil * 12 * pay / payda
    ay_yildan = floor(round(ay_yildan_ham, 6))
    sonuc_ay += ay_yildan if artis else -ay_yildan
    ay_yildan_artik = ay_yildan_ham - ay_yildan

    ay_ham = ay * pay / payda
    ay_degisim = floor(round(ay_ham, 6))
    sonuc_ay += ay_degisim if artis else -ay_degisim
    ay_artik = ay_ham - ay_degisim + ay_yildan_artik

    gun_ham = gun * pay / payda
    gun_artik = ay_artik * 30

    if artis:
        gun_degisim = floor(round(gun_ham, 6)) + floor(round(gun_artik, 6))
    else:
        gun_degisim = ceil(round(gun_ham, 6)) + ceil(round(gun_artik, 6))

    sonuc_gun += gun_degisim if artis else -gun_degisim

    if sonuc_gun < 0:
        ay_eksi = (abs(sonuc_gun) + 29) // 30
        sonuc_ay -= ay_eksi
        sonuc_gun += ay_eksi * 30

    if sonuc_ay < 0:
        yil_eksi = (abs(sonuc_ay) + 11) // 12
        sonuc_yil -= yil_eksi
        sonuc_ay += yil_eksi * 12

    sonuc_yil = max(0, int(sonuc_yil))
    sonuc_ay = max(0, int(sonuc_ay))
    sonuc_gun = max(0, int(sonuc_gun))

    gun_para_sonuc = gun_para_hesapla(gun_para, pay, payda, artis)
    islem_sayaci += 1
    lbl_sayac.config(text=f"İşlem: {islem_sayaci}")

    girilen_list = []
    if yil: girilen_list.append(f"{yil} yıl")
    if ay: girilen_list.append(f"{ay} ay")
    if gun: girilen_list.append(f"{gun} gün")
    girilen_str = " ".join(girilen_list) if girilen_list else "0 gün"

    sonuc_list = []
    if sonuc_yil: sonuc_list.append(f"{sonuc_yil} yıl")
    if sonuc_ay:  sonuc_list.append(f"{sonuc_ay} ay")
    if sonuc_gun: sonuc_list.append(f"{sonuc_gun} gün")
    sonuc_str = " ".join(sonuc_list) if sonuc_list else "0 gün"

    islem_text = "artırıldı" if artis else "indirildi"
    mesaj = f"{girilen_str} {pay}/{payda} oranında {islem_text} → {sonuc_str} yaptı.\n---\n"

    txt_sonuc.config(state="normal")
    txt_sonuc.insert(tk.END, mesaj)
    txt_sonuc.see(tk.END)
    txt_sonuc.config(state="disabled")

    e_yil.delete(0, tk.END); e_yil.insert(0, sonuc_yil)
    e_ay.delete(0, tk.END);  e_ay.insert(0, sonuc_ay)
    e_gun.delete(0, tk.END); e_gun.insert(0, sonuc_gun)
    e_gun_para.delete(0, tk.END); e_gun_para.insert(0, int(gun_para_sonuc))

# ================= GUI =================

root = tk.Tk()

# 🔴 TEK EKLEME: İKON
root.iconbitmap("icon.ico")

root.title("CezaHesapMakinesi-Kenan ŞENLİK")
root.geometry("360x640")
root.resizable(False, False)

def hakkinda():
    messagebox.showinfo("Hakkında", "CezaHesapMakinesi 1.0\nHakim Kenan Şenlik")

menu_bar = tk.Menu(root)
yardim_menu = tk.Menu(menu_bar, tearoff=0)
yardim_menu.add_command(label="Hakkında", command=hakkinda)
menu_bar.add_cascade(label="Yardım", menu=yardim_menu)
root.config(menu=menu_bar)

islem_sayaci = 0

def alan(label, y):
    tk.Label(root, text=label).place(x=20, y=y)
    e = tk.Entry(root)
    e.place(x=140, y=y, width=180, height=28)
    e.insert(0, "0")
    return e

e_yil = alan("Yıl", 30)
e_ay = alan("Ay", 70)
e_gun = alan("Gün", 110)
e_gun_para = alan("Gün Para", 150)

tk.Label(root, text="Oran").place(x=20, y=190)
e_oran = tk.Entry(root)
e_oran.place(x=140, y=190, width=180, height=28)
e_oran.insert(0, "1/6")

btn_artir = tk.Button(root, text="ARTIR", height=2, bg="#ef5350", command=lambda: hesapla(True))
btn_indir = tk.Button(root, text="İNDİR", height=2, bg="#66bb6a", command=lambda: hesapla(False))

btn_artir.place(x=20, y=240, width=140)
btn_indir.place(x=180, y=240, width=140)

frame = tk.Frame(root)
frame.place(x=20, y=310, width=320, height=260)
scroll_y = tk.Scrollbar(frame, orient="vertical")
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
txt_sonuc = tk.Text(frame, state="disabled", wrap="none", yscrollcommand=scroll_y.set)
txt_sonuc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_y.config(command=txt_sonuc.yview)

lbl_sayac = tk.Label(root, text="İşlem: 0", relief="solid", padx=5)
lbl_sayac.place(x=300, y=5)

root.mainloop()
