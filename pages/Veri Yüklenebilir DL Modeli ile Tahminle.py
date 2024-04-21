import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
st.set_page_config(page_title="Energy Forecasting with LSTM", page_icon="🔋")
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)

def load_and_preprocess_data(uploaded_file):
    df = pd.read_csv(uploaded_file, parse_dates=['Time'], index_col='Time')
    df = df.resample('H').mean().ffill()
    return df

def create_dataset(data, look_back=1):
    X, Y = [], []
    for i in range(len(data) - look_back - 1):
        a = data[i:(i + look_back)]
        X.append(a)
        Y.append(data[i + look_back])
    return np.array(X), np.array(Y)

def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, input_shape=(input_shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_future_hours(model, scaler, data, look_back, hours):
    last_known_data = data[-look_back:]
    predictions = []
    for _ in range(hours):
        x_input = last_known_data.reshape((1, look_back, 1))
        y_hat = model.predict(x_input)[0][0]
        predictions.append(y_hat)
        last_known_data = np.append(last_known_data[1:], y_hat)
    predictions = np.array(predictions).reshape(-1, 1)
    return scaler.inverse_transform(predictions)


def main():
    st.title('LSTM Modeli ile Enerji Tahmini 🔋')

    uploaded_file = st.file_uploader("Lütfen 'Time' ve 'Power' sutünlarını içeren veriseti yükleyiniz:")
    if uploaded_file is not None:
        df = load_and_preprocess_data(uploaded_file)
        st.write(df.head())

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df[['Power']].values)
        look_back = st.slider('Select look back period', min_value=1, max_value=72, value=24)

        X, Y = create_dataset(scaled_data, look_back)
        X = X.reshape(X.shape[0], X.shape[1], 1)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        model = build_model(X_train.shape)

        if st.button('Train Model'):
            with st.spinner('Training model...'):
                history = model.fit(X_train, Y_train, epochs=20, batch_size=1, verbose=1)
            st.success('Model trained successfully!')
            st.line_chart(history.history['loss'])

        if st.button('Predict'):
            train_predict = model.predict(X_train)
            test_predict = model.predict(X_test)
            train_predict = scaler.inverse_transform(train_predict)
            test_predict = scaler.inverse_transform(test_predict)

            fig, ax = plt.subplots()
            ax.plot(df.index[-len(Y_test):], scaler.inverse_transform(Y_test), label='Actual')
            ax.plot(df.index[-len(test_predict):], test_predict, label='Predicted')
            ax.legend()
            st.pyplot(fig)

            train_mae = mean_absolute_error(scaler.inverse_transform(Y_train), train_predict)
            test_mae = mean_absolute_error(scaler.inverse_transform(Y_test), test_predict)
           # st.write(f"Training MAE: {train_mae}")
           # st.write(f"Test MAE: {test_mae}")

        hours_to_predict = st.number_input("Enter the number of hours to predict:", min_value=1, max_value=48, value=24)
        if st.button('Forecast Future'):
            future_predictions = predict_future_hours(model, scaler, scaled_data[-look_back:], look_back,
                                                      hours_to_predict)
            future_dates = pd.date_range(df.index[-1], periods=hours_to_predict + 1, freq='H')[1:]

            fig, ax = plt.subplots()
            ax.plot(future_dates, future_predictions, label='Future predictions', color='orange', linestyle='--')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.xticks(rotation=45)
            ax.set_title('Future Forecast with LSTM')
            ax.set_xlabel('Time (Hourly)')
            ax.set_ylabel('Power Generation')
            ax.legend()
            st.pyplot(fig)



if __name__ == '__main__':
    main()

