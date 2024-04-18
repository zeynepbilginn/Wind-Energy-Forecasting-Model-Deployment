import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

import contextlib
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

st.set_page_config(page_title="Energy Forecasting with XgBoost", page_icon="🔋")

st.sidebar.markdown("<div style='position: fixed; top: 0; padding: 20px;'></div>", unsafe_allow_html=True)
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)


class XGBRegressorWithEarlyStopping(XGBRegressor):
    def fit(self, X, y, **kwargs):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        eval_set = [(X_val, y_val)]
        super().fit(X_train, y_train, eval_set=eval_set, early_stopping_rounds=5, verbose=True, **kwargs)
        return self


# Modelin yüklendiği yer
model_path = r'power_forecasting_pipeline7.pkl'
model = joblib.load(model_path)


def create_features(df):
    df['temperature_2m'] = np.random.normal(loc=20, scale=5, size=len(df))
    df['relativehumidity_2m'] = np.random.normal(loc=70, scale=10, size=len(df))
    df['dewpoint_2m'] = np.random.normal(loc=10, scale=3, size=len(df))
    df['windspeed_10m'] = np.random.normal(loc=10, scale=3, size=len(df))  # Dummy data
    df['windspeed_100m'] = np.random.normal(loc=15, scale=5, size=len(df))  # Dummy data
    df['winddirection_10m'] = np.random.choice(range(360), size=len(df))
    df['winddirection_100m'] = np.random.choice(range(360), size=len(df))
    df['windgusts_10m'] = np.random.normal(loc=5, scale=2, size=len(df))  # Dummy data
    return df[['temperature_2m', 'relativehumidity_2m', 'dewpoint_2m', 'windspeed_10m',
               'windspeed_100m', 'winddirection_10m', 'winddirection_100m', 'windgusts_10m']]


def predict_future_hours(start_date, hours):
    start_datetime = pd.to_datetime(start_date)
    future_datetimes = pd.date_range(start=start_datetime, periods=hours + 1, freq='H')[1:]
    future_df = pd.DataFrame(index=future_datetimes)
    future_features = create_features(future_df)
    predictions = model.predict(future_features)
    predictions_df = pd.DataFrame(predictions, index=future_datetimes, columns=['Predicted Power'])
    return predictions_df


st.title('XgBoost ile Enerji Tahmini 🔋')

# Tarih seçme bileşeni ekleme
selected_date = st.date_input('Tahmin için tarih seçin lütfen:', value=datetime.today())

# Saat sayısı giriş bileşeni
hours = st.number_input('Kaç saatlik tahmin istiyorsunuz?', min_value=1, max_value=72, value=24)

if st.button('Tahmin Et'):
    predictions = predict_future_hours(selected_date, hours)
    st.write(predictions)
    st.line_chart(predictions)

    if predictions is not None:

        real_values = pd.Series([0] * len(predictions.index), index=predictions.index)

        # Modelin doğruluğunu hesapla
        mae = mean_absolute_error(real_values, predictions['Predicted Power'])
        st.write(f'Ortalama Mutlak Hata (MAE): {mae}')

# Profit Model
