-- ================================================================
-- Consumer360: Cohort Analysis Data Extraction
-- Week 1: Data Engineering & Schema
-- ================================================================
-- This script extracts data for cohort retention analysis
-- Cohorts are based on the month of first purchase
-- ================================================================

SET NOCOUNT ON;
GO

-- ================================================================
-- Cohort Retention Analysis
-- Tracks customer retention by first purchase month
-- ================================================================

WITH CustomerCohort AS (
    -- Assign each customer to a cohort based on first purchase month
    SELECT 
        c.CustomerKey,
        c.CustomerID,
        MIN(s.OrderDate) AS FirstPurchaseDate,
        FORMAT(MIN(s.OrderDate), 'yyyy-MM') AS CohortMonth,
        DATEDIFF(MONTH, MIN(s.OrderDate), GETDATE()) AS CohortAge
    FROM Dim_Customer c
    INNER JOIN Fact_Sales s ON c.CustomerKey = s.CustomerKey
    WHERE s.OrderStatus = 'Completed'
    GROUP BY c.CustomerKey, c.CustomerID
),
CustomerActivity AS (
    -- Get all purchase months for each customer
    SELECT DISTINCT
        s.CustomerKey,
        FORMAT(s.OrderDate, 'yyyy-MM') AS PurchaseMonth,
        s.OrderDate
    FROM Fact_Sales s
    WHERE s.OrderStatus = 'Completed'
),
CohortActivity AS (
    -- Calculate months since first purchase for each activity
    SELECT 
        cc.CohortMonth,
        ca.CustomerKey,
        ca.PurchaseMonth,
        DATEDIFF(MONTH, cc.FirstPurchaseDate, ca.OrderDate) AS MonthsSinceFirstPurchase
    FROM CustomerCohort cc
    INNER JOIN CustomerActivity ca ON cc.CustomerKey = ca.CustomerKey
)
-- Create retention matrix
SELECT 
    CohortMonth,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 0 THEN CustomerKey END) AS Month_0,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 1 THEN CustomerKey END) AS Month_1,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 2 THEN CustomerKey END) AS Month_2,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 3 THEN CustomerKey END) AS Month_3,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 4 THEN CustomerKey END) AS Month_4,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 5 THEN CustomerKey END) AS Month_5,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 6 THEN CustomerKey END) AS Month_6,
    COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase >= 7 THEN CustomerKey END) AS Month_7_Plus,
    
    -- Retention rates (as percentages)
    CAST(COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 1 THEN CustomerKey END) * 100.0 / 
         NULLIF(COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 0 THEN CustomerKey END), 0) AS DECIMAL(5,2)) AS RetentionRate_Month1,
    
    CAST(COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 3 THEN CustomerKey END) * 100.0 / 
         NULLIF(COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 0 THEN CustomerKey END), 0) AS DECIMAL(5,2)) AS RetentionRate_Month3,
    
    CAST(COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 6 THEN CustomerKey END) * 100.0 / 
         NULLIF(COUNT(DISTINCT CASE WHEN MonthsSinceFirstPurchase = 0 THEN CustomerKey END), 0) AS DECIMAL(5,2)) AS RetentionRate_Month6
FROM CohortActivity
GROUP BY CohortMonth
ORDER BY CohortMonth DESC;
GO

PRINT 'Cohort analysis data extracted successfully!';
GO
