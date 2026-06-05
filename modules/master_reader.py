import pandas as pd


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


def read_master(file):

    raw_df = pd.read_excel(
        file,
        header=None
    )

    header_row = find_header_row(
        raw_df
    )

    if header_row is None:

        raise Exception(
            "Header Master tidak ditemukan"
        )

    df = pd.read_excel(
        file,
        header=header_row
    )

    df = df.dropna(
        how="all"
    )

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    return df


def build_master_dict(df):

    master_dict = {}

    for _, row in df.iterrows():

        nik = str(
            row["Nik"]
        ).strip()

        master_dict[nik] = {
            "Nama": row["Nama"],
            "Bagian": row["Bagian"],
            "Jam Masuk": str(
                row["Jam Masuk"]
            ),
            "Jam Keluar Normal": str(
                row["Jam Keluar Normal"]
            ),
            "Jam Keluar Jumat": str(
                row["Jam Keluar Jumat"]
            )
        }

    return master_dict
