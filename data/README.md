# Data folder

- `raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` is the source dataset as downloaded from a public mirror. See [`DATA_LICENSE.md`](DATA_LICENSE.md) for attribution, the Kaggle page, and terms.
- `processed/employees_clean.csv` is rebuilt by `python scripts/build_assets.py`. It drops the source's administrative identifier and constant columns, then adds derived bands and cost assumptions.
- `processed/*_summary.csv` and `processed/summary.json` are aggregate outputs used to inspect and compare the sample.
- `employee_attrition.sqlite` is created locally by `python scripts/load_sqlite.py` and is ignored by Git.

Do not treat the file as real employee data. The source is a fictional demonstration dataset.
