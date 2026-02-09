import streamlit as st
from math import floor, ceil

# ================= YARDIMCI (AYNI) =================

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

# ================= STREAMLIT STATE =================

if "islem_sayaci" not in st.session_state:
    st.session_state.islem_sayaci = 0

if "sonuclar" not in st.session_state:
    st.session_state.sonuclar = ""

# ================= HESAPLAMA (AYNI) =================

def hesapla(artis, yil, ay, gun, gun_para, oran):
    kesir = kesir_oku(oran)
    if not kesir:
        return "❌ Oran geçersiz (örn: 1/6)"

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

    st.session_state.islem_sayaci += 1

    girilen = []
    if yil: girilen.append(f"{yil} yıl")
    if ay: girilen.append(f"{ay} ay")
    if gun: girilen.append(f"{gun} gün")
    girilen_str = " ".join(girilen) if girilen else "0 gün"

    sonuc = []
    if sonuc_yil: sonuc.append(f"{sonuc_yil} yıl")
    if sonuc_ay: sonuc.append(f"{sonuc_ay} ay")
    if sonuc_gun: sonuc.append(f"{sonuc_gun} gün")
    sonuc_str = " ".join(sonuc) if sonuc else "0 gün"

    islem_text = "artırıldı" if artis else "indirildi"
    mesaj = f"{girilen_str} {pay}/{payda} oranında {islem_text} → {sonuc_str} yaptı.\n---\n"

    st.session_state.sonuclar += mesaj

    return sonuc_yil, sonuc_ay, sonuc_gun, gun_para_sonuc

# ================= UI =================

st.set_page_config(
    page_title="CezaHesapMakinesi",
    page_icon="icon.png",
    layout="centered"
)

st.markdown("## ⚖️ Ceza Hesap Makinesi")
st.caption("Kenan Şenlik")

yil = st.number_input("Yıl", min_value=0, value=0)
ay = st.number_input("Ay", min_value=0, value=0)
gun = st.number_input("Gün", min_value=0, value=0)
gun_para = st.number_input("Gün Para", min_value=0, value=0)
oran = st.text_input("Oran", value="1/6")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔴 ARTIR"):
        r = hesapla(True, yil, ay, gun, gun_para, oran)
        if isinstance(r, tuple):
            yil, ay, gun, gun_para = r

with col2:
    if st.button("🟢 İNDİR"):
        r = hesapla(False, yil, ay, gun, gun_para, oran)
        if isinstance(r, tuple):
            yil, ay, gun, gun_para = r

st.text_area(
    f"Sonuçlar (İşlem: {st.session_state.islem_sayaci})",
    st.session_state.sonuclar,
    height=260
)
