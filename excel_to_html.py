import pandas as pd

EXCEL_FILE = "レシート、領収書.xlsx"
OUTPUT_FILE = "index.html"

def main():
    wb = pd.ExcelFile(EXCEL_FILE)
    html_parts = ["<html><head><meta charset='utf-8'><title>Receipts</title></head><body>"]
    for sheet in wb.sheet_names:
        df = wb.parse(sheet)
        html_parts.append(f"<h2>{sheet}</h2>")
        html_parts.append(df.to_html(index=False, border=1))
    html_parts.append("</body></html>")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))
    print(f"HTML saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
