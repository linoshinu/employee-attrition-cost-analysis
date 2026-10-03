# Employee Attrition & Cost Impact Analysis

A reproducible people analytics portfolio project using SQL and Python. Explore attrition patterns across a fictional 1,470 employee sample, estimate replacement-cost exposure under transparent assumptions, and compare hypothetical retention budget strategies.

> **Scope:** This is synthetic sample data. Cost values are scenario estimates, not company losses; the analysis does not establish causes or predict individual departures. Use only for aggregate learning and planning.

## What this project answers

- Where is sample attrition higher across department, tenure, overtime, and role?
- How does modeled replacement-cost exposure change under low, base, and high assumptions?
- How do equal, attrition-weighted, and cost-weighted budget allocations compare when assumptions change?

## Key sample observations

- 1,470 fictional employee records; 237 marked as attrition (16.1%).
- Attrition is 30.5% in the overtime-Yes group and 10.4% in the overtime-No group in this sample.
- Attrition is 36.4% among the 44 records with under one year of tenure, versus 8.1% among 246 records with 11+ years.
- The base replacement-cost proxy is 50% of annualized monthly income; low/high cases use 25%/75%. Income currency is unspecified, so values are shown in dataset income units.

These are descriptive patterns only. The source contains no verified recruiting costs, vacancy duration, productivity loss, or intervention outcomes.

## Run locally

Requires Python 3.10 or newer:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python scripts/build_assets.py
streamlit run app.py
```

The app provides aggregate department, overtime, tenure, and role views plus adjustable hypothetical budget scenarios. To run the SQL examples, run `python scripts/load_sqlite.py` followed by `python scripts/run_queries.py`.

## Repository map

- `app.py` — interactive Streamlit dashboard
- `scripts/` — reproducible data preparation and SQLite loading
- `sql/` — analysis questions and aggregate validation checks
- `data/raw/` — source sample and provenance notes
- `tableau/dashboard_guide.md` — Tableau-ready field map and dashboard build guide
- `docs/interview_guide.md` — project walkthrough and likely interview questions
- `docs/linkedin_posts.md` — post drafts with accurate data disclosures

## Data, assumptions, and responsible use

The source is IBM's fictional HR Analytics Employee Attrition & Performance sample distributed via Kaggle; see `data/DATA_LICENSE.md` for provenance and license details. Project code is MIT licensed; the dataset retains its own terms.

This one-time synthetic snapshot cannot establish when or why an employee left. Associations are not causal evidence. The replacement-cost and intervention-effect values are user-controlled examples, not finance-approved estimates or proven recommendations. Do not score, rank, target, or make employment decisions about individuals using this project.

## Dashboard options

The working dashboard is the Python Streamlit app. `tableau/dashboard_guide.md` explains how to recreate the aggregate stakeholder view in Tableau Public; a native Tableau workbook is not included. See `DEPLOYMENT.md` for hosting instructions.
