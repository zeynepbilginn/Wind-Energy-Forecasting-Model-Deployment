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
    my_bar.empty()  # Clear the progress bar

def load_data(filepath):
    with st_progress_bar('Loading Data...') as progress:
        df = pd.read_csv(filepath, parse_dates=['Time'], index_col='Time')
        progress(25)  # Partial progress update after loading data
        df_prophet = df.reset_index().rename(columns={'Time': 'ds', 'Power': 'y'})
        progress(100)  # Complete the progress after data prep
        return df_prophet

def train_model(df_prophet):
    with st_progress_bar('Training Model...') as progress:
        model = Prophet(daily_seasonality=True)
        model.fit(df_prophet)
        progress(100)
        return model


def make_predictions(model, periods, freq='H'):
    with st_progress_bar('Making Predictions...') as progress:
        future = model.make_future_dataframe(periods=periods, freq=freq)
        progress(50)
        forecast = model.predict(future)
        progress(100)
        return forecast


def show_forecast_data(forecast, last_n=5):
    # This will return the specified number of last rows from the forecast DataFrame
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(last_n)


# Streamlit user interface
st.title('Prophet Modeli ile Rüzgar Enerjisi Tahmini')

# File uploader
uploaded_file = st.file_uploader("Lütfen "Time" ve "Power" içeren bir veriseti yükleyiniz:")
if uploaded_file is not None:
    df_prophet = load_data(uploaded_file)
    model = train_model(df_prophet)

    periods = st.number_input("Enter the number of hours to predict:", min_value=1, value=24)
    option = st.selectbox("Choose an option:", [
                                                'Show Forecast Data'])

    if st.button('Show Results'):
        if option == 'Show Forecast Data':
            forecast = make_predictions(model, periods)
            st.dataframe(show_forecast_data(forecast, periods))

#streamlit run strimlit_prophte_pipeline.py
