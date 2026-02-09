import streamlit as st
from fractions import Fraction
from PIL import Image

# --------------------
# Sayfa ayarları
# --------------------
st.set_page_config(
    page_title="Ceza Hesap Makinesi",
    page_icon="icon.png",
    layout="wide"
)

# --------------------
# Sidebar (Hakkında)
# --------------------
st.sidebar.markdown(
    """
    <div style="background:#e3efff;padding:15px;border-radius:10px">
        <strong>CezaHesapMakinesi 1.0</strong><br>
        Hakim Kenan Şenlik
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------
# Üst başlık + ikon
# --------------------
col_icon, col_title = st.columns([1, 10])

with col_icon:
    try:
        img = Image.open("icon.png")
        st.image(img, width=64)
    except:
        pass

with col_title:
    st.markdown("## Ceza Hesap Makinesi")
    st.caption("Kenan Şenlik")

st.divider()

# --------------------
# Giriş alanları
# --------------------
c1, c2 = st.columns(2)

with c1:
    yil = st.number_input("Yıl", min_value=0, step=1, value=0)
    ay = st.number_input("Ay", min_value=0, step=1, value=0)
    gun = st.number_input("Gün", min_value=0, step=1, value=0)

with c2:
    gun_para = st.number_input("Gün Para", min_value=0, step=1, value=0)
    oran_text = st.text_input("Oran (örn: 1/6)", value="1/6")

# --------------------
# Oran çözümleme
# --------------------
try:
    oran = Fraction(oran_text)
except:
    st.error("Oran geçersiz (örn: 1/6)")
    st.stop()

# --------------------
# Hesaplama fonksiyonu
# --------------------
def toplam_gun(y, a, g):
    return y * 365 + a * 30 + g

# --------------------
# Butonlar (yan yana & renkli)
# --------------------
b1, b2 = st.columns(2)

with b1:
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #ef5350;
            color: white;
            height: 50px;
            width: 150px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    artir = st.button("▲ ARTIR")

with b2:
    st.markdown(
        """
        <style>
        div.stButton > button:last-child {
            background-color: #66bb6a;
            color: white;
            height: 50px;
            width: 150px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    indir = st.button("▼ İNDİR")

# --------------------
# Sonuç alanı
# --------------------
if artir or indir:
    toplam = toplam_gun(yil, ay, gun)

    if artir:
        sonuc = toplam + int(toplam * oran)
        st.success(f"Artırılmış gün: {sonuc}")

    if indir:
        sonuc = toplam - int(toplam * oran)
        st.success(f"İndirilmiş gün: {sonuc}")
