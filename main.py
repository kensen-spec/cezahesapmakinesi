import streamlit as st
from math import floor, ceil
from PIL import Image
import os

# ================= 1. SAYFA VE İKON AYARLARI =================
icon_yolu = "icon.ico" 

if os.path.exists(icon_yolu):
    try:
        img = Image.open(icon_yolu)
        st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon=img, layout="centered")
    except:
        st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon="")
else:
    st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon="")

# ================= 2. FONKSİYONLAR (Orijinal Mantığınız) =================
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

# ================= 3. HAFIZA SİSTEMİ (Tkinter'deki gibi çalışma) =================
# Bu kısım, kutucuklardaki rakamların güncellenmesini sağlar
if 'yil' not in st.session_state: st.session_state.yil = 0
if 'ay' not in st.session_state: st.session_state.ay = 0
if 'gun' not in st.session_state: st.session_state.gun = 0
if 'para' not in st.session_state: st.session_state.para = 0
if 'gecmis' not in st.session_state: st.session_state.gecmis = []

# ================= 4. ARAYÜZ (LOGO VE BAŞLIK) =================
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

# ================= 5. GİRİŞ ALANLARI =================
c_yil, c_ay, c_gun, c_para = st.columns(4)

with c_yil:
    yil = st.number_input("Yıl", min_value=0, step=1, key="yil_input", value=st.session_state.yil)
with c_ay:
    ay = st.number_input("Ay", min_value=0, max_value=11, step=1, key="ay_input", value=st.session_state.ay)
with c_gun:
    gun = st.number_input("Gün", min_value=0, max_value=29, step=1, key="gun_input", value=st.session_state.gun)
with c_para:
    para = st.number_input("Para", min_value=0, step=1, key="para_input", value=st.session_state.para)

oran_str = st.text_input("Oran (Örn: 1/6)", value="1/6")

# ================= 6. HESAPLAMA BUTONLARI =================
b1, b2, b3 = st.columns(3)

def hesapla_ve_guncelle(artis_mi):
    kesir = kesir_oku(oran_str)
    if not kesir:
        st.error("Oran hatalı!")
        return
    
    pay, payda = kesir
    # Sizin orijinal matematiksel işlemleriniz
    s_yil, s_ay, s_gun = yil, ay, gun
    tam_yil = (yil // payda) * payda
    kalan_yil = yil - tam_yil
    yil_degisim = (tam_yil // payda) * pay
    s_yil += yil_degisim if artis_mi else -yil_degisim
    ay_yildan_ham = kalan_yil * 12 * pay / payda
    ay_yildan = floor(round(ay_yildan_ham, 6))
    s_ay += ay_yildan if artis_mi else -ay_yildan
    ay_yildan_artik = ay_yildan_ham - ay_yildan
    ay_ham = ay * pay / payda
    ay_degisim = floor(round(ay_ham, 6))
    s_ay += ay_degisim if artis_mi else -ay_degisim
    ay_artik = ay_ham - ay_degisim + ay_yildan_artik
    gun_ham = gun * pay / payda
    gun_artik = ay_artik * 30
    
    if artis_mi:
        gun_degisim = floor(round(gun_ham, 6)) + floor(round(gun_artik, 6))
    else:
        gun_degisim = ceil(round(gun_ham, 6)) + ceil(round(gun_artik, 6))
    
    s_gun += gun_degisim if artis_mi else -gun_degisim
    
    # Dengeleme
    if s_gun < 0:
        ay_eksi = (abs(s_gun) + 29) // 30
        s_ay -= ay_eksi
        s_gun += ay_eksi * 30
    if s_ay < 0:
        yil_eksi = (abs(s_ay) + 11) // 12
        s_yil -= yil_eksi
        s_ay += yil_eksi * 12

    # Yeni değerleri hafızaya al (Böylece kutucuklar güncellenir)
    st.session_state.yil = max(0, int(s_yil))
    st.session_state.ay = max(0, int(s_ay))
    st.session_state.gun = max(0, int(s_gun))
    st.session_state.para = int(gun_para_hesapla(para, pay, payda, artis_mi))
    
    # Geçmişe ekle (Tkinter'deki alttaki liste gibi)
    islem = "Artırım" if artis_mi else "İndirim"
    st.session_state.gecmis.append(f"✅ {pay}/{payda} {islem} → {st.session_state.yil}y {st.session_state.ay}ay {st.session_state.gun}g")
    st.rerun()

if b1.button("🛑 ARTIR", use_container_width=True):
    hesapla_ve_guncelle(True)

if b2.button("✅ İNDİR", use_container_width=True):
    hesapla_ve_guncelle(False)

if b3.button("🔄 SIFIRLA", use_container_width=True):
    st.session_state.yil = 0
    st.session_state.ay = 0
    st.session_state.gun = 0
    st.session_state.para = 0
    st.session_state.gecmis = []
    st.rerun()

# ================= 7. İŞLEM GEÇMİŞİ (Tkinter'deki Liste Alanı) =================
if st.session_state.gecmis:
    st.info("📋 İşlem Geçmişi")
    for satir in reversed(st.session_state.gecmis):
        st.write(satir)

