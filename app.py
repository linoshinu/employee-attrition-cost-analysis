from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "processed" / "employees_clean.csv"
NAVY = "#17365D"
TEAL = "#167D8D"
GOLD = "#D59B32"

st.set_page_config(page_title="People Analytics | Attrition & Cost", page_icon="📊", layout="wide")
st.markdown(
    f"""
    <style>
      .block-container {{padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1450px;}}
      h1, h2, h3 {{color: {NAVY};}}
      [data-testid="stMetric"] {{background: #f5f8fb; border: 1px solid #e4ebf2;
        padding: 14px 16px; border-radius: 10px;}}
      .note {{background: #f2f7f8; border-left: 4px solid {TEAL}; padding: 12px 16px;
        border-radius: 4px; margin: 10px 0 18px 0;}}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_FILE)


def rate_table(frame: pd.DataFrame, dimension: str) -> pd.DataFrame:
    result = frame.groupby(dimension, observed=True).agg(
        Employees=("AttritionFlag", "size"),
        Leavers=("AttritionFlag", "sum"),
    ).reset_index()
    result["Attrition rate"] = result["Leavers"] / result["Employees"]
    return result


def style_chart(fig, y_title: str = ""):
    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="Arial, sans-serif", color="#273746"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title=y_title,
    )
    fig.update_yaxes(gridcolor="#e8edf2", zeroline=False)
    fig.update_xaxes(showgrid=False)
    return fig


def allocate_scenarios(frame: pd.DataFrame, budget: float, participant_cost: float, uplift_pp: float) -> pd.DataFrame:
    by_dept = frame.groupby("Department", observed=True).agg(
        Employees=("AttritionFlag", "size"),
        Leavers=("AttritionFlag", "sum"),
        Exposure=("ReplacementCostBase", lambda x: x[frame.loc[x.index, "AttritionFlag"].eq(1)].sum()),
    ).reset_index()
    if by_dept.empty:
        return pd.DataFrame()

    plans = {
        "Equal across departments": pd.Series(1.0, index=by_dept.index),
        "Weighted by sample leavers": by_dept["Leavers"].astype(float),
        "Weighted by modeled cost": by_dept["Exposure"].astype(float),
    }
    rows = []
    for name, weight in plans.items():
        if weight.sum() <= 0:
            continue
        planned = budget * weight / weight.sum()
        participants = (planned / participant_cost).astype(int).clip(upper=by_dept["Employees"])
        expected_prevented = (participants * uplift_pp / 100).clip(upper=by_dept["Leavers"])
        avg_exit_value = by_dept["Exposure"].div(by_dept["Leavers"].replace(0, pd.NA)).fillna(0)
        program_spend = participants * participant_cost
        modeled_value = expected_prevented * avg_exit_value
        spent = float(program_spend.sum())
        value = float(modeled_value.sum())
        rows.append({
            "Allocation plan": name,
            "Participants": int(participants.sum()),
            "Modeled exits avoided": float(expected_prevented.sum()),
            "Estimated program spend": spent,
            "Modeled cost avoided": value,
            "Modeled net value": value - spent,
            "Modeled net return": (value - spent) / spent if spent else 0.0,
        })
    return pd.DataFrame(rows).sort_values("Modeled net value", ascending=False)


st.title("Employee attrition & cost impact")
st.caption("A decision-support demonstration built with Python, SQL, and Tableau-ready data")
st.markdown(
    "<div class='note'><b>Read this first:</b> The IBM sample contains fictional records. "
    "Cost values are scenario estimates in unspecified dataset income units, not actual company losses. "
    "This aggregate dashboard does not predict or score individual employees.</div>",
    unsafe_allow_html=True,
)

if not DATA_FILE.exists():
    with st.spinner("Preparing the Tableau-ready data from the included source file…"):
        from scripts.build_assets import build_assets

        build_assets()
        load_data.clear()

data = load_data()
with st.sidebar:
    st.header("Explore the sample")
    departments = sorted(data["Department"].dropna().unique().tolist())
    roles = sorted(data["JobRole"].dropna().unique().tolist())
    tenure_bands = ["<1 year", "1-3 years", "4-5 years", "6-10 years", "11+ years"]
    selected_departments = st.multiselect("Department", departments, default=departments)
    selected_overtime = st.multiselect("Overtime", ["No", "Yes"], default=["No", "Yes"])
    selected_tenure = st.multiselect("Tenure", tenure_bands, default=tenure_bands)
    selected_roles = st.multiselect("Job role", roles, default=roles)
    st.caption("Each chart updates to the selected groups. Small cohorts should be interpreted carefully.")

filtered = data[
    data["Department"].isin(selected_departments)
    & data["OverTime"].isin(selected_overtime)
    & data["TenureBand"].isin(selected_tenure)
    & data["JobRole"].isin(selected_roles)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Widen one or more selections.")
    st.stop()

sample_size = len(filtered)
leavers = int(filtered["AttritionFlag"].sum())
attrition_rate = leavers / sample_size
base_exposure = float(filtered.loc[filtered["AttritionFlag"].eq(1), "ReplacementCostBase"].sum())
low_exposure = float(filtered.loc[filtered["AttritionFlag"].eq(1), "ReplacementCostLow"].sum())
high_exposure = float(filtered.loc[filtered["AttritionFlag"].eq(1), "ReplacementCostHigh"].sum())

metric_cols = st.columns(4)
metric_cols[0].metric("Sample employees", f"{sample_size:,}")
metric_cols[1].metric("Sample leavers", f"{leavers:,}")
metric_cols[2].metric("Observed attrition rate", f"{attrition_rate:.1%}")
metric_cols[3].metric("Base cost proxy", f"{base_exposure:,.0f} units")
st.caption(
    f"Estimated replacement-cost range for the filtered sample: {low_exposure:,.0f} to "
    f"{high_exposure:,.0f} dataset income units. Base case: {base_exposure:,.0f}."
)

overview, scenarios, definitions = st.tabs(["Attrition patterns", "Budget scenarios", "About this analysis"])

with overview:
    left, right = st.columns(2)
    with left:
        dept = rate_table(filtered, "Department").sort_values("Attrition rate", ascending=True)
        fig = px.bar(
            dept,
            x="Attrition rate",
            y="Department",
            orientation="h",
            text=dept["Attrition rate"].map(lambda x: f"{x:.1%}"),
            hover_data={"Employees": True, "Leavers": True, "Attrition rate": ":.1%"},
            color="Attrition rate",
            color_continuous_scale=[[0, "#b9dce0"], [1, TEAL]],
            title="Attrition rate by department",
        )
        st.plotly_chart(style_chart(fig, ""), use_container_width=True)
    with right:
        tenure_order = [x for x in tenure_bands if x in filtered["TenureBand"].unique()]
        tenure = rate_table(filtered, "TenureBand")
        tenure["TenureBand"] = pd.Categorical(tenure["TenureBand"], tenure_order, ordered=True)
        tenure = tenure.sort_values("TenureBand")
        fig = px.bar(
            tenure,
            x="TenureBand",
            y="Attrition rate",
            text=tenure["Attrition rate"].map(lambda x: f"{x:.1%}"),
            hover_data={"Employees": True, "Leavers": True, "Attrition rate": ":.1%"},
            color_discrete_sequence=[GOLD],
            title="Attrition rate by tenure band",
        )
        st.plotly_chart(style_chart(fig, "Rate"), use_container_width=True)

    left, right = st.columns(2)
    with left:
        overtime = rate_table(filtered, "OverTime").sort_values("OverTime")
        fig = px.bar(
            overtime,
            x="OverTime",
            y="Attrition rate",
            text=overtime["Attrition rate"].map(lambda x: f"{x:.1%}"),
            hover_data={"Employees": True, "Leavers": True, "Attrition rate": ":.1%"},
            color="OverTime",
            color_discrete_map={"No": "#a9cbd1", "Yes": TEAL},
            title="Overtime comparison",
        )
        st.plotly_chart(style_chart(fig, "Rate"), use_container_width=True)
    with right:
        roles_view = rate_table(filtered, "JobRole").sort_values("Attrition rate")
        fig = px.bar(
            roles_view,
            x="Attrition rate",
            y="JobRole",
            orientation="h",
            text=roles_view["Attrition rate"].map(lambda x: f"{x:.1%}"),
            hover_data={"Employees": True, "Leavers": True, "Attrition rate": ":.1%"},
            color_discrete_sequence=[NAVY],
            title="Attrition rate by job role",
        )
        st.plotly_chart(style_chart(fig, ""), use_container_width=True)

    dept_cost = filtered.groupby("Department", observed=True).agg(
        Employees=("AttritionFlag", "size"),
        Leavers=("AttritionFlag", "sum"),
        CostLow=("ReplacementCostLow", lambda x: x[filtered.loc[x.index, "AttritionFlag"].eq(1)].sum()),
        CostBase=("ReplacementCostBase", lambda x: x[filtered.loc[x.index, "AttritionFlag"].eq(1)].sum()),
        CostHigh=("ReplacementCostHigh", lambda x: x[filtered.loc[x.index, "AttritionFlag"].eq(1)].sum()),
    ).reset_index().sort_values("CostBase")
    st.subheader("Modeled replacement-cost exposure")
    st.caption("Low/base/high cases are 25% / 50% / 75% of annualized income per sample departure.")
    fig = px.bar(
        dept_cost,
        x="CostBase",
        y="Department",
        orientation="h",
        error_x=dept_cost["CostHigh"] - dept_cost["CostBase"],
        error_x_minus=dept_cost["CostBase"] - dept_cost["CostLow"],
        hover_data={"Employees": True, "Leavers": True, "CostBase": ":,.0f"},
        color_discrete_sequence=[TEAL],
        title="Cost range by department (dataset income units)",
    )
    st.plotly_chart(style_chart(fig, ""), use_container_width=True)

with scenarios:
    st.subheader("Compare allocation approaches")
    st.markdown(
        "This what-if model assumes each funded participant gets the same improvement. "
        "It does not estimate a program effect from the sample. Change the assumptions and treat the ranking as conditional."
    )
    controls = st.columns(3)
    budget = controls[0].number_input("Total budget (dataset units)", min_value=1000, max_value=2_000_000, value=100_000, step=5_000)
    participant_cost = controls[1].number_input("Assumed cost per participant", min_value=100, max_value=100_000, value=2_000, step=500)
    uplift_pp = controls[2].slider("Assumed absolute attrition reduction (pp)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    scenario = allocate_scenarios(filtered, float(budget), float(participant_cost), float(uplift_pp))
    if scenario.empty:
        st.info("Select records with sample leavers to compare cost-weighted strategies.")
    else:
        winner = scenario.iloc[0]
        st.markdown(
            f"<div class='note'>Under the current assumptions, <b>{winner['Allocation plan']}</b> has the "
            f"highest modeled net value. This is not evidence that it will work in a real workforce.</div>",
            unsafe_allow_html=True,
        )
        display = scenario.copy()
        display["Modeled exits avoided"] = display["Modeled exits avoided"].map(lambda x: f"{x:.1f}")
        for column in ["Estimated program spend", "Modeled cost avoided", "Modeled net value"]:
            display[column] = display[column].map(lambda x: f"{x:,.0f}")
        display["Modeled net return"] = display["Modeled net return"].map(lambda x: f"{x:.1%}")
        st.dataframe(display, hide_index=True, use_container_width=True)
        st.caption(
            "Calculation: funded participants = allocated budget / assumed cost per participant; "
            "expected exits avoided = participants × assumed percentage-point reduction, capped at observed sample leavers; "
            "modeled value = expected exits avoided × average base-case cost proxy for sample leavers."
        )
        st.markdown(
            "**Before using this model for a real budget:** validate replacement costs with Finance, estimate effects from a "
            "well-designed pilot, and review privacy, equity, and employee feedback with HR."
        )

with definitions:
    st.subheader("Metric definitions")
    st.markdown(
        "- **Observed attrition rate:** sample rows marked `Attrition = Yes` divided by all selected sample rows.\n"
        "- **Annualized income:** `MonthlyIncome × 12`. The data source does not specify a currency.\n"
        "- **Replacement-cost proxy:** annualized income multiplied by an illustrative 25%, 50%, or 75% scenario.\n"
        "- **Tenure band:** `<1`, `1-3`, `4-5`, `6-10`, and `11+` years at the company.\n"
        "- **Salary band:** thirds of the sample's monthly-income distribution, for descriptive comparison."
    )
    st.subheader("What the data can and cannot say")
    st.markdown(
        "The sample has 1,470 fictional rows and one attrition label per row. It supports group-level description and "
        "a transparent scenario exercise. It has no event dates, recruitment invoices, vacancy duration, intervention "
        "records, or follow-up outcomes. It therefore cannot identify causes, forecast future losses, or estimate the "
        "effectiveness of a retention program. Use the findings as questions for a real pilot, not as employee decisions."
    )
    st.markdown("Source: [IBM HR Analytics sample on Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset). See `data/DATA_LICENSE.md`.")

st.divider()
st.caption("Portfolio demonstration • Python + SQL + Tableau-ready CSV • Fictional data • Aggregate decision support only")
