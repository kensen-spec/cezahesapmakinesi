import streamlit as st
from math import floor, ceil

# ================= YARDIMCI FONKSİYONLAR =================
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

# ================= STREAMLIT ARAYÜZÜ =================
st.set_page_config(page_title="Ceza Hesap Makinesi", page_icon="⚖️")
st.title("⚖️ Ceza Hesap Makinesi")
st.subheader("Hakim Kenan Şenlik")

col1, col2 = st.columns(2)
with col1:
    yil = st.number_input("Yıl", min_value=0, value=0)
    ay = st.number_input("Ay", min_value=0, value=0)
with col2:
    gun = st.number_input("Gün", min_value=0, value=0)
    gun_para = st.number_input("Gün Para", min_value=0, value=0)

oran_str = st.text_input("Oran (Örn: 1/6)", value="1/6")

c1, c2 = st.columns(2)
artis_durumu = None
if c1.button("🛑 ARTIR", use_container_width=True): artis_durumu = True
if c2.button("✅ İNDİR", use_container_width=True): artis_durumu = False

# ================= HESAPLAMA MANTIĞI =================
if artis_durumu is not None:
    kesir = kesir_oku(oran_str)
    if not kesir:
        st.error("Oran geçersiz!")
    else:
        pay, payda = kesir
        sonuc_yil, sonuc_ay, sonuc_gun = yil, ay, gun
        
        tam_yil = (yil // payda) * payda
        kalan_yil = yil - tam_yil
        yil_degisim = (tam_yil // payda) * pay
        sonuc_yil += yil_degisim if artis_durumu else -yil_degisim

        ay_yildan_ham = kalan_yil * 12 * pay / payda
        ay_yildan = floor(round(ay_yildan_ham, 6))
        sonuc_ay += ay_yildan if artis_durumu else -ay_yildan
        ay_yildan_artik = ay_yildan_ham - ay_yildan

        ay_ham = ay * pay / payda
        ay_degisim = floor(round(ay_ham, 6))
        sonuc_ay += ay_degisim if artis_durumu else -ay_degisim
        ay_artik = ay_ham - ay_degisim + ay_yildan_artik

        gun_ham = gun * pay / payda
        gun_artik = ay_artik * 30

        if artis_durumu:
            gun_degisim = floor(round(gun_ham, 6)) + floor(round(gun_artik, 6))
        else:
            gun_degisim = ceil(round(gun_ham, 6)) + ceil(round(gun_artik, 6))

        sonuc_gun += gun_degisim if artis_durumu else -gun_degisim

        if sonuc_gun < 0:
            ay_eksi = (abs(sonuc_gun) + 29) // 30
            sonuc_ay -= ay_eksi
            sonuc_gun += ay_eksi * 30
        if sonuc_ay < 0:
            yil_eksi = (abs(sonuc_ay) + 11) // 12
            sonuc_yil -= yil_eksi
            sonuc_ay += yil_eksi * 12

        st.divider()
        st.success(f"**Sonuç:** {max(0,int(sonuc_yil))} Yıl, {max(0,int(sonuc_ay))} Ay, {max(0,int(sonuc_gun))} Gün")
        st.info(f"**Gün Para:** {int(gun_para_hesapla(gun_para, pay, payda, artis_durumu))}")
