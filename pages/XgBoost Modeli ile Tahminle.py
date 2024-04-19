import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import joblib
import streamlit as st
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 100)

def load_data(feature_file_path, power_file_path):
    df_feature = pd.read_csv(feature_file_path, parse_dates=['Time'], index_col='Time')
    df_power = pd.read_csv(power_file_path, parse_dates=['Time'], index_col='Time')
    return df_feature, df_power

def create_features(df):
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    return df

def prepare_data(df_feature, df_power):
    df_features = create_features(df_feature)
    df_combined = pd.concat([df_features, df_power], axis=1).dropna()
    X = df_combined.drop('Power', axis=1)
    y = df_combined['Power']
    return X, y

def train_model(X, y):
    scaler = StandardScaler()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = xgb.XGBRegressor(n_estimators=1000, learning_rate=0.05)
    model.fit(X_train_scaled, y_train, early_stopping_rounds=5, eval_set=[(X_test_scaled, y_test)], verbose=False)
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    return model, scaler, X_train.columns, X_test, y_test, y_pred, mae

@st.experimental_singleton
def load_model():
    feature_path = r'Data/bu1 (2)'
    power_path = r'Data/your_new_file_path'
    df_feature, df_power = load_data(feature_path, power_path)
    X, y = prepare_data(df_feature, df_power)
    model, scaler, columns, X_test, y_test, y_pred, mae = train_model(X, y)
    return model, scaler, columns, X_test, y_test, y_pred, mae

def main():
    st.title('Power Prediction Model')
    feature_file_path = r'Data/bu1 (2)'
    power_file_path = r'Data/your_new_file_path'
    model, scaler, columns, X_test, y_test, y_pred, mae = load_model()

    # Allowed dates for predictions
    allowed_dates = [datetime(2022, 1, i).date() for i in range(1, 6)]

    # Date selector for predictions
    selected_date = st.date_input("Select a date for prediction", value=datetime(2022, 1, 1), min_value=min(allowed_dates), max_value=max(allowed_dates))

    # Show test prediction errors and calculate MAE
    if st.button('Show Test Prediction Errors'):
        if selected_date in allowed_dates:
            st.write(f"Mean Absolute Error (MAE): {mae:.4f}")
        else:
            st.error("Selected date is not allowed. Please select another date.")

    # Predict future hours
    hours_to_predict = st.number_input("Enter the number of hours to predict:", min_value=1, max_value=48, value=24)

    if st.button('Predict Future Hours'):
        if selected_date in allowed_dates:
            _, df_power = load_data(feature_file_path, power_file_path)
            last_date = df_power.index[-1]  # Last timestamp in the dataset
            predict_start = last_date + timedelta(hours=1)
            future_datetimes = pd.date_range(start=predict_start, periods=hours_to_predict, freq='H')
            future_df = pd.DataFrame(index=future_datetimes)
            future_df = create_features(future_df)
            future_features = future_df.reindex(columns=columns, fill_value=0)
            future_features_scaled = scaler.transform(future_features)
            predictions = model.predict(future_features_scaled)
            predictions_df = pd.DataFrame(predictions, index=future_datetimes, columns=['Predicted Power'])
            st.dataframe(predictions_df)  # Display predictions in a table

            # Plotting
            fig, ax = plt.subplots()
            ax.plot(future_datetimes, predictions, label='Predicted Power')
            ax.set_title('Future Power Predictions')
            ax.set_xlabel('Datetime')
            ax.set_ylabel('Power')
            ax.legend()
            locator = mdates.AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(locator)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Download predictions
            csv = predictions_df.to_csv(index=True)
            st.download_button(
                label="Download predictions as CSV",
                data=csv,
                file_name='predictions.csv',
                mime='text/csv',
            )
        else:
            st.error("Selected date is not allowed for future hour predictions. Please select another date.")

if __name__ == "__main__":
    main()



#streamlit run yenixcbootsd.py
