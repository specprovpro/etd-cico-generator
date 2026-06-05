import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ETD CICO Generator",
    layout="wide"
)

st.title("ETD CICO Report Generator")

master_file = st.file_uploader(
    "Master Karyawan",
    type=["xlsx"]
)

realisasi_file = st.file_uploader(
    "Realisasi Bulanan",
    type=["xlsx"]
)

rws_files = st.file_uploader(
    "RWS Mingguan",
    type=["xlsx"],
    accept_multiple_files=True
)

if master_file:

    df_master = pd.read_excel(master_file)

    st.success(
        f"Master berhasil dibaca ({len(df_master)} karyawan)"
    )

    st.subheader("Preview Master")

    st.dataframe(df_master.head())

if st.button("Generate"):

    st.success("Generate ditekan")
