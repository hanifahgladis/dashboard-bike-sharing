import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import datetime, timedelta
from babel.numbers import format_currency

# Load dataset
all_df = pd.read_csv("all_data.csv")

# Membuat kolom baru 'season_label' dengan label musim
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
all_df['season_label'] = all_df['season_day'].map(season_labels)

# Set judul dashboard
st.title('Bike Sharing Dashboard')

# Konversi nilai minimum dan maksimum dari kolom 'dteday' menjadi objek datetime.date
min_date = datetime.strptime(all_df['dteday'].min(), '%Y-%m-%d').date()
max_date = datetime.strptime(all_df['dteday'].max(), '%Y-%m-%d').date()

# Menambahkan filter tanggal dengan kalender di sidebar
with st.sidebar:
    st.image("bike-share.png")
    start_date = st.date_input("Pilih Tanggal Mulai", min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("Pilih Tanggal Selesai", max_date, min_value=min_date, max_value=max_date)

# Filter dataset berdasarkan tanggal
filtered_df = all_df[(all_df['dteday'] >= str(start_date)) & (all_df['dteday'] <= str(end_date))]

# Menampilkan hasil filter
st.write("Data Frame Setelah Filter:")
st.write(filtered_df)

# Menampilkan statistik sederhana
st.header('Statistik Peminjaman Sepeda')
st.write(f"Total Peminjaman Sepeda: {filtered_df['cnt_day'].sum()}")
st.write(f"Rata-rata Suhu: {filtered_df['temp_day'].mean()} °C")

# Bar chart untuk membandingkan jumlah peminjaman sepeda pada hari kerja dan hari libur
st.subheader("Peminjaman Sepeda Setiap Musim pada Hari Kerja dan Libur")
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(data=filtered_df, x='cnt_day', y='season_label', hue='workingday_day', ci=None, estimator='sum', palette='coolwarm', orient='h', ax=ax)

plt.xlabel('Jumlah Peminjaman Sepeda')
plt.ylabel('Musim')
# Menambahkan legenda
plt.legend(title='Hari Kerja', loc='upper right', labels=['Hari Kerja', 'Hari Libur'])
st.pyplot(fig)

# Donut chart untuk presentase jumlah peminjaman sepeda berdasarkan kondisi cuaca
st.subheader("Presentase Jumlah Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
weather_counts = filtered_df['weathersit_day'].value_counts()
total = weather_counts.sum()
weather_percentages = (weather_counts / total) * 100

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(weather_percentages, labels=weather_percentages.index, autopct='%1.1f%%',
                                  startangle=90, wedgeprops=dict(width=0.4), textprops=dict(color="black"))
ax.legend(wedges, ['- 1: Clear, Few clouds, Partly cloudy, Partly cloudy',
                   '- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
                   '- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
                   '- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'],
          title='Kondisi Cuaca', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
ax.add_artist(plt.Circle((0, 0), 0.3, fc='white'))
st.pyplot(fig)

# Scatter plot
st.subheader("Pengaruh Suhu, Kelembapan & Kecepatan Angin terhadap Jumlah Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))
scatter = sns.scatterplot(x='temp_day', y='cnt_day', hue='hum_day', size='windspeed_day', data=filtered_df, palette='viridis', ax=ax)
plt.xlabel("Suhu (Normalized)")
plt.ylabel("Jumlah Peminjaman Sepeda")
plt.legend(title='Kelembaban', loc='upper right')
plt.colorbar(scatter.collections[0], label='Kelembaban')
st.pyplot(fig)

# Line chart untuk perbedaan jumlah peminjaman sepeda antara casual dan registered
st.subheader("Peminjam Sepeda Casual vs Peminjam Sepeda Registered")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='casual_day', data=filtered_df, label='Casual', color='skyblue', ax=ax)
sns.lineplot(x='dteday', y='registered_day', data=filtered_df, label='Registered', color='salmon', ax=ax)
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Peminjaman Sepeda')
plt.legend(title='Tipe Pengguna', loc='upper left')
st.pyplot(fig)

# Line chart untuk perbedaan jumlah jam antara peminjam casual dan 'terdaftar'
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='casual_hour', data=filtered_df, label='Casual', marker='o', color='skyblue', ax=ax)
sns.lineplot(x='hr', y='registered_hour', data=filtered_df, label='Registered', marker='o', color='salmon', ax=ax)
plt.xlabel('Waktu (Pukul 0 - 24)')
plt.ylabel('Jumlah Jam Peminjaman Sepeda')
plt.legend(title='Tipe Peminjam')
st.pyplot(fig)


# Menampilkan footer
st.markdown('Copyright (c) Hanifah Gladis Amalia 2023')

