import streamlit as st
from math import floor, ceil
from PIL import Image
import os

# ================= YARDIMCI (AYNEN) =================

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

# ================= STREAMLIT SETUP =================

st.set_page_config(
    page_title="CezaHesapMakinesi - Kenan Şenlik",
    layout="centered"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "icon.png")

# ================= BAŞLIK =================

col1, col2 = st.columns([1, 8])
with col1:
    if os.path.exists(ICON_PATH):
        st.image(Image.open(ICON_PATH), width=50)
with col2:
    st.markdown("## ⚖️ Ceza Hesap Makinesi")
    st.caption("Kenan Şenlik")

st.divider()

# ================= GİRİŞLER =================

yil = st.number_input("Yıl", min_value=0, step=1, value=0)
ay = st.number_input("Ay", min_value=0, step=1, value=0)
gun = st.number_input("Gün", min_value=0, step=1, value=0)
gun_para = st.number_input("Gün Para", min_value=0, step=1, value=0)
oran_text = st.text_input("Oran (örn: 1/6)", value="1/6")

kesir = kesir_oku(oran_text)
if not kesir:
    st.error("Oran geçersiz (örn: 1/6)")
    st.stop()

pay, payda = kesir

# ================= HESAPLAMA (AYNEN) =================

def hesapla(artis):
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

    return sonuc_yil, sonuc_ay, sonuc_gun, gun_para_sonuc

# ================= BUTONLAR =================

c1, c2 = st.columns(2)

with c1:
    if st.button("ARTIR", use_container_width=True):
        y, a, g, gp = hesapla(True)
        st.success(f"Sonuç: {y} yıl {a} ay {g} gün | Gün Para: {gp}")

with c2:
    if st.button("İNDİR", use_container_width=True):
        y, a, g, gp = hesapla(False)
        st.success(f"Sonuç: {y} yıl {a} ay {g} gün | Gün Para: {gp}")
