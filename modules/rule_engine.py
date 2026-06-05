import pandas as pd


def parse_duration_to_seconds(duration_value):

    if pd.isna(duration_value):
        return 0

    try:

        parts = str(duration_value).split(":")

        if len(parts) != 3:
            return 0

        h = int(parts[0])
        m = int(parts[1])
        s = int(parts[2])

        return h * 3600 + m * 60 + s

    except:
        return 0


def check_violation(
    row,
    master_dict,
    realisasi_dict
):

    nik = str(row["NIK"])

    tanggal = pd.to_datetime(
        row["Tanggal"]
    ).day

    # =====================
    # CEK CUTI / SAKIT
    # =====================

    if nik in realisasi_dict:

        exc = realisasi_dict[nik]

        if tanggal in exc["CUTI"]:
            return None

        if tanggal in exc["SAKIT"]:
            return None

    # =====================
    # CLOCK IN / OUT
    # =====================

    clock_in = row["Clock In"]
    clock_out = row["Clock Out"]

    if pd.isna(clock_in) and pd.isna(clock_out):
        return "TIDAK_CICO"

    if (
        pd.notna(clock_in)
        and pd.isna(clock_out)
    ):
        return "LUPA_CLOCK_OUT"

    # =====================
    # DATA MASTER
    # =====================

    if nik not in master_dict:
        return None

    master = master_dict[nik]

    jam_masuk = str(
        master["Jam Masuk"]
    )

    jam_keluar = str(
        master["Jam Keluar Normal"]
    )

    # =====================
    # TELAT
    # =====================

    try:

        if str(clock_in) > jam_masuk:
            return "TELAT"

    except:
        pass

    # =====================
    # PULANG CEPAT
    # =====================

    try:

        izin_pulang = []

        if nik in realisasi_dict:
            izin_pulang = (
                realisasi_dict[nik]
                ["IJIN_PULANG"]
            )

        if (
            tanggal
            not in izin_pulang
        ):

            if str(clock_out) < jam_keluar:
                return "PULANG_CEPAT"

    except:
        pass

    # =====================
    # DURASI
    # =====================

    durasi_sec = parse_duration_to_seconds(
        row["Durasi"]
    )

    if durasi_sec < 32400:
        return "DURASI_KURANG"

    return None


def build_violation_report(
    attendance_df,
    master_dict,
    realisasi_dict
):

    violations = []

    for _, row in attendance_df.iterrows():

        violation = check_violation(
            row,
            master_dict,
            realisasi_dict
        )

        if violation:

            violations.append(
                {
                    "NIK": row["NIK"],
                    "Nama": row["Nama"],
                    "Tanggal": row["Tanggal"],
                    "Pelanggaran": violation
                }
            )

    return pd.DataFrame(
        violations
    )
