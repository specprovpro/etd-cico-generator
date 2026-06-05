import streamlit as st

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

if st.button("Generate"):

    if not master_file:
        st.error("Master belum dipilih")
        st.stop()

    if not realisasi_file:
        st.error("Realisasi belum dipilih")
        st.stop()

    if len(rws_files) == 0:
        st.error("RWS belum dipilih")
        st.stop()

    st.success("File berhasil diterima")

    st.write("Master :", master_file.name)
    st.write("Realisasi :", realisasi_file.name)

    for file in rws_files:
        st.write(file.name)
