import streamlit as st
from math import floor, ceil
from PIL import Image
import os

# Sayfa ayarı (Sadece sizin logonuz için)
icon_yolu = "icon.ico"
if os.path.exists(icon_yolu):
    img = Image.open(icon_yolu)
    st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon=img)
else:
    st.set_page_config(page_title="Ceza Hesap Makinesi")

# ================= SİZİN YARDIMCI FONKSİYONLARINIZ (BİREBİR) =================
def kesir_oku(s):
    s = s.strip()
    if "/" not in s: return None
    try:
        pay, payda = s.split("/")
        pay = int(pay)
        payda = int(payda)
        if pay > 0 and payda > 0: return pay, payda
    except: return None
    return None

def gun_para_hesapla(gun, pay, payda, artis):
    ham = gun * pay / payda
    degisim = floor(ham) if artis else ceil(ham)
    sonuc = gun + degisim if artis else gun - degisim
    return max(0, sonuc)

# ================= HAFIZA (ZİNCİRLEME İŞLEM İÇİN) =================
if 'yil' not in st.session_state: st.session_state.yil = 0
if 'ay' not in st.session_state: st.session_state.ay = 0
if 'gun' not in st.session_state: st.session_state.gun = 0
if 'para' not in st.session_state: st.session_state.para = 0

# ================= ARAYÜZ =================
if os.path.exists(icon_yolu):
    col_logo, col_text = st.columns([1, 4], vertical_alignment="center")
    with col_logo: st.image(icon_yolu, width=100)
    with col_text:
        st.markdown(f"<h1>Ceza Hesap Makinesi</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3>Hakim Kenan Şenlik</h3>", unsafe_allow_html=True)

# GİRİŞ ALANLARI (Sizin kodunuzdaki Entry'ler)
e_yil = st.number_input("Yıl", value=int(st.session_state.yil), step=1)
e_ay = st.number_input("Ay", value=int(st.session_state.ay), step=1)
e_gun = st.number_input("Gün", value=int(st.session_state.gun), step=1)
e_gun_para = st.number_input("Gün Para", value=int(st.session_state.para), step=1)
e_oran = st.text_input("Oran", value="1/6")

# ================= HESAPLA FONKSİYONU (SİZİN MANTIĞINIZ) =================
def hesapla(artis):
    kesir = kesir_oku(e_oran)
    if not kesir:
        st.error("Oran geçersiz")
        return

    pay, payda = kesir
    yil, ay, gun = e_yil, e_ay, e_gun
    
    sonuc_yil, sonuc_ay, sonuc_gun = yil, ay, gun

    # SİZİN ORİJİNAL MANTIĞINIZ (BİREBİR KOPYALANDI)
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

    # Kutucukları güncellemek için hafızaya yaz
    st.session_state.yil = max(0, int(sonuc_yil))
    st.session_state.ay = max(0, int(sonuc_ay))
    st.session_state.gun = max(0, int(sonuc_gun))
    st.session_state.para = int(gun_para_hesapla(e_gun_para, pay, payda, artis))
    st.rerun()

# BUTONLAR
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("ARTIR", use_container_width=True, type="secondary"): hesapla(True)
with col_btn2:
    if st.button("İNDİR", use_container_width=True, type="primary"): hesapla(False)

if st.button("SIFIRLA"):
    st.session_state.yil = 0
    st.session_state.ay = 0
    st.session_state.gun = 0
    st.session_state.para = 0
    st.rerun()
