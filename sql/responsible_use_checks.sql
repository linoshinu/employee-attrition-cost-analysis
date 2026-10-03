-- These are descriptive group-level checks. Do not use them to rank individuals.

-- Attrition rate by broad age band and gender to make visible where the sample is
-- too small or imbalanced for simplistic comparisons. This is not a fairness audit.
SELECT
    CASE
        WHEN Age < 25 THEN 'Under 25'
        WHEN Age < 35 THEN '25-34'
        WHEN Age < 45 THEN '35-44'
        WHEN Age < 55 THEN '45-54'
        ELSE '55+'
    END AS age_band,
    Gender,
    COUNT(*) AS employees,
    SUM(AttritionFlag) AS leavers,
    1.0 * SUM(AttritionFlag) / COUNT(*) AS attrition_rate
FROM employee_attrition
GROUP BY age_band, Gender
ORDER BY age_band, Gender;
