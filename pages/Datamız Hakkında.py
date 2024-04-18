import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Rüzgar Enerjisi",page_icon = "⚡")
st.sidebar.markdown("<div style='position: fixed; top: 0; padding: 20px;'></div>", unsafe_allow_html=True)
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)


@st.cache_data
def load_data():
    data = pd.read_csv('Data/data.csv')
    return data

data = load_data()

st.title("Rüzgar Enerjisi Üretimi Veri Seti Analizi")

st.write("""
Bu uygulama, rüzgar enerjisi üretim veri setinin analizini yapmak için tasarlanmıştır.
""")
st.write("İşte veri setinin ilk 10 satırı:")
if data is not None:
    st.write(data.head(10))
st.write("## Veri Seti Özeti")
st.write("Bu veri seti, rüzgar enerjisi üretimine ilişkin saatlik gözlemleri içerir. Temel değişkenler arasında zaman, sıcaklık, nem, rüzgar hızı ve güç üretimi bulunmaktadır.")

# Grafik seçimi
options = ['Sıcaklık', 'Nem', 'Rüzgar Hızı', 'Güç Üretimi', 'Sıcaklık Dağılımı', 'Rüzgar Hızı Dağılımı']
selected_option = st.sidebar.selectbox('Grafik Seçin:', options)

st.title("Veri Seti Açıklaması")
st.write("""
Şirketimizin operasyonel sahalarından doğrudan toplanan saha tabanlı meteorolojik gözlemler ve rüzgar enerjisi üretim verilerinin benzersiz bir derlemesi olan bu veri seti, 2 Ocak 2017'den itibaren detaylı bir saatlik kaydı temsil eder. Zengin içeriğiyle çeşitli hava koşulları ile rüzgar enerjisi üretimi arasındaki ilişkiyi gerçek dünya örnekleriyle sunarak, endüstriye özgü araştırmalar, operasyonel optimizasyon ve akademik çalışmalar için önemli bir kaynak oluşturmayı hedefler.""")

# Kolon Adları ve Açıklamaları
st.header("Kolon Adları ve Açıklamaları")

# Tablo oluşturma
columns = st.columns(2)

with columns[0]:
    with st.expander("Sıcaklık (temperature_2m)"):
        st.write("Sıcaklık sütunu, hava sıcaklığını Celsius derece cinsinden temsil eder.")

    with st.expander("Nem (relativehumidity_2m)"):
        st.write("""
        Nem sütunu, hava nemini yüzde olarak temsil eder.
        """)

    with st.expander("Rüzgar Yönü (winddirection_10m)"):
        st.write("""
        Rüzgar yönü sütunu, rüzgarın 10 metre yükseklikteki yönünü derece cinsinden temsil eder.
        """)

    with st.expander("Rüzgar Şiddeti (windgusts_10m)"):
        st.write("""
        Rüzgar şiddeti sütunu, rüzgarın 10 metre yükseklikteki şiddetini metre/saniye cinsinden temsil eder.
        """)

with columns[1]:
    with st.expander("Çiy Noktası (dewpoint_2m)"):
        st.write("""
        Çiy noktası sütunu, hava çiy noktasını Celsius derece cinsinden temsil eder.
        """)

    with st.expander("Rüzgar Hızı (windspeed_10m)"):
        st.write("""
        Rüzgar hızı sütunu, rüzgarın 10 metre yükseklikteki hızını metre/saniye cinsinden temsil eder.
        """)

    with st.expander("Güç Üretimi (Power)"):
        st.write("""
        Güç üretimi sütunu, rüzgar enerjisi üretimini MW cinsinden temsil eder.
        """)

    with st.expander("Konum (Location)"):
        st.write("""
        Konum sütunu, ölçümün yapıldığı konumu temsil eder.
        """)


# Grafik oluşturma
if selected_option == 'Sıcaklık':
    fig = px.line(data, x='Time', y='temperature_2m', title='Sıcaklık Değişimi')
    fig.update_xaxes(title_text='Zaman')
    fig.update_yaxes(title_text='Sıcaklık (°C)')
    st.plotly_chart(fig)

elif selected_option == 'Nem':
    fig = px.line(data, x='Time', y='relativehumidity_2m', title='Nem Değişimi')
    fig.update_xaxes(title_text='Zaman')
    fig.update_yaxes(title_text='Nem (%)')
    st.plotly_chart(fig)

elif selected_option == 'Rüzgar Hızı':
    fig = px.line(data, x='Time', y=['windspeed_10m', 'windspeed_100m'], title='Rüzgar Hızı Değişimi')
    fig.update_xaxes(title_text='Zaman')
    fig.update_yaxes(title_text='Rüzgar Hızı (m/s)')
    st.plotly_chart(fig)

elif selected_option == 'Güç Üretimi':
    fig = px.line(data, x='Time', y='Power', title='Güç Üretimi Değişimi')
    fig.update_xaxes(title_text='Zaman')
    fig.update_yaxes(title_text='Güç (MW)')
    st.plotly_chart(fig)

elif selected_option == 'Sıcaklık Dağılımı':
    fig = px.histogram(data, x='temperature_2m', title='Sıcaklık Dağılımı')
    fig.update_xaxes(title_text='Sıcaklık (°C)')
    fig.update_yaxes(title_text='Frekans')
    st.plotly_chart(fig)

else:
    fig = px.histogram(data, x='windspeed_10m', title='Rüzgar Hızı Dağılımı')
    fig.update_xaxes(title_text='Rüzgar Hızı (m/s)')
    fig.update_yaxes(title_text='Frekans')
    st.plotly_chart(fig)
