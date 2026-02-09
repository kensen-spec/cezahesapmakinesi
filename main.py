import streamlit as st
from math import floor, ceil
from PIL import Image
import os

# ================= 1. SAYFA VE İKON AYARLARI =================
icon_yolu = "icon.png" 
site_url = "https://cezahesapmakinesi.onrender.com"

if os.path.exists(icon_yolu):
    try:
        img = Image.open(icon_yolu)
        st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon=img, layout="centered")
        # Mobil cihazlar için ikon tanıtımı
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
    /* ARTIR Butonu - Kırmızı (#ef5350) */
    div.stButton > button:first-child {
        background-color: #ef5350;
        color: white;
        border: none;
    }
    /* İNDİR Butonu - Yeşil (#66bb6a) */
    .stElementContainer:nth-child(2) div.stButton > button {
        background-color: #66bb6a !important;
        color: white !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= 3. YARDIMCI FONKSİYONLAR (BİREBİR AYNI) =================

def kesir_oku(s):
    s = s.strip()
    if "/" not in s: return None
    try:
        pay, payda = s.split("/")
        pay = int(pay); payda = int(payda)
        if pay > 0 and payda > 0: return pay, payda
    except: return None
    return None

def gun_para_hesapla(gun, pay, payda, artis):
    ham = gun * pay / payda
    degisim = floor(ham) if artis else ceil(ham)
    sonuc = gun + degisim if artis else gun - degisim
    return max(0, sonuc)

# ================= 4. SAYAÇ VE HAFIZA SİSTEMİ =================

if 'log' not in st.session_state: st.session_state.log = []
if 'yil' not in st.session_state: st.session_state.yil = 0
if 'ay' not in st.session_state: st.session_state.ay = 0
if 'gun' not in st.session_state: st.session_state.gun = 0
if 'para' not in st.session_state: st.session_state.para = 0

def ziyaret_sayaci():
    dosya = "ziyaret_sayisi.txt"
    if not os.path.exists(dosya):
        with open(dosya, "w") as f: f.write("0")
    with open(dosya, "r") as f:
        toplam = int(f.read())
    if "sayildi" not in st.session_state:
        toplam += 1
        with open(dosya, "w") as f: f.write(str(toplam))
        st.session_state.sayildi = True
    return toplam

toplam_ziyaret = ziyaret_sayaci()

# ================= 5. ARAYÜZ / BAŞLIK =================

if os.path.exists(icon_yolu):
    col_logo, col_text = st.columns([1, 4], vertical_alignment="center")
    with col_logo:
        st.image(icon_yolu, width=90)
    with col_text:
        st.markdown("<h1 style='margin:0;'>Ceza Hesap Makinesi</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; color: gray;'>Hakim Kenan Şenlik</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h1>Ceza Hesap Makinesi</h1>", unsafe_allow_html=True)
    st.caption("Hakim Kenan Şenlik")

st.write("---")

# ================= 6. GİRİŞ ALANLARI =================

c1, c2, c3, c4 = st.columns(4)
with c1: e_yil = st.number_input("Yıl", value=int(st.session_state.yil), step=1)
with c2: e_ay = st.number_input("Ay", value=int(st.session_state.ay), step=1)
with c3: e_gun = st.number_input("Gün", value=int(st.session_state.gun), step=1)
with c4: e_gun_para = st.number_input("Gün Para", value=int(st.session_state.para), step=1)

e_oran = st.text_input("Oran", value="1/6")

# ================= 7. HESAPLAMA (ORİJİNAL MANTIK) =================

def hesapla_islem(artis):
    kesir = kesir_oku(e_oran)
    if not kesir:
        st.error("Oran geçersiz (örn: 1/6)")
        return

    pay, payda = kesir
    yil, ay, gun, gun_para = e_yil, e_ay, e_gun, e_gun_para
    
    sonuc_yil, sonuc_ay, sonuc_gun = yil, ay, gun

    # Sizin orijinal matematiksel bloklarınız
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

    # Hafızayı ve Sonuçları Güncelle
    st.session_state.yil = max(0, int(sonuc_yil))
    st.session_state.ay = max(0, int(sonuc_ay))
    st.session_state.gun = max(0, int(sonuc_gun))
    st.session_state.para = int(gun_para_hesapla(gun_para, pay, payda, artis))

    # Log mesajını oluştur
    girilen_str = f"{yil}y {ay}ay {gun}g"
    sonuc_str = f"{st.session_state.yil}y {st.session_state.ay}ay {st.session_state.gun}g"
    islem_text = "artırıldı" if artis else "indirildi"
    mesaj = f"✅ {girilen_str} {pay}/{payda} {islem_text} → {sonuc_str}"
    st.session_state.log.append(mesaj)
    st.rerun()

# BUTONLAR
col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("ARTIR", use_container_width=True): hesapla_islem(True)
with col_b2:
    if st.button("İNDİR", use_container_width=True): hesapla_islem(False)

# ================= 8. SONUÇLAR VE SAYAÇ =================
st.write("---")
for m in reversed(st.session_state.log):
    st.write(m)

st.write("---")
st.markdown(f"<p style='text-align:center; opacity:0.6;'>Toplam Ziyaret Sayısı: {toplam_ziyaret}</p>", unsafe_allow_html=True)

if st.button("SIFIRLA"):
    st.session_state.log = []
    st.session_state.yil = 0; st.session_state.ay = 0; st.session_state.gun = 0; st.session_state.para = 0
    st.rerun()
