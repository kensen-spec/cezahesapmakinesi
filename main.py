import streamlit as st
from math import floor, ceil

st.set_page_config(
    page_title="CezaHesapMakinesi-Kenan ŞENLİK",
    page_icon="icon.ico",
    layout="centered"
)

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

def hesapla(artis, yil, ay, gun, gun_para, oran, islem_sayaci):
    kesir = kesir_oku(oran)
    if not kesir:
        st.error("Oran geçersiz (örn: 1/6)")
        return yil, ay, gun, gun_para, islem_sayaci, ""
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

    return sonuc_yil, sonuc_ay, sonuc_gun, int(gun_para_sonuc), islem_sayaci, mesaj

# ================= STATE =================

for key in ["yil", "ay", "gun", "gun_para"]:
    if key not in st.session_state:
        st.session_state[key] = 0

if "islem_sayaci" not in st.session_state:
    st.session_state.islem_sayaci = 0
if "sonuclar" not in st.session_state:
    st.session_state.sonuclar = ""

# ================= ARAYÜZ =================

st.title("CezaHesapMakinesi-Kenan ŞENLİK")

yil = st.number_input("Yıl", min_value=0, step=1, key="yil")
ay = st.number_input("Ay", min_value=0, step=1, key="ay")
gun = st.number_input("Gün", min_value=0, step=1, key="gun")
gun_para = st.number_input("Gün Para", min_value=0, step=1, key="gun_para")
oran = st.text_input("Oran", value="1/6")

col1, col2 = st.columns(2)

with col1:
    if st.button("ARTIR", type="primary"):
        y, a, g, gp, st.session_state.islem_sayaci, mesaj = hesapla(
            True, yil, ay, gun, gun_para, oran, st.session_state.islem_sayaci
        )

        st.session_state.yil = y
        st.session_state.ay = a
        st.session_state.gun = g
        st.session_state.gun_para = gp
        st.session_state.sonuclar += mesaj
        st.rerun()

with col2:
    if st.button("İNDİR", type="secondary"):
        y, a, g, gp, st.session_state.islem_sayaci, mesaj = hesapla(
            False, yil, ay, gun, gun_para, oran, st.session_state.islem_sayaci
        )

        st.session_state.yil = y
        st.session_state.ay = a
        st.session_state.gun = g
        st.session_state.gun_para = gp
        st.session_state.sonuclar += mesaj
        st.rerun()

st.subheader(f"İşlem: {st.session_state.islem_sayaci}")
st.text_area("Sonuçlar", value=st.session_state.sonuclar, height=300)
