import streamlit as st
from math import floor, ceil
from PIL import Image
import os

# ================= 1. SAYFA VE İKON AYARLARI =================
icon_yolu = "icon.ico" 
site_url = "https://cezahesapmakinesi.onrender.com"

if os.path.exists(icon_yolu):
    try:
        img = Image.open(icon_yolu)
        st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon=img, layout="centered")
        
        # Hem Android hem iOS ana ekran ikonu için meta etiketleri
        st.markdown(f"""
            <link rel="apple-touch-icon" href="{site_url}/{icon_yolu}">
            <link rel="icon" sizes="192x192" href="{site_url}/{icon_yolu}">
            """, unsafe_allow_html=True)
    except:
        st.set_page_config(page_title="Ceza Hesap Makinesi", layout="centered")
else:
    st.set_page_config(page_title="Ceza Hesap Makinesi", layout="centered")

# ================= 2. BUTON RENKLERİ (CSS) =================
st.markdown("""
    <style>
    /* Artır Butonu - Kırmızı */
    div.stButton > button:first-child {
        background-color: #d32f2f;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= 3. SİZİN FONKSİYONLARINIZ =================
def kesir_oku(s):
    s = s.strip()
    if "/" not in s: return None
    try:
        pay, payda = s.split("/")
        pay, payda = int(pay), int(payda)
        if pay > 0 and payda > 0: return pay, payda
    except: return None
    return None

def gun_para_hesapla(gun, pay, payda, artis):
    ham = gun * pay / payda
    degisim = floor(ham) if artis else ceil(ham)
    sonuc = gun + degisim if artis else gun - degisim
    return max(0, sonuc)

# ================= 4. HAFIZA (ZİNCİRLEME İŞLEM) =================
if 'yil' not in st.session_state: st.session_state.yil = 0
if 'ay' not in st.session_state: st.session_state.ay = 0
if 'gun' not in st.session_state: st.session_state.gun = 0
if 'para' not in st.session_state: st.session_state.para = 0

# ================= 5. ARAYÜZ (LOGONUN SAĞINDA YAZI) =================
if os.path.exists(icon_yolu):
    col_logo, col_text = st.columns([1, 4], vertical_alignment="center") 
    with col_logo:
        st.image(icon_yolu, width=100)
    with col_text:
        st.markdown("<h1 style='margin:0;'>Ceza Hesap Makinesi</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; color: gray;'>Hakim Kenan Şenlik</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h1>Ceza Hesap Makinesi</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: gray;'>Hakim Kenan Şenlik</h3>", unsafe_allow_html=True)

st.write("---")

# ================= 6. GİRİŞ ALANLARI =================
c1, c2, c3, c4 = st.columns(4)
with c1: e_yil = st.number_input("Yıl", value=int(st.session_state.yil), step=1)
with c2: e_ay = st.number_input("Ay", value=int(st.session_state.ay), step=1)
with c3: e_gun = st.number_input("Gün", value=int(st.session_state.gun), step=1)
with c4: e_gun_para = st.number_input("Para", value=int(st.session_state.para), step=1)

e_oran = st.text_input("Oran (Örn: 1/6)", value="1/6")

# ================= 7. HESAPLA (MANTIĞINIZ KORUNDU) =================
def hesapla(artis):
    kesir = kesir_oku(e_oran)
    if not kesir:
        st.error("Oran geçersiz")
        return

    pay, payda = kesir
    yil, ay, gun = e_yil, e_ay, e_gun
    sonuc_yil, sonuc_ay, sonuc_gun = yil, ay, gun

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

    # Hafızayı Güncelle (Kutucuklara yansıması için)
    st.session_state.yil = max(0, int(sonuc_yil))
    st.session_state.ay = max(0, int(sonuc_ay))
    st.session_state.gun = max(0, int(sonuc_gun))
    st.session_state.para = int(gun_para_hesapla(e_gun_para, pay, payda, artis))
    st.rerun()

# BUTONLAR
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("ARTIR", use_container_width=True): hesapla(True)
with col_btn2:
    if st.button("İNDİR", use_container_width=True, type="primary"): hesapla(False)
with col_btn3:
    if st.button("SIFIRLA", use_container_width=True):
        st.session_state.yil = 0
        st.session_state.ay = 0
        st.session_state.gun = 0
        st.session_state.para = 0
        st.rerun()
