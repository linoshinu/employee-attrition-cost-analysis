# Interview walkthrough

## 60-second version

“I built an end-to-end people analytics portfolio project around IBM's fictional 1,470-row attrition sample. I prepared a Tableau-ready dataset in Python, added SQL queries for department, tenure, overtime, job role, and replacement-cost views, and made an interactive dashboard with drill-down filters. I separated observed counts and rates from modeled costs: because the source has no recruiting invoices or vacancy data, I show a 25%, 50%, and 75% of annualized income sensitivity range rather than calling it a realized loss. The retention-budget page is a what-if model with user-controlled program cost and effect assumptions, not a causal prediction. My main takeaway is that analysts should show both the rate and cohort size, make assumptions visible, and identify what evidence the business needs before spending.”

## STAR outline

- **Situation:** A stakeholder needs to understand where attrition is concentrated and how to frame its possible financial exposure.
- **Task:** Build a clear, reproducible analysis that a non-technical audience can explore.
- **Action:** Prepared source data with Python; checked the target and dimensions; added tenure/salary bands and cost sensitivities; wrote SQL group queries; created an interactive dashboard and a Tableau build specification.
- **Result:** The project separates what the sample observes from what the scenario assumes, gives stakeholders filterable aggregate comparisons, and makes the follow-up data needs explicit.

Use only if it accurately reflects the work you personally reviewed and can explain. Be ready to walk through the code and change an assumption live.

This repository was created with AI assistance. Describe that honestly, and make sure you understand every query, calculation, and limitation before presenting it as your work. Do not describe this synthetic-data exercise as client or employer analysis.

## Questions an interviewer may ask

**Why use attrition rate and count together?**  
A rate helps compare departments of different sizes; the count and denominator show how much evidence supports that percentage and how many records it represents.

**How did you calculate the cost?**  
The data has monthly income but no direct replacement-cost field. I annualize income, then apply 25%, 50%, and 75% assumptions to each sample departure. That creates a transparent sensitivity range, not actual accounting cost.

**Can the dashboard say overtime causes attrition?**  
No. It is a cross-sectional fictional sample, and the chart is an association. It does not establish time ordering or rule out confounding. A real study would need longitudinal data and a careful design.

**How do you choose a retention budget strategy?**  
The scenario tool compares equal, leaver-weighted, and modeled-cost-weighted allocations under assumed participant cost and absolute effect. Its ranking is conditional. I would validate costs, test an intervention with a pilot and comparison group, and assess equity and employee experience before making a recommendation.

**Why not predict individual employees who may leave?**  
This project's goal is aggregate planning, and the source is not suitable for employee decisions. Individual predictions can create privacy and fairness harms and may not transfer to a real organization. The dashboard does not show risk scores or identify people.

**What would you request next from a client?**  
Monthly workforce snapshots and event dates, approved replacement-cost components, intervention eligibility and delivery records, employee feedback, and a pre-agreed outcome measure. Access should be minimized and aggregated wherever possible.

## Before the interview

- Run the app and explain one SQL query without reading from this guide.
- Change the cost percentage and show how the range changes.
- Explain why sample percentages are not forecasts and why the default budget ranking is not a business recommendation.
- If asked about Tableau, recreate the documented workbook in Tableau Public and save your own `.twb`/`.twbx` before claiming that file as an artifact.
