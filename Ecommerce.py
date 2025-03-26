import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi dasar dashboard
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Judul Dashboard
st.title("📊 E-Commerce Data Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_cleaned_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_month"] = df["order_purchase_timestamp"].dt.strftime("%Y-%m")
    return df

df = load_data()

# Sidebar - Filter Bulan
st.sidebar.header("Filter Data")
selected_month = st.sidebar.selectbox("Pilih Bulan", df["order_month"].unique())

# Filter data berdasarkan bulan yang dipilih
filtered_df = df[df["order_month"] == selected_month]

# ======== SECTION 1: KPI Metrics ========
st.subheader("📌 Statistik Utama")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Pesanan", filtered_df["order_id"].nunique())

with col2:
    st.metric("Rata-rata Pembayaran (BRL)", round(filtered_df["payment_value"].mean(), 2))

with col3:
    st.metric("Rata-rata Rating", round(filtered_df["review_score"].mean(), 2))

# ======== SECTION 2: Tren Pesanan per Bulan ========
st.subheader("📊 Tren Volume Pesanan")

# Group data berdasarkan bulan
order_trend = df.groupby("order_month").size().reset_index(name="order_count")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=order_trend, x="order_month", y="order_count", marker="o", color="blue", ax=ax)
plt.xticks(rotation=45)
plt.title("Tren Volume Pesanan per Bulan")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Pesanan")
st.pyplot(fig)

# ======== SECTION 3: Distribusi Rating Pelanggan ========
st.subheader("⭐ Distribusi Rating Pelanggan")

fig, ax = plt.subplots(figsize=(10, 5))
sns.countplot(x="review_score", data=df, palette="viridis", ax=ax)
plt.title("Distribusi Review Score")
plt.xlabel("Review Score")
plt.ylabel("Jumlah Ulasan")
st.pyplot(fig)

# ======== SECTION 4: Hubungan Pembayaran dan Rating ========
st.subheader("💰 Hubungan antara Pembayaran dan Rating")

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x="review_score", y="payment_value", data=df, ax=ax)
plt.title("Distribusi Pembayaran berdasarkan Rating Ulasan")
plt.xlabel("Review Score")
plt.ylabel("Total Pembayaran (BRL)")
plt.ylim(0, 5000)  # Batasi skala agar lebih informatif
st.pyplot(fig)

# Footer
st.markdown("**risqienursalsabilailman**")
