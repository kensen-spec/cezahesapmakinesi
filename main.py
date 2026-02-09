import streamlit as st
from math import floor, ceil
from PIL import Image

# ================= HESAPLAMA =================

def kesir_oku(s):
    try:
        a, b = s.split("/")
        return int(a), int(b)
    except:
        return None

def gun_para_hesapla(gun, pay, payda, artis):
    ham = gun * pay / payda
    degisim = floor(ham) if artis else ceil(ham)
    return max(0, gun + degisim if artis else gun - degisim)

def hesapla(yil, ay, gun, gun_para, oran, artis):
    k = kesir_oku(oran)
    if not k:
        return None, "Oran hatalı (örn: 1/6)"

    pay, payda = k

    sonuc_yil = yil + (yil * pay // payda if artis else -(yil * pay // payda))
    sonuc_ay = ay + (ay * pay // payda if artis else -(ay * pay // payda))
    sonuc_gun = gun + (gun * pay // payda if artis else -(gun * pay // payda))

    gun_para_sonuc = gun_para_hesapla(gun_para, pay, payda, artis)

    return (
        f"{yil} yıl {ay} ay {gun} gün → "
        f"{max(0,sonuc_yil)} yıl {max(0,sonuc_ay)} ay {max(0,sonuc_gun)} gün",
        None
    )

# ================= SAYFA AYARI =================

st.set_page_config(
    page_title="Ceza Hesaplama",
    page_icon="icon.png",
    layout="centered"
)

# ================= GİRİŞ SAYACI =================

if "ziyaret" not in st.session_state:
    st.session_state.ziyaret = 0

st.session_state.ziyaret += 1

# ================= BAŞLIK =================

icon = Image.open("icon.png")
st.image(icon, width=90)
st.caption("Kenan Şenlik")

st.divider()

# ================= FORM =================

yil = st.number_input("Yıl", min_value=0, step=1)
ay = st.number_input("Ay", min_value=0, step=1)
gun = st.number_input("Gün", min_value=0, step=1)
gun_para = st.number_input("Gün Para", min_value=0, step=1)
oran = st.text_input("Oran", "1/6")

if "log" not in st.session_state:
    st.session_state.log = []

c1, c2 = st.columns(2)

with c1:
    if st.button("ARTIR", use_container_width=True):
        msg, hata = hesapla(yil, ay, gun, gun_para, oran, True)
        if hata:
            st.error(hata)
        else:
            st.session_state.log.append(msg)

with c2:
    if st.button("İNDİR", use_container_width=True):
        msg, hata = hesapla(yil, ay, gun, gun_para, oran, False)
        if hata:
            st.error(hata)
        else:
            st.session_state.log.append(msg)

st.divider()

for m in reversed(st.session_state.log):
    st.write(m)

# ================= SAYAÇ (EN ALT) =================

st.divider()
st.markdown(
    f"""
    <div style="text-align:center; font-size:18px; opacity:0.8;">
    🔢 Bu oturumda görüntülenme: <b>{st.session_state.ziyaret}</b>
    </div>
    """,
    unsafe_allow_html=True
)
