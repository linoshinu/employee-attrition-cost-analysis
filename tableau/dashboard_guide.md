# Tableau Public dashboard build guide

The repository's `data/processed/employees_clean.csv` is ready to connect in Tableau Public. The Python app is the reproducible interactive demo; this guide recreates the same stakeholder view in Tableau Desktop/Public without requiring a custom database.

## Connect and prepare

1. Open Tableau Public and choose **Text File**.
2. Select `data/processed/employees_clean.csv`.
3. Confirm `AttritionFlag` is a whole number, `AnnualIncome` and the three `ReplacementCost*` fields are decimal numbers, and dimensions such as `Department`, `OverTime`, `JobRole`, `TenureBand`, and `SalaryBand` are strings.
4. Hide `EmployeeNumber` is already removed from the prepared table. Keep employee-level records out of published tooltips and views; show aggregate counts only.

## Create calculated fields

Create these fields in the workbook so their definitions remain visible to reviewers:

```text
Attrition Rate
SUM([AttritionFlag]) / COUNT([AttritionFlag])

Sample Leavers
SUM([AttritionFlag])

Sample Employees
COUNT([AttritionFlag])

Modeled Cost - Low
SUM(IF [AttritionFlag] = 1 THEN [ReplacementCostLow] END)

Modeled Cost - Base
SUM(IF [AttritionFlag] = 1 THEN [ReplacementCostBase] END)

Modeled Cost - High
SUM(IF [AttritionFlag] = 1 THEN [ReplacementCostHigh] END)
```

Format `Attrition Rate` as a percentage. Format costs as numbers with separators and append “dataset income units” to the worksheet title or tooltip; the source does not specify a currency.

## Assemble a one-page dashboard

Use a fixed desktop canvas near 1200 × 850 px, with navy titles, teal for attrition/cost, and amber for tenure. Keep cohort size visible in the tooltip.

| Area | View | Fields |
|---|---|---|
| Top row | KPI tiles | `Sample Employees`, `Sample Leavers`, `Attrition Rate`, `Modeled Cost - Base` |
| Left | Department comparison | `Department` rows; `Attrition Rate` columns; `Sample Employees` and `Sample Leavers` in tooltip |
| Right | Tenure comparison | `TenureBand` columns; `Attrition Rate` rows; custom order `<1`, `1-3`, `4-5`, `6-10`, `11+` |
| Bottom left | Overtime comparison | `OverTime` columns; `Attrition Rate` rows; count in tooltip |
| Bottom right | Cost sensitivity | `Department` rows and the three modeled cost fields as side-by-side bars |
| Filter rail | Drill-down controls | `Department`, `OverTime`, `TenureBand`, and `JobRole`; apply to all worksheets |

Use labels sparingly. Include both the percentage and the sample count in tooltips so a small group is not mistaken for a stable estimate. A caption should state: “Fictional IBM sample data. Cost cases are assumptions, not realized losses. Descriptive patterns do not establish causes.”

## Publish and retain the artifact

Tableau Public makes a workbook public. Review the source note and synthetic-data caveat before publishing, then use **File → Save to Tableau Public**. Save/download the workbook into this folder as a `.twb` or `.twbx` and add the Tableau Public share URL to the GitHub README only after you have opened the published view and confirmed its filters and captions.

The Tableau workbook is intentionally authored in Tableau Public rather than generated from guessed XML. This repository includes the validated input CSV, field definitions, layout, and calculation recipe so the published workbook can be opened and maintained in Tableau.
