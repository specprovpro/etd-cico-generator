import pandas as pd


def preview_rws(file):
    return pd.read_excel(
        file,
        header=None
    )


def extract_rws(file):

    df = pd.read_excel(
        file,
        header=None
    )

    records = []

    HEADER_ROW = 5
    DATA_ROW = 7

    # =====================================
    # Cari semua kolom tanggal
    # =====================================

    date_columns = []

    for col in range(len(df.columns)):

        value = df.iloc[HEADER_ROW, col]

        if pd.isna(value):
            continue

        value_str = str(value).strip()

        if value_str.startswith("2026-"):

            date_columns.append(
                {
                    "tanggal": value_str,
                    "clock_in_col": col,
                    "clock_out_col": col + 1,
                    "durasi_col": col + 2
                }
            )

    # =====================================
    # Loop seluruh karyawan
    # =====================================

    for row in range(DATA_ROW, len(df)):

        nik = df.iloc[row, 1]
        nama = df.iloc[row, 2]

        if pd.isna(nik):
            continue

        if pd.isna(nama):
            continue

        nik = str(nik).strip()
        nama = str(nama).strip()

        # ==========================
        # Loop seluruh tanggal
        # ==========================

        for item in date_columns:

            tanggal = item["tanggal"]

            clock_in = df.iloc[
                row,
                item["clock_in_col"]
            ]

            clock_out = df.iloc[
                row,
                item["clock_out_col"]
            ]

            durasi = df.iloc[
                row,
                item["durasi_col"]
            ]

            # rapikan value kosong

            if pd.isna(clock_in):
                clock_in = None

            if pd.isna(clock_out):
                clock_out = None

            if pd.isna(durasi):
                durasi = None

            records.append(
                {
                    "NIK": nik,
                    "Nama": nama,
                    "Tanggal": tanggal,
                    "Clock In": clock_in,
                    "Clock Out": clock_out,
                    "Durasi": durasi
                }
            )

    attendance_df = pd.DataFrame(
        records
    )

    return attendance_df
