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

    header_row = 5
    subheader_row = 6
    first_data_row = 7

    date_columns = []

    for col in range(len(df.columns)):

        value = df.iloc[header_row, col]

        if str(value).startswith("2026-"):

            date_columns.append(
                (
                    col,
                    str(value)
                )
            )

    for row in range(
        first_data_row,
        len(df)
    ):

        nik = df.iloc[row, 1]
        nama = df.iloc[row, 2]

        if pd.isna(nik):
            continue

        for date_col, tanggal in date_columns:

            clock_in = df.iloc[row, date_col]
            clock_out = df.iloc[row, date_col + 1]
            durasi = df.iloc[row, date_col + 2]

            records.append(
                {
                    "NIK": nik,
                    "Nama": nama,
                    "Tanggal": tanggal,
                    "Clock In": clock_in,
                    "Clock Out": clock_out,
                    "Durasi": durasi,
                }
            )

    return pd.DataFrame(records)
