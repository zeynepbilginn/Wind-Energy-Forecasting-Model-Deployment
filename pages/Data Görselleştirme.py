import locale
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import uuid
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Rüzgar Enerjisi Görselleştirmeleri", page_icon="⚡")
st.sidebar.markdown("<div style='position: fixed; top: 0; padding: 20px;'></div>", unsafe_allow_html=True)
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)

@st.cache_data
def get_data():
    dataframe = pd.read_csv("Data/data.csv")
    return dataframe


df = get_data()

col1, col2, col3 = st.columns((1, 4, 1))

df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace=True)

# Normalizasyon işlemi
scaler = MinMaxScaler()
num_cols = ['temperature_2m', 'relativehumidity_2m', 'dewpoint_2m', 'windspeed_10m', 'windspeed_100m',
            'winddirection_10m', 'winddirection_100m', 'windgusts_10m', 'Power']
df_numeric = df[num_cols]
df_numeric.fillna(method='ffill', inplace=True)
df_normalized = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns)
df_normalized['Time'] = df.index
df_normalized.set_index('Time', inplace=True)

# Günlük ortalamaları alalım
daily_means_normalized = df_normalized.resample('D').mean()

# Değişken adlarını Türkçe olarak güncelleme
variable_names = {
    'temperature_2m': 'Sıcaklık',
    'relativehumidity_2m': 'Nem',
    'dewpoint_2m': 'Çiy Noktası',
    'windspeed_10m': 'Rüzgar Hızı (10m)',
    'windspeed_100m': 'Rüzgar Hızı (100m)',
    'winddirection_10m': 'Rüzgar Yönü (10m)',
    'winddirection_100m': 'Rüzgar Yönü (100m)',
    'windgusts_10m': 'Rüzgar Şiddeti (10m)',
    'Power': 'Güç'
}
daily_means_normalized = daily_means_normalized.rename(columns=variable_names)
variable_names_inverse = {v: k for k, v in variable_names.items()}

# Streamlit arayüzü oluşturma
col2.title('Güç Değişkeninin Günlük Ortalamaları ile İlişkili Değişkenler')
col2.write(
    'Zaman içinde Güç değişkeninin günlük ortalama değerleri ile ilişkili diğer değişkenlerin normalleştirilmiş değerlerini gösterir.')

selected_variable = col2.selectbox('Lütfen Güç ile ilişkisini incelemek istediğiniz değişkeni seçin:',
                                   daily_means_normalized.columns.drop('Güç'))


# Grafik oluşturma fonksiyonu
def create_plot(data, x, y, title):
    fig = px.scatter(data_frame=data, x=x, y=y,
                     labels={'x': 'Power', 'y': y},
                     title=title,
                     trendline='ols', color='Güç', hover_name=data.index,
                     color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_xaxes(title_text='Günlük Ortalama Güç')
    fig.update_yaxes(title_text=f'Günlük Ortalama {y}')
    fig.update_traces(marker=dict(size=8, opacity=0.5))
   # fig.update_layout(width=1200, height=500, plot_bgcolor='white')
    return fig


# İlk grafik
col2.plotly_chart(create_plot(daily_means_normalized, 'Güç', selected_variable,
                              f'Power ile {selected_variable} Arasındaki İlişki'))

selectbox1_key = uuid.uuid4().hex
selectbox2_key = uuid.uuid4().hex


def create_plot(data, x, y, title):
    fig = px.scatter(data_frame=data, x=x, y=y,
                     labels={'x': 'Power', 'y': y},
                     title=title,
                     trendline='ols', color='Güç', hover_name=data.index,
                     color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_xaxes(title_text='Günlük Ortalama Güç')
    fig.update_yaxes(title_text=f'Günlük Ortalama {y}')
    fig.update_traces(marker=dict(size=8, opacity=0.5))
    # fig.update_layout(width=1200, height=800)
    return fig


def update_graph(selected_year, selected_month):
    filtered_data = daily_means_normalized[
        (daily_means_normalized.index.year == selected_year) & (daily_means_normalized.index.month == selected_month)]
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(x=filtered_data.index, y=filtered_data['Güç'], mode='lines+markers', name='Günlük Ortalama Güç'))
    fig2.update_layout(title=f'{selected_year} - {selected_month} | Günlük Ortalama Güç', xaxis_title='Tarih',
                       yaxis_title='Günlük Ortalama Güç')
    # fig2.update_layout(width=1200, height=800)
    col2.plotly_chart(fig2, key="second_graph")


turkish_month_names = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık"
}

# locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")

col2.subheader('Yıl ve Ay Seçin (İkinci Grafik)')
selected_year = col2.selectbox('Lütfen bir yıl seçin:', df.index.year.unique(), key="selectbox_year")
selected_month = col2.selectbox('Lütfen bir ay seçin:', range(1, 13), format_func=lambda x: turkish_month_names[x],
                                key="selectbox_month")

# İkinci grafik
update_graph(selected_year, selected_month)


# ------------------------------------

def create_additional_plot(data, selected_variable):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data[selected_variable], mode='markers',
                             name=variable_names_inverse[selected_variable],
                             marker=dict(color='orange', size=8, opacity=0.8),
                             ))
    fig.add_trace(go.Scatter(x=data.index, y=data['Güç'], mode='lines', name='Güç',
                             line=dict(color='green', width=2),
                             ))
    fig.update_layout(title=f'{variable_names_inverse[selected_variable]} ve Güç Arasındaki İlişki',
                      xaxis_title='Tarih',
                      yaxis_title='Değer',
                      # width=1000, height=600,
                      )
    return fig


col2.subheader('Rüzgar Hızı ve Diğer Değişkenler Arasındaki İlişki')

selected_variable_additional = col2.selectbox('Lütfen bir değişken seçin:',
                                              daily_means_normalized.columns.drop(['Güç']))

additional_data = daily_means_normalized[[selected_variable_additional, 'Güç']]

col2.plotly_chart(create_additional_plot(additional_data, selected_variable_additional))
