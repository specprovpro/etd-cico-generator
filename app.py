import streamlit as st
import pandas as pd

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
# PREVIEW MASTER
# ==================================

if master_file:

    try:

        raw_df = pd.read_excel(
            master_file,
            header=None
        )

        header_row = find_header_row(raw_df)

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
# PREVIEW RWS
# ==================================

if len(rws_files) > 0:

    st.subheader("Preview RWS")

    first_rws = rws_files[0]

    try:

        df_rws = pd.read_excel(
            first_rws,
            header=None
        )

        st.success(
            f"{first_rws.name} berhasil dibaca"
        )

        st.write(
            f"Jumlah Baris : {len(df_rws)}"
        )

        st.write(
            f"Jumlah Kolom : {len(df_rws.columns)}"
        )

        st.subheader(
            "15 Baris Pertama RWS"
        )

        st.dataframe(
            df_rws.head(15),
            use_container_width=True
        )

        st.subheader(
            "Nama File RWS"
        )

        for file in rws_files:

            st.write(
                f"📄 {file.name}"
            )

    except Exception as e:

        st.error(
            f"Gagal membaca RWS : {e}"
        )


# ==================================
# PREVIEW REALISASI
# ==================================

if realisasi_file:

    try:

        xls = pd.ExcelFile(
            realisasi_file
        )

        st.subheader(
            "Sheet Realisasi"
        )

        st.write(
            xls.sheet_names
        )

    except Exception as e:

        st.error(
            f"Gagal membaca Realisasi : {e}"
        )


# ==================================
# GENERATE
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
        "Sprint 2 berhasil."
    )

    st.info(
        "Tahap berikutnya: Analisa struktur RWS."
    )
