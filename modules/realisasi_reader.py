import pandas as pd


def split_days(value):

    if pd.isna(value):
        return []

    value = str(value).strip()

    if value.lower() == "none":
        return []

    result = []

    parts = value.split(",")

    for item in parts:

        item = item.strip()

        if item.isdigit():

            result.append(
                int(item)
            )

    return result


def read_realisasi(file):

    df = pd.read_excel(
        file,
        header=None
    )

    # ambil header dari baris pertama
    df.columns = [
        str(x).strip()
        for x in df.iloc[0]
    ]

    # hapus baris header
    df = df.iloc[1:]

    # hapus baris kosong
    df = df.dropna(
        how="all"
    )

    # reset index
    df = df.reset_index(
        drop=True
    )

    return df


def build_realisasi_dict(df):

    realisasi_dict = {}

    for _, row in df.iterrows():

        nik = str(
            row["NIK"]
        ).strip()

        realisasi_dict[nik] = {

            "CUTI":
            split_days(
                row["TANGGAL CUTI"]
            ),

            "SAKIT":
            split_days(
                row["TANGGAL SAKIT"]
            ),

            "IJIN_TERLAMBAT":
            split_days(
                row["TANGGAL IJIN DATANG TERLAMBAT"]
            ),

            "IJIN_PULANG":
            split_days(
                row["TANGGAL IJIN PULANG"]
            ),

            "PERUBAHAN_JAM":
            split_days(
                row["TANGGAL PERUBAHAN JAM"]
            )
        }

    return realisasi_dict
