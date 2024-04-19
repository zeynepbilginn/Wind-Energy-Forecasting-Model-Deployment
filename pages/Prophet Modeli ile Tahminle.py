import contextlib
import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error



@contextlib.contextmanager
def st_progress_bar(title, max_value=100):
    my_bar = st.progress(0)
    yield lambda x: my_bar.progress(x)
    my_bar.empty()

st.set_page_config(page_title="Energy Forecasting with Prophet", page_icon="🔋")
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)

# Veriyi yükleme fonksiyonu
def load_data(filepath):
    with st_progress_bar('Loading Data...') as progress:
        df = pd.read_csv(filepath, parse_dates=['Time'], index_col='Time')
        progress(25)  # Veriyi yükleme tamamlandığında kısmi ilerleme güncellemesi
        df_prophet = df.reset_index().rename(columns={'Time': 'ds', 'Power': 'y'})
        progress(100)  # Veri hazırlığı tamamlandığında tam ilerleme güncellemesi
        return df_prophet

# Prophet modelini eğitme fonksiyonu
def train_model(df_prophet):
    with st_progress_bar('Training Model...') as progress:
        model = Prophet(daily_seasonality=True)
        model.fit(df_prophet)
        progress(100)
        return model

# Tahmin yapma fonksiyonu
def make_predictions(model, periods, freq='H'):
    with st_progress_bar('Making Predictions...') as progress:
        future = model.make_future_dataframe(periods=periods, freq=freq)
        progress(50)
        forecast = model.predict(future)
        progress(100)
        return forecast

# Tahmin verilerini gösterme fonksiyonu
def show_forecast_data(forecast, last_n=5):
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(last_n)

# Streamlit kullanıcı arayüzü
st.title('Prophet ile Enerji Tahmini 🔋')

# Dosya yükleyici
uploaded_file = st.file_uploader("Lütfen Time ve Date sutunlarını içeren verinizi yükleyiniz:")
if uploaded_file is not None:
    df_prophet = load_data(uploaded_file)
    model = train_model(df_prophet)

    periods = st.number_input("Enter the number of hours to predict:", min_value=1, value=24)
    option = st.selectbox("Choose an option:", ['View Forecast and Components', 'View Comparison Plot', 'Calculate MAE',
                                                'Show Forecast Data'])

    if st.button('Show Results'):
        if option == 'View Forecast and Components':
            forecast = make_predictions(model, periods)
            st.pyplot(model.plot(forecast))
            st.pyplot(model.plot_components(forecast))
        elif option == 'View Comparison Plot':
            forecast = make_predictions(model, periods)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df_prophet['ds'], df_prophet['y'], label='Actual Data', color='blue')
            ax.plot(forecast['ds'], forecast['yhat'], label='Forecast', color='red', linestyle='--')
            ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.5)
            ax.set_title('Comparison of Actual Data and Prophet Forecast')
            ax.set_xlabel('Date')
            ax.set_ylabel('Power')
            ax.legend()
            st.pyplot(fig)
        elif option == 'Calculate MAE':
            forecast = make_predictions(model, periods)
            forecast = forecast.set_index('ds')[['yhat']].join(df_prophet.set_index('ds'))
            forecast.dropna(inplace=True)
            mae = mean_absolute_error(forecast['y'], forecast['yhat'])
            st.write(f"The MAE score is: {mae}")
        elif option == 'Show Forecast Data':
            forecast = make_predictions(model, periods)
            st.dataframe(show_forecast_data(forecast, periods))
