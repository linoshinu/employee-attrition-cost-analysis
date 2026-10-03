"""Load the prepared CSV into a local SQLite database for the query examples."""

from pathlib import Path
import sqlite3

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "processed" / "employees_clean.csv"
DB = ROOT / "data" / "employee_attrition.sqlite"


def main() -> None:
    if not CSV.exists():
        raise FileNotFoundError("Run `python scripts/build_assets.py` first.")
    data = pd.read_csv(CSV)
    with sqlite3.connect(DB) as connection:
        data.to_sql("employee_attrition", connection, if_exists="replace", index=False)
    print(f"Loaded {len(data):,} rows into {DB.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
