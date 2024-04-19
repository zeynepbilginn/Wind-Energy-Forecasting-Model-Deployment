import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import Callback
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rüzgar Enerjisi", page_icon="🔋")
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.markdown("<div style='position: fixed; top: 0; padding: 20px;'></div>", unsafe_allow_html=True)
st.sidebar.image("img/BZDAY.jpg", use_column_width=True)

class ProgressCallback(Callback):
    def __init__(self, st_progress_bar):
        super(ProgressCallback, self).__init__()
        self.st_progress_bar = st_progress_bar

    def on_epoch_end(self, epoch, logs=None):
        # Update the progress bar
        self.st_progress_bar.progress((epoch + 1) / self.params['epochs'])

@st.cache_resource()
def load_data():
    dfs = []
    file_paths = [
        "Data/Location1.csv",
        "Data/Location2.csv",
        "Data/Location3.csv",
        "Data/Location4.csv"
    ]
    for file in file_paths:
        df = pd.read_csv(file, parse_dates=[0])
        dfs.append(df)
    df = pd.concat(dfs)
    df.set_index('Time', inplace=True)
    return df

def prepare_data(df):
    y = df['Power'].values
    X = df.drop(['Power'], axis=1).values
    return X, y

def create_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, input_shape=(input_shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# def plot_results(y_test, pred, n_results):
#   plt.figure(figsize=(14, 7))
#    plt.plot(y_test[:n_results], label='Actual', color='blue')
#    plt.plot(pred[:n_results], label='Predicted', color='red')
#    plt.bar(range(n_results), y_test[:n_results] - pred[:, 0][:n_results], label='Difference', color='gray')
#    plt.title('Comparison of Actual and Predicted Values')
#    plt.xlabel('Sample Index')
#    plt.ylabel('Power Output')
#    plt.legend()
#    st.pyplot(plt)

def main():
    st.title('LSTM ile Enerji Tahmini 🔋')

    # LSTM ile ilgili bilgilerin metin kutusunda gösterilmesi
    st.write("""
    Long Short-Term Memory (LSTM), bir tür Recurrent Neural Network (RNN) yapısıdır. 
    RNN'ler, zaman serileri gibi sıralı verileri işlemek için kullanılır ve önceki adımların 
    bilgisini gelecek adımlarda kullanabilme yeteneğine sahiptir. 
    
    LSTM, RNN'lerin hafıza sıkıntısı sorununu çözmek için tasarlanmıştır ve uzun zaman aralıklarında 
    bilgiyi saklayabilme yeteneğine sahiptir. Bu nedenle, zaman serileri tahmininde 
    sıklıkla kullanılır.
    """)



    df = load_data()

    if st.button('Veri Yükle'):
        st.write(df.head())

    X, y = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    model = create_model(X_train.shape)

    if st.button('Modeli Eğit'):
        progress_bar = st.progress(0)
        model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1, callbacks=[ProgressCallback(progress_bar)])
        st.success('Model trained successfully!')

    if st.button('Tahmin Et'):
        pred = model.predict(X_test)
        mse = mean_squared_error(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        r2 = r2_score(y_test, pred)
        # st.write(f"MSE: {mse}, MAE: {mae}, R2: {r2}")

        n_results = st.number_input('Enter the number of results to display:', min_value=1, max_value=len(y_test), value=10)
        # plot_results(y_test, pred, n_results)

if __name__ == '__main__':
    main()
