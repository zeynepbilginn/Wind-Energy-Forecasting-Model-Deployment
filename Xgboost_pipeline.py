from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from datetime import datetime, timedelta

# Load datasets
df_power = pd.read_csv(r'Data/bu1 (2)', parse_dates=['Time'], index_col='Time')
df_feature = pd.read_csv(r'Data/your_new_file_path', parse_dates=['Time'], index_col='Time')


def create_features(df):
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day

    # Existing dummy data
    df['temperature_2m'] = np.random.normal(loc=20, scale=5, size=len(df))
    df['relativehumidity_2m'] = np.random.normal(loc=70, scale=10, size=len(df))
    df['dewpoint_2m'] = np.random.normal(loc=10, scale=3, size=len(df))
    df['windspeed_10m'] = np.random.normal(loc=10, scale=3, size=len(df))  # Dummy data
    df['windspeed_100m'] = np.random.normal(loc=15, scale=5, size=len(df))  # Dummy data
    df['winddirection_10m'] = np.random.choice(range(360), size=len(df))
    df['winddirection_100m'] = np.random.choice(range(360), size=len(df))

    # Adding missing wind features
    df['windgusts_10m'] = np.random.normal(loc=5, scale=2, size=len(df))  # Dummy data

    return df[['temperature_2m', 'relativehumidity_2m', 'dewpoint_2m', 'windspeed_10m',
               'windspeed_100m', 'winddirection_10m', 'winddirection_100m', 'windgusts_10m']]


df_features = create_features(df_feature)
df_combined = pd.concat([df_features, df_power], axis=1).dropna()

# Split the data
X = df_combined.drop('Power', axis=1)
y = df_combined['Power']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.base import clone
import xgboost as xgb


class XGBRegressorWithEarlyStopping(xgb.XGBRegressor):
    def fit(self, X, y, **kwargs):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        eval_set = [(X_val, y_val)]
        super().fit(X_train, y_train, eval_set=eval_set, early_stopping_rounds=5, verbose=False, **kwargs)
        return self


pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', XGBRegressorWithEarlyStopping(n_estimators=1000, learning_rate=0.05, verbosity=0))
])

pipeline.fit(X_train, y_train)


joblib.dump(pipeline, 'power_forecasting_pipeline7.pkl')

loaded_pipeline = joblib.load('power_forecasting_pipeline7.pkl')


predictions = loaded_pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae:.3f}")


def predict_future_hours(loaded_pipeline, hours):
    last_point = pd.Timestamp.now()
    future_datetimes = pd.date_range(start=last_point, periods=hours + 1, freq='H')[1:]
    future_df = pd.DataFrame(index=future_datetimes)
    future_features = create_features(future_df)

    columns_order = X_train.columns.tolist()
    future_features = future_features.reindex(columns=columns_order)  # Align columns

    future_predictions = loaded_pipeline.predict(future_features)
    predictions_df = pd.DataFrame(future_predictions, index=future_datetimes, columns=['Predicted Power'])
    return predictions_df


hours_to_predict = int(input("Enter the number of hours to predict: "))
future_predictions = predict_future_hours(loaded_pipeline, hours_to_predict)
print(future_predictions)
