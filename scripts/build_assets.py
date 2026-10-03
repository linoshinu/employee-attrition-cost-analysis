"""Prepare a de-identified, Tableau-ready table and aggregate dashboard assets."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
PROCESSED = ROOT / "data" / "processed"


def prepare_employees(raw: pd.DataFrame) -> pd.DataFrame:
    required = {"Attrition", "Department", "MonthlyIncome", "YearsAtCompany", "OverTime"}
    missing = required.difference(raw.columns)
    if missing:
        raise ValueError(f"Required columns are missing: {sorted(missing)}")
    if raw["Attrition"].isna().any() or not set(raw["Attrition"].unique()).issubset({"Yes", "No"}):
        raise ValueError("Attrition must contain only Yes/No values with no blanks")

    data = raw.drop(columns=["EmployeeNumber", "EmployeeCount", "Over18", "StandardHours"], errors="ignore").copy()
    data["AttritionFlag"] = data["Attrition"].eq("Yes").astype("int8")
    data["AnnualIncome"] = data["MonthlyIncome"] * 12

    data["TenureBand"] = pd.cut(
        data["YearsAtCompany"],
        bins=[-1, 0, 3, 5, 10, np.inf],
        labels=["<1 year", "1-3 years", "4-5 years", "6-10 years", "11+ years"],
        include_lowest=True,
    ).astype("string")
    income_percentile = data["MonthlyIncome"].rank(method="average", pct=True)
    data["SalaryBand"] = np.select(
        [income_percentile <= 1 / 3, income_percentile <= 2 / 3],
        ["Lower third", "Middle third"],
        default="Upper third",
    )

    # Sensitivity range only: the source has no actual replacement-cost fields.
    data["ReplacementCostLow"] = data["AnnualIncome"] * 0.25
    data["ReplacementCostBase"] = data["AnnualIncome"] * 0.50
    data["ReplacementCostHigh"] = data["AnnualIncome"] * 0.75
    return data


def summarize(data: pd.DataFrame, dimension: str) -> pd.DataFrame:
    grouped = data.groupby(dimension, observed=True, dropna=False)
    result = grouped.agg(
        Employees=("AttritionFlag", "size"),
        Leavers=("AttritionFlag", "sum"),
        AverageMonthlyIncome=("MonthlyIncome", "mean"),
    ).reset_index()
    result["AttritionRate"] = result["Leavers"] / result["Employees"]
    leavers = data.loc[data["AttritionFlag"].eq(1)]
    costs = leavers.groupby(dimension, observed=True).agg(
        CostLow=("ReplacementCostLow", "sum"),
        CostBase=("ReplacementCostBase", "sum"),
        CostHigh=("ReplacementCostHigh", "sum"),
    ).reset_index()
    result = result.merge(costs, on=dimension, how="left").fillna(
        {"CostLow": 0.0, "CostBase": 0.0, "CostHigh": 0.0}
    )
    return result.sort_values("AttritionRate", ascending=False).reset_index(drop=True)


def build_assets() -> dict[str, object]:
    if not RAW.exists():
        raise FileNotFoundError(f"Source CSV not found: {RAW}")
    raw = pd.read_csv(RAW, encoding="utf-8-sig")
    if raw.shape != (1470, 35):
        raise ValueError(f"Expected source shape (1470, 35), received {raw.shape}")

    data = prepare_employees(raw)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    data.to_csv(PROCESSED / "employees_clean.csv", index=False)

    summary_files = {
        "department_summary.csv": summarize(data, "Department"),
        "tenure_summary.csv": summarize(data, "TenureBand"),
        "overtime_summary.csv": summarize(data, "OverTime"),
        "role_summary.csv": summarize(data, "JobRole"),
        "salary_band_summary.csv": summarize(data, "SalaryBand"),
    }
    for filename, summary in summary_files.items():
        summary.to_csv(PROCESSED / filename, index=False)

    total = len(data)
    leavers = int(data["AttritionFlag"].sum())
    result = {
        "source_rows": total,
        "source_columns": len(raw.columns),
        "leavers": leavers,
        "attrition_rate": leavers / total,
        "cost_assumptions": {"low": 0.25, "base": 0.50, "high": 0.75},
        "currency": "Not specified by source; displayed as dataset income units",
    }
    (PROCESSED / "summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(build_assets(), indent=2))
