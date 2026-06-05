import streamlit as st
import pandas as pd

from modules.master_reader import (
    read_master,
    build_master_dict
)

from modules.realisasi_reader import (
    read_realisasi,
    build_realisasi_dict
)

from modules.rws_reader import (
    extract_rws
)

from modules.rule_engine import (
    build_violation_report
)

st.set_page_config(
    page_title="ETD CICO Generator",
    layout="wide"
)

st.title(
    "ETD CICO Report Generator"
)

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
# GENERATE
# ==================================

if st.button("Generate"):

    try:

        # ==========================
        # VALIDASI
        # ==========================

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

        # ==========================
        # MASTER
        # ==========================

        master_df = read_master(
            master_file
        )

        master_dict = (
            build_master_dict(
                master_df
            )
        )

        # ==========================
        # REALISASI
        # ==========================

        realisasi_df = (
            read_realisasi(
                realisasi_file
            )
        )

        realisasi_dict = (
            build_realisasi_dict(
                realisasi_df
            )
        )

        # ==========================
        # RWS
        # ==========================

        all_attendance = []

        for file in rws_files:

            attendance_df = (
                extract_rws(
                    file
                )
            )

            all_attendance.append(
                attendance_df
            )

        attendance_df = pd.concat(
            all_attendance,
            ignore_index=True
        )

        st.success(
            f"Total transaksi: {len(attendance_df)}"
        )

        # ==========================
        # PELANGGARAN
        # ==========================

        violation_df = (
            build_violation_report(
                attendance_df,
                master_dict,
                realisasi_dict
            )
        )

        st.subheader(
            "Detail Pelanggaran"
        )

        st.write(
            f"Total Pelanggaran: {len(violation_df)}"
        )

        st.dataframe(
            violation_df,
            use_container_width=True
        )

        # ==========================
        # REKAP
        # ==========================

        if len(
            violation_df
        ) > 0:

            summary_df = (
                violation_df
                .groupby(
                    [
                        "NIK",
                        "Nama"
                    ]
                )
                .size()
                .reset_index(
                    name="Total Pelanggaran"
                )
                .sort_values(
                    "Total Pelanggaran",
                    ascending=False
                )
            )

            st.subheader(
                "Ranking Pelanggaran"
            )

            st.dataframe(
                summary_df,
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )
