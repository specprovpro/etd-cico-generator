import pandas as pd


def read_realisasi(file):

    df = pd.read_excel(
        file,
        header=0
    )

    # Header sebenarnya ada di baris pertama
    df.columns = [
        str(x).strip()
        for x in df.iloc[0]
    ]

    # Buang baris header duplikat
    df = df.iloc[1:].reset_index(drop=True)

    # Buang baris kosong
    df = df.dropna(
        how="all"
    )

    return df
