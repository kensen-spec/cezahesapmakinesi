import streamlit as st
from PIL import Image
from fractions import Fraction
import os

# -------------------------------------------------
# Sayfa ayarları (Render uyumlu)
# -------------------------------------------------
st.set_page_config(
    page_title="Ceza Hesap Makinesi",
    page_icon="⚖️",
    layout="wide"
)

# -------------------------------------------------
# icon yolu (kesin yol – Render/Linux uyumlu)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "icon.png")

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.markdown(
    """
    <div style="background:#e8f0ff;padding:15px;border-radius:10px">
        <strong>Ceza Hesap Makinesi</strong><br>
        Kenan Şenlik
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Başlık + ikon
# -------------------------------------------------
col_icon, col_title = st.columns([1, 12])

with col_icon:
    if os.path.exists(ICON_PATH):
        img = Image.open(ICON_PATH)
        st.image(img, width=60)
    else:
        st.markdown("### ⚖️")

with col_title:
    st.markdown("## Ceza Hesap Makinesi")
    st.caption("Kenan Şenlik")

st.divider()

# -------------------------------------------------
# Girdi alanları
# -------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    yil = st.number_input("Yıl", min_value=0, step=1, value=0)
    ay = st.number_input("Ay", min_value=0, step=1, value=0)
    gun = st.number_input("Gün", min_value=0, step=1, value=0)

with c2:
    gun_para = st.number_input("Gün Para", min_value=0, step=1, value=0)
    oran_text = st.text_input("Oran (örn: 1/6)", value="1/6")

# -------------------------------------------------
# Oran kontrolü
# -------------------------------------------------
try:
    oran = Fraction(oran_text)
except:
    st.error("Oran geçersiz. Örnek: 1/6")
    st.stop()

# -------------------------------------------------
# Hesaplama
# -------------------------------------------------
def toplam_gun(y, a, g):
    return y * 365 + a * 30 + g

# -------------------------------------------------
# Buton stilleri
# -------------------------------------------------
st.markdown(
    """
    <style>
    .artir button {
        background-color: #d32f2f;
        color: white;
        height: 50px;
        width: 160px;
        font-size: 16px;
    }
    .indir button {
        background-color: #388e3c;
        color: white;
        height: 50px;
        width: 160px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Butonlar (YAN YANA)
# -------------------------------------------------
b1, b2 = st.columns(2)

with b1:
    st.markdown('<div class="artir">', unsafe_allow_html=True)
    artir = st.button("▲ ARTIR")
    st.markdown('</div>', unsafe_allow_html=True)

with b2:
    st.markdown('<div class="indir">', unsafe_allow_html=True)
    indir = st.button("▼ İNDİR")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Sonuç
# -------------------------------------------------
if artir or indir:
    toplam = toplam_gun(yil, ay, gun)

    if artir:
        sonuc = toplam + int(toplam * oran)
        st.success(f"Artırılmış ceza süresi: {sonuc} gün")

    if indir:
        sonuc = toplam - int(toplam * oran)
        st.success(f"İndirilmiş ceza süresi: {sonuc} gün")
