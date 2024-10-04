import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

## HELPER FUNCTION

# Fungsi banyaknya penyewaan sepeda
def total_penyewaan_sepeda_df(day_df):
   cnt_day_df = day_df.groupby(by="dteday").agg({
      "cnt": "sum"})
   cnt_day_df = cnt_day_df.reset_index()
   return cnt_day_df 

# Fungsi banyaknya penyewa registered
def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"})
   reg_df = reg_df.reset_index()
   return reg_df

# Fungsi banyaknya penyewa casual
def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dteday").agg({
      "casual": "sum"})
   cas_df = cas_df.reset_index()
   return cas_df

# Fungsi banyaknya penyewa sepeda berdasarkan jam
def total_jam_df(hour_df):
    total_penyewaan_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return total_penyewaan_df

# Fungsi banyaknya penyewa sepeda berdasarkan musim
def total_musim_df(day_df): 
    season_df = day_df.groupby(by="season").cnt.sum().reset_index() 
    return season_df

# Fungsi banyaknya penyewa sepeda berdasarkan hari dan tanggal
def penyewa_harian_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

## LOAD BERKAS DAN DEFINISIKAN DATA

# Definisikan data
day_df = pd.read_csv("days_clean.csv")
hour_df = pd.read_csv("hours_clean.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)   

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

## KOMPONEN FILTER

minimal_datedy_day = day_df["dteday"].min()
maximum_datedy_day = day_df["dteday"].max()

minimal_datedy_hour = hour_df["dteday"].min()
maximal_datedy_hour = hour_df["dteday"].max()

with st.sidebar:
    # start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=minimal_datedy_day,
        max_value=maximum_datedy_day,
        value=[minimal_datedy_day, maximum_datedy_day])
  
main_df_day = day_df[(day_df["dteday"] >= str(start_date)) & 
                        (day_df["dteday"] <= str(end_date))]

main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                        (hour_df["dteday"] <= str(end_date))]

sewa_total_df = total_penyewaan_sepeda_df(main_df_day)
registered_df = total_registered_df(main_df_day)
casual_df = total_casual_df(main_df_day)
total_penjualan_jam = total_jam_df(main_df_hour)
season_df = total_musim_df(main_df_day)
day_df_count_2011 = penyewa_harian_df(main_df_day)

## VISUALISASI DATA DASHBOARD

st.header('Bike Sharing :sparkles:')

# 1
# Menampilkan penyewaan sepeda secara keseluruhan, registered, dan casual
st.subheader('Penyewaan Total Sepeda')
col1, col2, col3 = st.columns(3)
# Menampilkan data banyaknya total penyewa sepeda 
with col1:
    total_orders = sewa_total_df.cnt.sum()
    st.metric("Total Penyewaan Sepeda", value=total_orders)
# Menampilkan data banyaknya total penyewa sepeda registered
with col2:
    total_sum = registered_df.registered.sum()
    st.metric("Total Registered", value=total_sum)
# Menampilkan data banyaknya total penyewa sepeda casual
with col3:
    total_sum = casual_df.casual.sum()
    st.metric("Total Casual", value=total_sum)

# 2
# Menampilkan Penyewaan Sepeda Harian Seiring Waktu
st.subheader("Penyewaan Sepeda Harian Seiring Waktu")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    day_df["dteday"],
    day_df["cnt"],
    marker='o', 
    linewidth=6,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)

st.pyplot(fig)

# 3
# Menampilkan jam penyewaan sepeda
st.subheader("Jumlah Penyewaan Sepeda Ketika Jam Paling Sibuk dan Jam Tidak Sibuk")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

sns.barplot(x="hr", y="cnt", data=total_penjualan_jam.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel("Jumlah Penyewaan Sepeda")
ax[0].set_xlabel("Waktu Paling Sibuk", fontsize=20)
ax[0].set_title("Jumlah Penyewaan Sepeda ketika Jam Sibuk", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=10)
 
sns.barplot(x="hr", y="cnt", data=total_penjualan_jam.sort_values(by="hr", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel("Jumlah Penyewaan Sepeda")
ax[1].set_xlabel("Waktu Paling Tidak Sibuk",  fontsize=20)
ax[1].set_title("Jumlah Penyewaan Sepeda ketika Jam Tidak Sibuk", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=10)
 
st.pyplot(fig)

# 4
# Menampilkan tren bulanan penyewaan sepeda
st.subheader("Tren Bulanan Penyewaan Sepeda dari 2011 hingga 2012")

grouped_data = day_df.groupby(pd.Grouper(key='dteday', freq='M'))['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(20, 5))
ax.plot(
    grouped_data['dteday'], 
    grouped_data['cnt'], 
    marker='o', 
    linewidth=2,
    color="#90CAF9"
    )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# 5
# Menampilkan musim penyewaan sepeda
st.subheader("Musim Penyewaan Sepeda")

labels = '1: Semi', '2: Panas', '3: Gugur', '4: Dingin'
colors1 = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
        y="cnt", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        palette=colors1,
    )
ax.set_ylabel(None)
ax.set_xlabel("Musim")
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)

# 6
# Menampilkan jumlah penyewaan sepeda registered dan casual
st.subheader("Perbandingan Penyewaaan Sepeda Registered dengan Casual")

labels = 'casual', 'registered'
sizes = [15, 60]
explode = (0, 0.2) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)