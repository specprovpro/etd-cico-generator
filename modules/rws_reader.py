import pandas as pd


def preview_rws(file):

    df = pd.read_excel(
        file,
        header=None
    )

    return df
