-- Karoo Organics Capstone Project
-- This file contains the SQL queries used for the Q4 performance report.
-- The queries help management compare actual sales with targets
-- and identify the best performing suppliers in each region.

-- QUERY 1:
-- This query shows how each region performed against its Q4 sales target.
-- It adds up actual revenue from orders and compares it to the target amount.
-- CASE is used to avoid division by zero.

SELECT
    s.region,
    SUM(o.total_price) AS actual_revenue,
    st.target_amount,
    CASE
        WHEN st.target_amount = 0 THEN 0
        ELSE ROUND((SUM(o.total_price) / st.target_amount) * 100, 2)
    END AS percentage_of_target
FROM Suppliers s
JOIN Orders o
    ON s.supplier_id = o.supplier_id
JOIN Sales_Targets st
    ON s.region = st.region
WHERE st.quarter = '2025-Q4'
GROUP BY s.region, st.target_amount
ORDER BY percentage_of_target DESC;


-- QUERY 2:
-- This query ranks the top suppliers in each region by revenue.
-- RANK() gives each supplier a position within their own region.
-- PARTITION BY means the ranking starts again for every region.

SELECT
    region,
    farm_name,
    total_revenue,
    regional_rank
FROM (
    SELECT
        s.region,
        s.farm_name,
        SUM(o.total_price) AS total_revenue,
        RANK() OVER (
            PARTITION BY s.region
            ORDER BY SUM(o.total_price) DESC
        ) AS regional_rank
    FROM Suppliers s
    JOIN Orders o
        ON s.supplier_id = o.supplier_id
    GROUP BY s.region, s.farm_name
) ranked_suppliers
WHERE regional_rank <= 3
ORDER BY region, regional_rank;