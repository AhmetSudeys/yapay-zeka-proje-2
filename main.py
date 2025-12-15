import streamlit as st

from config import DEFAULT_ALFA, DEFAULT_BETA, DEFAULT_BUHARLASMA, DEFAULT_KARINCA_SAYISI, DEFAULT_ITERASYON
from data.coordinates import NOKTALAR, NOKTA_ISIMLERI
from core.google_maps import gmaps_client_olustur, mesafe_matrisi_olustur
from core.aco_algorithm import aco_coz
from visual.plotting import yakin_sama_grafigi
from visual.mapping import rota_haritasi_olustur


st.set_page_config(page_title="ACO Yol Optimizasyonu - Senaryo 8", layout="wide")
st.title("Karinca Kolonisi Algoritmasi ile Yol Optimizasyonu (Senaryo 8)")

api_key = st.secrets.get("GOOGLE_MAPS_API_KEY", None)
if not api_key:
    st.error("API key bulunamadi. .streamlit/secrets.toml dosyasini kontrol et.")
    st.stop()

st.subheader("Kullanilan noktalar")
st.write(f"Toplam nokta: {len(NOKTALAR)}")
st.write(NOKTA_ISIMLERI)

st.subheader("ACO parametreleri")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    karinca_sayisi = st.number_input("Karinca sayisi", 5, 300, DEFAULT_KARINCA_SAYISI)
with col2:
    iterasyon = st.number_input("Iterasyon", 10, 500, DEFAULT_ITERASYON)
with col3:
    alfa = st.number_input("Alfa", 0.1, 10.0, DEFAULT_ALFA)
with col4:
    beta = st.number_input("Beta", 0.1, 15.0, DEFAULT_BETA)
with col5:
    buharlas = st.number_input("Buharlas", 0.01, 0.99, DEFAULT_BUHARLASMA)

baslangic_index = st.number_input("Baslangic noktasi index", 0, len(NOKTALAR) - 1, 0)
mode = st.selectbox("Mesafe tipi", ["driving", "walking"], index=0)

# Butona basilmadan once harita/rota gosterilmeyecek (cunku en_iyi_rota yok)
if st.button("Rota Hesapla", type="primary"):

    with st.spinner("Google Maps ile mesafe matrisi aliniyor..."):
        gmaps = gmaps_client_olustur(api_key)
        mesafe_matrisi = mesafe_matrisi_olustur(gmaps, NOKTALAR, mode=mode)

    with st.spinner("ACO calisiyor..."):
        en_iyi_rota, en_iyi_mesafe, en_iyi_tarihce = aco_coz(
            mesafe_matrisi,
            karinca_sayisi=int(karinca_sayisi),
            iterasyon_sayisi=int(iterasyon),
            alfa=float(alfa),
            beta=float(beta),
            buharlas=float(buharlas),
            baslangic_index=int(baslangic_index)
        )

    st.success("Hesaplama tamamlandi.")

    # np.int64 gorunumunu duzeltmek icin normal int'e ceviriyorum
    en_iyi_rota = [int(x) for x in en_iyi_rota]

    st.subheader("Sonuc")
    st.write("En iyi rota (index):", en_iyi_rota)
    st.write("En iyi rota (isim):", [NOKTA_ISIMLERI[i] for i in en_iyi_rota])
    st.write(f"Toplam mesafe: {en_iyi_mesafe/1000:.2f} km")

    st.subheader("Yakinsama grafigi")
    fig = yakin_sama_grafigi(en_iyi_tarihce)
    st.pyplot(fig)

    st.subheader("Harita uzerinde rota")
    deck = rota_haritasi_olustur(en_iyi_rota, NOKTALAR, isimler=NOKTA_ISIMLERI)
    st.pydeck_chart(deck)
