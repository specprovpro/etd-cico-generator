import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ETD CICO Generator",
    layout="wide"
)

st.title("ETD CICO Report Generator")

# ==========================
# Upload File
# ==========================

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

# ==========================
# Fungsi Cari Header Otomatis
# ==========================

def find_header_row(df):

    for idx, row in df.iterrows():

        values = [
            str(x).strip().lower()
            for x in row.values
            if pd.notna(x)
        ]

        row_text = " ".join(values)

        if (
            "nik" in row_text
            and "nama" in row_text
        ):
            return idx

    return None


# ==========================
# Preview Master
# ==========================

if master_file:

    try:

        raw_df = pd.read_excel(
            master_file,
            header=None
        )

        header_row = find_header_row(raw_df)

        if header_row is None:

            st.error(
                "Header tidak ditemukan. Pastikan terdapat kolom NIK dan Nama."
            )

        else:

            df_master = pd.read_excel(
                master_file,
                header=header_row
            )

            # hapus baris kosong
            df_master = df_master.dropna(
                how="all"
            )

            # rapikan nama kolom
            df_master.columns = [
                str(col).strip()
                for col in df_master.columns
            ]

            st.success(
                f"Master berhasil dibaca ({len(df_master)} karyawan)"
            )

            st.subheader("Kolom Terdeteksi")

            st.write(
                df_master.columns.tolist()
            )

            st.subheader("Preview Master")

            st.dataframe(
                df_master.head(20),
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"Gagal membaca file master: {e}"
        )


# ==========================
# Preview RWS
# ==========================

if len(rws_files) > 0:

    st.subheader("File RWS Terdeteksi")

    for file in rws_files:

        st.write(file.name)


# ==========================
# Tombol Generate
# ==========================

if st.button("Generate"):

    if not master_file:

        st.error(
            "Master Karyawan belum dipilih"
        )

        st.stop()

    if not realisasi_file:

        st.error(
            "Realisasi Bulanan belum dipilih"
        )

        st.stop()

    if len(rws_files) == 0:

        st.error(
            "File RWS belum dipilih"
        )

        st.stop()

    st.success(
        "Semua file berhasil diterima."
    )

    st.info(
        "Tahap berikutnya: Membaca dan memproses file RWS."
    )
