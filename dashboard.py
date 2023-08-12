'''
1. Jumlah pengguna casual dan registered
2. Hari terbanyak sewa sepeda
3. Jam sewa paling ramai
4. Sewa Kerja saat weekend dan workingday
5. Sewa Sepeda berdasarkan season
6. Pengaruh Suhu, Kelembaban, dan Kecepatan Angin pada Sewa Sepeda
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("https://raw.githubusercontent.com/yocimm/bike_sharing_dashboard/master/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/yocimm/bike_sharing_dashboard/master/data/hour.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])


min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo sepeda
    st.image('speda.png')

    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.header(':sparkles: Bike Sharing Dashboard :sparkles:')

#jumlah pengguna
st.subheader('Jumlah Pengguna')
col1, col2 = st.columns(2)

with col1:
    total_registered = day_df['registered'].sum()
    st.metric("Registered", value=total_registered)
 
with col2:
    total_casual = day_df['casual'].sum()
    st.metric("Casual", value=total_casual)


#sewa hari
st.subheader("Rata-Rata Sewa Sepeda Berdasarkan Hari")

avg_rentals_day = day_df.groupby('weekday')['cnt'].mean()
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

colors = ['skyblue'] * 7
colors[np.argmax(avg_rentals_day.values)] = 'darkblue'

fig, ax = plt.subplots(figsize=(8,2))

ax.bar(range(7), avg_rentals_day, color=colors)
ax.set_xticks(range(7))
ax.set_xticklabels(days, rotation=45, fontsize=6)
ax.set_ylabel("Average Bike Rentals", fontsize=6)

st.pyplot(fig)

#sewa jam
st.subheader("Rata-Rata Sewa Sepeda Berdasarkan Jam")

avg_rentals_hour = hour_df.groupby('hr')['cnt'].mean()
colors_hourly = ['lightgreen'] * 24
colors_hourly[np.argmax(avg_rentals_hour.values)] = 'darkgreen'

fig, ax = plt.subplots(figsize=(8,2))

ax.bar(range(24), avg_rentals_hour, color=colors_hourly)
ax.set_xticks(range(24))
ax.set_xticklabels(range(24), fontsize=10)
ax.set_xlabel("Hour of the Day", fontsize=10)
ax.set_ylabel("Average Bike Rentals", fontsize=10)

st.pyplot(fig)

#jenis hari
col1, col2 = st.columns(2)
with col1:
    holiday_rentals = day_df.groupby('holiday')['cnt'].sum()

    labels = ['Regular Days', 'Holidays']
    colors = ['yellow', 'blue']
    explode = (0.1, 0) 

    fig, ax = plt.subplots()

    ax.pie(holiday_rentals, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
    ax.set_title("Holidays vs Regular Days", fontsize=12, fontweight='bold')

    st.pyplot(fig)

with col2:
    seasons_dict = {
    1: 'Springer',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
    }

    avg_rentals_season = day_df.groupby('season')['cnt'].mean()

    labels = [seasons_dict[s] for s in avg_rentals_season.index]
    colors = ['blue', 'coral', 'green', 'yellow']
    explode = [0.1 if s == np.argmax(avg_rentals_season.values) else 0 for s in range(4)]

    fig, ax = plt.subplots()

    ax.pie(avg_rentals_season, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
    ax.set_title("Season", fontsize=12, fontweight='bold')

    st.pyplot(fig)

#Kondisi Cuaca
st.subheader("Pengaruh Cuaca pada Sewa Sepeda")

def categorize_day(row):
    if row['temp'] < 0.25:
        temp_category = 'Dingin'
    elif row['temp'] < 0.5:
        temp_category = 'Sejuk'
    elif row['temp'] < 0.75:
        temp_category = 'Hangat'
    else:
        temp_category = 'Panas'

    if row['hum'] < 0.3:
        hum_category = 'Kering'
    elif row['hum'] < 0.7:
        hum_category = 'Normal'
    else:
        hum_category = 'Lembap'

    if row['windspeed'] < 0.3:
        wind_category = 'Tenang'
    elif row['windspeed'] < 0.6:
        wind_category = 'Sedang'
    else:
        wind_category = 'Kencang'

    weather_map = {
        1: 'Cerah',
        2: 'Berawan/Berkabut',
        3: 'Hujan Ringan/Salju',
        4: 'Hujan Lebat/Salju Besar'
    }
    weather_category = weather_map[row['weathersit']]

    return temp_category, hum_category, wind_category, weather_category

day_df['temp_category'], day_df['hum_category'], day_df['wind_category'], day_df['weather_category'] = zip(*day_df.apply(categorize_day, axis=1))

fig, axes = plt.subplots(2, 2, figsize=(20, 10))

# Suhu
sns.countplot(data=day_df, x='temp_category', order=['Dingin', 'Sejuk', 'Hangat', 'Panas'], ax=axes[0, 0])
axes[0, 0].set_title('Distribusi Hari Berdasarkan Suhu', fontweight='bold')
axes[0, 0].set_xlabel('Kategori Suhu')
axes[0, 0].set_ylabel('Jumlah Hari')

# Kelembapan
sns.countplot(data=day_df, x='hum_category', order=['Kering', 'Normal', 'Lembap'], ax=axes[0, 1])
axes[0, 1].set_title('Distribusi Hari Berdasarkan Kelembapan', fontweight='bold')
axes[0, 1].set_xlabel('Kategori Kelembapan')
axes[0, 1].set_ylabel('Jumlah Hari')

# Kecepatan Angin
sns.countplot(data=day_df, x='wind_category', order=['Tenang', 'Sedang', 'Kencang'], ax=axes[1, 0])
axes[1, 0].set_title('Distribusi Hari Berdasarkan Kecepatan Angin', fontweight='bold')
axes[1, 0].set_xlabel('Kategori Kecepatan Angin')
axes[1, 0].set_ylabel('Jumlah Hari')

# Kondisi Cuaca
sns.countplot(data=day_df, x='weather_category', order=['Cerah', 'Berawan/Berkabut', 'Hujan Ringan/Salju', 'Hujan Lebat/Salju Besar'], ax=axes[1, 1])
axes[1, 1].set_title('Distribusi Hari Berdasarkan Kondisi Cuaca', fontweight='bold')
axes[1, 1].set_xlabel('Kategori Kondisi Cuaca')
axes[1, 1].set_ylabel('Jumlah Hari')

st.pyplot(fig)

st.caption('Copyright (c) yocimm 2023')