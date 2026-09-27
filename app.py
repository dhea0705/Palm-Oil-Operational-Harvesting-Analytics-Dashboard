import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Operational Sawit", layout="wide")
st.title("🌴 Monitoring Operasional Panen Sawit")

# Load Data
df = pd.read_csv('operasional_panen_sawit.csv')

# --- SIDEBAR FILTER ---
st.sidebar.header("Filter Data")
wilayah = st.sidebar.multiselect(
    "Pilih Wilayah Kebun:",
    options=df['nama_wilayah'].unique(),
    default=df['nama_wilayah'].unique()
)

filtered_df = df[df['nama_wilayah'].isin(wilayah)]

# --- METRIK UTAMA (KPI Cards) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Panen (Kg)", f"{filtered_df['tbs_kg'].sum():,}")
col2.metric("Total Pemanen", f"{filtered_df['jumlah_pemanen'].sum()} Orang")
col3.metric("Rata-rata OER (%)", f"{filtered_df['oer_persen'].mean():.2f}%")
col4.metric("Rata-rata FFA (%)", f"{filtered_df['ffa_persen'].mean():.2f}%")

st.markdown("---")

# --- GRAFIK 1 & 2 ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Produktivitas Pemanen per Wilayah")
    rekap_pemanen = filtered_df.groupby('nama_wilayah').agg({
        'tbs_kg': 'sum',
        'jumlah_pemanen': 'sum'
    }).reset_index()
    rekap_pemanen['avg_kg'] = (rekap_pemanen['tbs_kg'] / rekap_pemanen['jumlah_pemanen']).round(2)
    
    fig_bar = px.bar(
        rekap_pemanen, x='nama_wilayah', y='avg_kg', 
        labels={'avg_kg': 'Rata-rata TBS (Kg/Orang)', 'nama_wilayah': 'Wilayah'},
        color='nama_wilayah'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Dampak Pengiriman Tertunda pada FFA (%)")
    fig_box = px.box(
        filtered_df, x='status_pengiriman', y='ffa_persen',
        color='status_pengiriman',
        labels={'ffa_persen': 'Kadar FFA (%)', 'status_pengiriman': 'Status Pengiriman'}
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- TABEL DATA ---
st.subheader("Data Transaksi Panen")
st.dataframe(filtered_df)