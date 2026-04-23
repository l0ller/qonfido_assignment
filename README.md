# Axis Mutual Fund Portfolio ETL (Qonfido Assignment)

This project downloads monthly portfolio disclosure files from Axis Mutual Fund, parses Excel sheets into tabular data, and normalizes the result into clean CSV outputs.

## What This Pipeline Does

The pipeline has 3 steps executed in sequence:

1. Download `.xls/.xlsx` files from Axis MF API metadata.
2. Parse each workbook and merge all relevant sheets.
3. Normalize columns and export cleaned CSV files.

Orchestration happens in `src/main.py`.

## Project Structure

```text
qonfido_assignment/
|-- data/
|   |-- raw/           # downloaded source Excel files
|   |-- processed/     # parsed CSVs (one per source file)
|-- output/            # final normalized CSVs
|-- src/
|   |-- download.py    # download logic (API metadata + file fetch)
|   |-- parser.py      # Excel parsing and sheet merge
|   |-- normalize.py   # data cleaning and output normalization
|   |-- main.py        # runs download -> parse -> normalize
|-- requirements.txt
```

## Requirements

- Python 3.10+ (recommended)
- Network access for Axis MF endpoints (for download step)

Python dependencies are listed in `requirements.txt`:

- `pandas`
- `openpyxl`
- `requests`
- `xlrd`

## Setup

### Windows PowerShell

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run The Full Pipeline

From project root:

```bash
python src/main.py
```

This will run:

- `download.main()`
- `parser.parse_all()`
- `normalize.normalize_all()`

## Inputs And Outputs

- Raw downloads: `data/raw/*.xls*`
- Parsed intermediate files: `data/processed/*.csv`
- Final normalized files: `output/*.csv`

Each normalized output currently includes a `Reporting Date` column derived from the filename pattern like `12Dec25`.

## Configure Download Month/Year

Edit `src/download.py` in the `main()` function:

```python
YEAR = 2025
MONTH = "December"
```

Then run `python src/main.py` again.

## Parsing Notes

- In each workbook, sheet named `index` is skipped.
- Parser assumes actual headers begin on row 4 (`header=3`).
- First column is dropped as junk (`df.iloc[:, 1:]`).

If source file formats change, adjust logic in `src/parser.py` and/or `src/normalize.py`.

## Known Assumptions / Limitations

- Date extraction in normalization depends on filename matching pattern: `DDMonYY`.
- Normalization expects specific columns to exist:
	- `% to Net\n Assets`
	- `Market/Fair Value\n (Rs. in Lakhs)`
- Download filter is currently hardcoded for:
	- Axis metadata category: `Monthly Scheme Portfolios`
	- Scheme code: `Consolidated`

## Quick Sanity Checks

After running, validate that:

1. `data/raw/` contains downloaded Excel files.
2. `data/processed/` contains parsed CSV files.
3. `output/` contains normalized CSV files.
4. Output files have non-empty rows and a populated `Reporting Date` where filename format matches.

## Troubleshooting

- `ModuleNotFoundError`: activate virtual environment and reinstall dependencies.
- Empty downloads: confirm `YEAR` and `MONTH` in `src/download.py` match available API metadata.
- Parse issues: source workbook layout may have changed; review `header=3` and dropped columns.
- Missing `Reporting Date`: filename does not match `DDMonYY` pattern.

## Suggested Next Improvements

1. Move `YEAR` and `MONTH` to CLI arguments or environment variables.
2. Add logging instead of `print` statements.
3. Add unit tests for parser/normalizer edge cases.
4. Add schema validation for required columns before normalization.
