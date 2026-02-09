import streamlit as st
from math import floor, ceil

# Sizin hesaplama fonksiyonlarınız (gun_para_hesapla, kesir_oku vb.) buraya gelecek

st.title("Ceza Hesap Makinesi")
st.subheader("Hakim Kenan Şenlik")

yil = st.number_input("Yıl", min_value=0, value=0)
ay = st.number_input("Ay", min_value=0, value=0)
gun = st.number_input("Gün", min_value=0, value=0)
oran = st.text_input("Oran", value="1/6")

col1, col2 = st.columns(2)
if col1.button("ARTIR"):
    # Hesaplama mantığını burada çalıştırıp st.write ile yazdıracağız
    st.success("Sonuç Artırıldı!")

if col2.button("İNDİR"):
    st.success("Sonuç İndirildi!")
