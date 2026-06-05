import streamlit as st
import pandas as pd

from modules.rws_reader import (
    preview_rws,
    extract_rws
)

st.set_page_config(
    page_title="ETD CICO Generator",
    layout="wide"
)

st.title("ETD CICO Report Generator")


# ==================================
# FUNGSI CARI HEADER MASTER
# ==================================

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


# ==================================
# UPLOAD FILE
# ==================================

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


# ==================================
# MASTER PREVIEW
# ==================================

if master_file:

    try:

        raw_df = pd.read_excel(
            master_file,
            header=None
        )

        header_row = find_header_row(
            raw_df
        )

        if header_row is None:

            st.error(
                "Header Master tidak ditemukan"
            )

        else:

            df_master = pd.read_excel(
                master_file,
                header=header_row
            )

            df_master = df_master.dropna(
                how="all"
            )

            df_master.columns = [
                str(col).strip()
                for col in df_master.columns
            ]

            st.success(
                f"Master berhasil dibaca ({len(df_master)} karyawan)"
            )

            with st.expander(
                "Preview Master"
            ):

                st.write(
                    df_master.columns.tolist()
                )

                st.dataframe(
                    df_master.head(20),
                    use_container_width=True
                )

    except Exception as e:

        st.error(
            f"Gagal membaca Master : {e}"
        )


# ==================================
# RWS PREVIEW
# ==================================

if len(rws_files) > 0:

    first_rws = rws_files[0]

    try:

        st.subheader(
            "Preview RWS Mentah"
        )

        raw_rws = preview_rws(
            first_rws
        )

        st.dataframe(
            raw_rws.head(15),
            use_container_width=True
        )

        st.subheader(
            "Hasil Extract RWS"
        )

        attendance_df = extract_rws(
            first_rws
        )

        st.success(
            f"Berhasil membuat {len(attendance_df)} transaksi"
        )

        st.dataframe(
            attendance_df.head(50),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Gagal membaca RWS : {e}"
        )


# ==================================
# REALISASI PREVIEW
# ==================================

if realisasi_file:

    try:

        realisasi_df = pd.read_excel(
            realisasi_file
        )

        st.subheader(
            "Preview Realisasi"
        )

        st.write(
            f"Jumlah Data : {len(realisasi_df)}"
        )

        st.dataframe(
            realisasi_df.head(20),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Gagal membaca Realisasi : {e}"
        )


# ==================================
# GENERATE BUTTON
# ==================================

if st.button("Generate"):

    if not master_file:

        st.error(
            "Master belum dipilih"
        )
        st.stop()

    if not realisasi_file:

        st.error(
            "Realisasi belum dipilih"
        )
        st.stop()

    if len(rws_files) == 0:

        st.error(
            "RWS belum dipilih"
        )
        st.stop()

    st.success(
        "Sprint 3 berhasil."
    )

    st.info(
        "Tahap berikutnya: Rule Engine."
    )
