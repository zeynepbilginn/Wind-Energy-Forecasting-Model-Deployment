import pandas as pd
import warnings

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
warnings.filterwarnings('ignore')





# Veri setini yükleme
df_location1 = pd.read_csv(r'C:\Users\User\OneDrive\Masaüstü\MiuulStreamlit\pythonProject3\Data\Location1.csv', parse_dates=['Time'], index_col='Time')
df_location2 = pd.read_csv(r'C:\Users\User\OneDrive\Masaüstü\MiuulStreamlit\pythonProject3\Data\Location2.csv', parse_dates=['Time'], index_col='Time')
df_location3 = pd.read_csv(r'C:\Users\User\OneDrive\Masaüstü\MiuulStreamlit\pythonProject3\Data\Location3.csv', parse_dates=['Time'], index_col='Time')
df_location4 = pd.read_csv(r'C:\Users\User\OneDrive\Masaüstü\MiuulStreamlit\pythonProject3\Data\Location4.csv', parse_dates=['Time'], index_col='Time')





# Her bir DataFrame'e konum sütunu ekle
df_location1['Location'] = 'Location1'
df_location2['Location'] = 'Location2'
df_location3['Location'] = 'Location3'
df_location4['Location'] = 'Location4'

# Veri setlerini tek bir DataFrame olarak birleştir
df = pd.concat([df_location1, df_location2, df_location3, df_location4])


# İndeksi sıfırla
df = df.reset_index()
df.head()
# df.to_csv('data.csv', index=False)


df["temperature_2m"].min()
df["temperature_2m"].max()
df["Power"].max()
df["Power"].min()