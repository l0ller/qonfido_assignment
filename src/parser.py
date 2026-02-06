import pandas as pd
import os
from datetime import datetime
import glob




def parse_excel_file(filepath, amc_name="Axis Mutual Fund"):
    xl = pd.ExcelFile(filepath)

    dfs = []

    for sheet in xl.sheet_names:

        if sheet.lower() == "index":
            continue

        # ✅ skip junk rows (header is at row 4)
        df = xl.parse(sheet, header=3)

        # ✅ drop first junk column (column A)
        df = df.iloc[:, 1:]

        df["AMC Name"] = amc_name
        df["Scheme Name"] = sheet

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)



def parse_all():

    files = glob.glob("data/raw/*.xls*")

    os.makedirs("data/processed", exist_ok=True)

    for f in files:
        print("Parsing:", f)

        df = parse_excel_file(f)
        # create output filename from raw filename
        base = os.path.splitext(os.path.basename(f))[0]
        out_path = f"data/processed/{base}.csv"

        df.to_csv(out_path, index=False)

        print("Saved →", out_path)


