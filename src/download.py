import os
import requests

BASE = "https://www.axismf.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# -------------------------------------------------
# Fetch metadata from API
# -------------------------------------------------
def fetch_monthly_metadata():
    url = "https://www.axismf.com/cms/api/statutory-disclosures-scheme"

    params = {
        "cat": "Monthly Scheme Portfolios"
    }

    r = requests.get(url, params=params, headers=HEADERS)
    r.raise_for_status()

    return r.json()


# -------------------------------------------------
# Filter files for given month + year
# -------------------------------------------------
def get_files_for_month_year(metadata, year, month):
    """
    month should be string like: 'January', 'December'
    """

    urls = []

    for item in metadata:

        if item.get("field_year") != str(year):
            continue

        if item.get("field_months") != month:
            continue
        if item.get("field_aboutus_scheme_code") != "Consolidated":
            continue

        file_path = item.get("field_related_file")

        if not file_path:
            continue

        if ".xls" not in file_path.lower():
            continue

        urls.append(BASE + file_path)

    return urls


# -------------------------------------------------
# Download helper
# -------------------------------------------------
def download_file(url, save_dir="data/raw"):
    os.makedirs(save_dir, exist_ok=True)

    filename = url.split("/")[-1]
    path = os.path.join(save_dir, filename)

    r = requests.get(url, headers=HEADERS)

    with open(path, "wb") as f:
        f.write(r.content)

    print("Downloaded:", path)


# -------------------------------------------------
# MAIN (all downloading ONLY here as you wanted)
# -------------------------------------------------
def main():
    YEAR = 2025
    MONTH = "December"

    print(f"\nDownloading Axis portfolios for {MONTH} {YEAR}\n")

    metadata = fetch_monthly_metadata()

    urls = get_files_for_month_year(metadata, YEAR, MONTH)

    if not urls:
        print("No files found")
        return

    for url in urls:
        download_file(url)


if __name__ == "__main__":
    main()
