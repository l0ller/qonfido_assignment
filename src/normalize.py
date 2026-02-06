import glob
import os
import pandas as pd
import re
from datetime import datetime

def normalize_columns(filepath):
    df = pd.read_csv(filepath)

    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    df = df[~(df.iloc[:, 4].isna() & df.iloc[:, 5].isna())]
    pct_col = '% to Net\n Assets'
    market_col = 'Market/Fair Value\n (Rs. in Lakhs)'

    # convert to numeric, non-convertible → NaN
    df[pct_col] = pd.to_numeric(df[pct_col].astype(str)
                                .str.replace("$", "", regex=False)
                                .str.replace("%", "", regex=False)
                                .str.replace(",", "", regex=False),
                                errors='coerce')

    df[market_col] = pd.to_numeric(df[market_col].astype(str)
                                .str.replace("$", "", regex=False)
                                .str.replace(",", "", regex=False),
                                errors='coerce')
                                
    df = df[~((df[market_col] == 0) & (df[pct_col] == 0))].reset_index(drop=True)
    filename = os.path.basename(filepath)
    match = re.search(r'(\d{1,2})(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\d{2})', filename)
    
    if match:
        day, mon_str, yr = match.groups()
        report_date = datetime.strptime(f"{day}{mon_str}{yr}", "%d%b%y").date()
    else:
        report_date = None  # fallback if no date found
    
    df['Reporting Date'] = report_date
    return df.reset_index(drop=True)

def normalize_all():
    files = glob.glob("data/processed/*.csv")
    os.makedirs("output", exist_ok=True)
    for f in files:
        print("Normalizing:", f)
        df = normalize_columns(f)
        base = os.path.splitext(os.path.basename(f))[0]
        out_path = f"output/{base}.csv"
        df.to_csv(out_path, index=False)
        print("Saved →", out_path)

def main():
    filepath = "C:\\Users\\uday9\\qonfido_assignment\\data\\processed\\Weekly%20Debt%20Portfolios%20-%2030Jan26.csv"
    # assign column name to a variable for clarity
    df = normalize_columns(filepath)
    df.to_csv("temp", index=False)
    print(df.columns.tolist())
    print(df.dtypes)
if __name__ == "__main__":    main()
