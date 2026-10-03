-- Load the table first: python scripts/load_sqlite.py
-- SQLite table: employee_attrition (one row per fictional sample record)

-- 1. Sample size, leavers, and overall attrition rate.
SELECT
    COUNT(*) AS employees,
    SUM(AttritionFlag) AS leavers,
    1.0 * SUM(AttritionFlag) / COUNT(*) AS attrition_rate
FROM employee_attrition;

-- 2. Department view: show both rates and counts to avoid small-group misreading.
SELECT
    Department,
    COUNT(*) AS employees,
    SUM(AttritionFlag) AS leavers,
    1.0 * SUM(AttritionFlag) / COUNT(*) AS attrition_rate,
    SUM(CASE WHEN AttritionFlag = 1 THEN ReplacementCostBase ELSE 0 END) AS modeled_cost_base
FROM employee_attrition
GROUP BY Department
ORDER BY attrition_rate DESC;

-- 3. Overtime comparison. This is descriptive association, not a causal effect.
SELECT
    OverTime,
    COUNT(*) AS employees,
    SUM(AttritionFlag) AS leavers,
    1.0 * SUM(AttritionFlag) / COUNT(*) AS attrition_rate
FROM employee_attrition
GROUP BY OverTime
ORDER BY OverTime;

-- 4. Tenure cohorts.
SELECT
    TenureBand,
    COUNT(*) AS employees,
    SUM(AttritionFlag) AS leavers,
    1.0 * SUM(AttritionFlag) / COUNT(*) AS attrition_rate,
    SUM(CASE WHEN AttritionFlag = 1 THEN ReplacementCostBase ELSE 0 END) AS modeled_cost_base
FROM employee_attrition
GROUP BY TenureBand
ORDER BY MIN(YearsAtCompany);

-- 5. Job-role view; interpret rates with cohort sizes.
SELECT
    JobRole,
    COUNT(*) AS employees,
    SUM(AttritionFlag) AS leavers,
    1.0 * SUM(AttritionFlag) / COUNT(*) AS attrition_rate
FROM employee_attrition
GROUP BY JobRole
ORDER BY attrition_rate DESC;

-- 6. Replacement-cost sensitivity range, counted only for sample rows marked Yes.
SELECT
    SUM(CASE WHEN AttritionFlag = 1 THEN ReplacementCostLow ELSE 0 END) AS modeled_low,
    SUM(CASE WHEN AttritionFlag = 1 THEN ReplacementCostBase ELSE 0 END) AS modeled_base,
    SUM(CASE WHEN AttritionFlag = 1 THEN ReplacementCostHigh ELSE 0 END) AS modeled_high
FROM employee_attrition;

-- 7. Salary band distribution.
SELECT
    SalaryBand,
    COUNT(*) AS employees,
    SUM(AttritionFlag) AS leavers,
    1.0 * SUM(AttritionFlag) / COUNT(*) AS attrition_rate
FROM employee_attrition
GROUP BY SalaryBand
ORDER BY SalaryBand;
