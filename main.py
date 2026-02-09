import streamlit as st
from math import floor, ceil

# -------------------------------------------------
# SAYFA AYARLARI
# -------------------------------------------------
st.set_page_config(
    page_title="Ceza Hesap Makinesi",
    page_icon="icon.png",
    layout="centered"
)

# -------------------------------------------------
# CSS (BUTON RENKLERİ + GENEL GÖRÜNÜM)
# -------------------------------------------------
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 48px;
    font-size: 17px;
    font-weight: bold;
    border-radius: 6px;
}
button[kind="primary"] {
    background-color: #ef5350;
}
button[kind="secondary"] {
    background-color: #66bb6a;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# BAŞLIK + ICON
# -------------------------------------------------
st.markdown("""
<div style="display:flex; align-items:center; gap:12px;">
    <img src="icon.png" width="48">
    <h2 style="margin:0;">Ceza Hesap Makinesi</h2>
</div>
<p style="margin-top:-6px; color:gray;">Kenan Şenlik</p>
""", unsafe_allow_html=True)

# -------------------------------------------------
# YARDIMCI FONKSİYONLAR (AYNEN KORUNDU)
# -------------------------------------------------
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

# -------------------------------------------------
# GİRİŞ ALANLARI
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    yil = st.number_input("Yıl", min_value=0, step=1)
    ay = st.number_input("Ay", min_value=0, step=1)
    gun = st.number_input("Gün", min_value=0, step=1)

with col2:
    gun_para = st.number_input("Gün Para", min_value=0, step=1)
    oran_str = st.text_input("Oran (örn: 1/6)", value="1/6")

# -------------------------------------------------
# HESAPLAMA
# -------------------------------------------------
def hesapla(artis):
    kesir = kesir_oku(oran_str)
    if not kesir:
        st.error("Oran geçersiz (örn: 1/6)")
        return

    pay, payda = kesir

    sonuc_yil = yil
    sonuc_ay = ay
    sonuc_gun = gun

    # --- ORİJİNAL MANTIK (DOKUNULMADI) ---
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

    st.success(
        f"{yil} yıl {ay} ay {gun} gün → "
        f"{sonuc_yil} yıl {sonuc_ay} ay {sonuc_gun} gün\n\n"
        f"Gün Para Sonucu: {gun_para_sonuc}"
    )

# -------------------------------------------------
# BUTONLAR (YAN YANA – EXE GİBİ)
# -------------------------------------------------
b1, b2 = st.columns(2)

with b1:
    if st.button("▲ ARTIR", type="primary"):
        hesapla(True)

with b2:
    if st.button("▼ İNDİR", type="secondary"):
        hesapla(False)

# -------------------------------------------------
# HAKKINDA
# -------------------------------------------------
with st.sidebar:
    st.info("CezaHesapMakinesi 1.0\n\nHakim Kenan Şenlik")
