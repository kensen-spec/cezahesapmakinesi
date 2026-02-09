import streamlit as st
from math import floor, ceil
from PIL import Image
import os

# ================= 1. SAYFA AYARLARI =================
icon_yolu = "icon.ico" 

if os.path.exists(icon_yolu):
    try:
        img = Image.open(icon_yolu)
        st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon=img, layout="centered")
    except:
        st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon="⚖️")
else:
    st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon="⚖️")

# ================= 2. FONKSİYONLAR =================
def kesir_oku(s):
    s = s.strip()
    if "/" not in s: return None
    try:
        pay, payda = s.split("/")
        return int(pay), int(payda)
    except: return None

def gun_para_hesapla(gun, pay, payda, artis):
    ham = gun * pay / payda
    degisim = floor(ham) if artis else ceil(ham)
    sonuc = gun + degisim if artis else gun - degisim
    return max(0, sonuc)

# ================= 3. LOGO VE BAŞLIK =================
if os.path.exists(icon_yolu):
    col_logo, col_text = st.columns([1, 4], vertical_alignment="center") 
    with col_logo:
        st.image(icon_yolu, width=100)
    with col_text:
        st.markdown("<h1 style='margin:0;'>Ceza Hesap Makinesi</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0; color: gray;'>Hakim Kenan Şenlik</h3>", unsafe_allow_html=True)
else:
    st.title("⚖️ Ceza Hesap Makinesi")
    st.subheader("Hakim Kenan Şenlik")

st.write("---")

# ================= 4. SESSION STATE (HAFIZA) AYARI =================
# Butona basıldığını hafızada tutmak için bu kısmı ekledik
if 'hesapla_durumu' not in st.session_state:
    st.session_state.hesapla_durumu = None

# ================= 5. GİRİŞ ALANLARI =================
col1, col2 = st.columns(2)
with col1:
    yil = st.number_input("Yıl", min_value=0, step=1, key="yil_input")
    ay = st.number_input("Ay", min_value=0, max_value=11, step=1, key="ay_input")
with col2:
    gun = st.number_input("Gün", min_value=0, max_value=29, step=1, key="gun_input")
    gun_para = st.number_input("Günlük Adli Para (₺)", min_value=0, step=1, key="para_input")

oran_str = st.text_input("Uygulanacak Oran (Örn: 1/6, 1/2)", value="1/6", key="oran_input")

st.write("")
c1, c2, c3 = st.columns([1, 1, 1])

# Butonlara basıldığında hafızayı güncelliyoruz
if c1.button("🛑 CEZAYI ARTIR", use_container_width=True):
    st.session_state.hesapla_durumu = "artir"

if c2.button("✅ CEZAYI İNDİR", use_container_width=True):
    st.session_state.hesapla_durumu = "indir"

if c3.button("🔄 SIFIRLA", use_container_width=True):
    st.session_state.hesapla_durumu = None
    st.rerun() # Sayfayı temizler

# ================= 6. HESAPLAMA MANTIĞI =================
if st.session_state.hesapla_durumu:
    kesir = kesir_oku(oran_str)
    if not kesir:
        st.error("Lütfen geçerli bir oran girin (Örn: 1/6)")
    else:
        pay, payda = kesir
        artis_mi = True if st.session_state.hesapla_durumu == "artir" else False
        
        sonuc_yil, sonuc_ay, sonuc_gun = yil, ay, gun
        
        # Matematiksel Hesaplama (Önceki kodunuzla aynı mantık)
        tam_yil = (yil // payda) * payda
        kalan_yil = yil - tam_yil
        yil_degisim = (tam_yil // payda) * pay
        sonuc_yil += yil_degisim if artis_mi else -yil_degisim
        ay_yildan_ham = kalan_yil * 12 * pay / payda
        ay_yildan = floor(round(ay_yildan_ham, 6))
        sonuc_ay += ay_yildan if artis_mi else -ay_yildan
        ay_yildan_artik = ay_yildan_ham - ay_yildan
        ay_ham = ay * pay / payda
        ay_degisim = floor(round(ay_ham, 6))
        sonuc_ay += ay_degisim if artis_mi else -ay_degisim
        ay_artik = ay_ham - ay_degisim + ay_yildan_artik
        gun_ham = gun * pay / payda
        gun_artik = ay_artik * 30
        if artis_mi:
            gun_degisim = floor(round(gun_ham, 6)) + floor(round(gun_artik, 6))
        else:
            gun_degisim = ceil(round(gun_ham, 6)) + ceil(round(gun_artik, 6))
        sonuc_gun += gun_degisim if artis_mi else -gun_degisim

        if sonuc_gun < 0:
            ay_eksi = (abs(sonuc_gun) + 29) // 30
            sonuc_ay -= ay_eksi
            sonuc_gun += ay_eksi * 30
        if sonuc_ay < 0:
            yil_eksi = (abs(sonuc_ay) + 11) // 12
            sonuc_yil -= yil_eksi
            sonuc_ay += yil_eksi * 12

        # Sonuç Ekranı
        st.divider()
        st.info(f"### 📋 {'Artırım' if artis_mi else 'İndirim'} Sonucu")
        st.subheader(f"✨ {max(0,int(sonuc_yil))} Yıl, {max(0,int(sonuc_ay))} Ay, {max(0,int(sonuc_gun))} Gün")
        
        if gun_para > 0:
            para_sonuc = gun_para_hesapla(gun_para, pay, payda, artis_mi)
            st.warning(f"💰 **Yeni Günlük Para Cezası:** {int(para_sonuc)} ₺")
