-- ================================================================
-- Consumer360: Optimized Data Extraction for RFM Analysis
-- Week 1: Data Engineering & Schema
-- ================================================================
-- This script extracts cleaned, aggregated customer transaction data
-- for RFM (Recency, Frequency, Monetary) analysis
-- Target: Execute in under 2 seconds
-- ================================================================

SET NOCOUNT ON;
GO

-- ================================================================
-- Extract RFM Base Data
-- Returns one row per customer with R, F, M metrics
-- ================================================================

WITH CustomerMetrics AS (
    SELECT 
        c.CustomerKey,
        c.CustomerID,
        c.CustomerName,
        c.Email,
        c.SignUpDate,
        c.FirstPurchaseDate,
        
        -- RECENCY: Days since last purchase
        DATEDIFF(DAY, MAX(s.OrderDate), GETDATE()) AS DaysSinceLastPurchase,
        
        -- FREQUENCY: Number of completed orders
        COUNT(DISTINCT CASE WHEN s.OrderStatus = 'Completed' THEN s.TransactionID END) AS TotalOrders,
        
        -- MONETARY: Total revenue from completed orders
        SUM(CASE WHEN s.OrderStatus = 'Completed' THEN s.TotalAmount ELSE 0 END) AS TotalRevenue,
        
        -- Additional metrics
        AVG(CASE WHEN s.OrderStatus = 'Completed' THEN s.TotalAmount END) AS AvgOrderValue,
        MIN(s.OrderDate) AS FirstOrderDate,
        MAX(s.OrderDate) AS LastOrderDate,
        COUNT(DISTINCT CASE WHEN s.OrderStatus = 'Returned' THEN s.TransactionID END) AS ReturnedOrders,
        COUNT(DISTINCT CASE WHEN s.OrderStatus = 'Cancelled' THEN s.TransactionID END) AS CancelledOrders
        
    FROM Dim_Customer c
    LEFT JOIN Fact_Sales s ON c.CustomerKey = s.CustomerKey
    GROUP BY 
        c.CustomerKey, c.CustomerID, c.CustomerName, 
        c.Email, c.SignUpDate, c.FirstPurchaseDate
)
SELECT 
    CustomerKey,
    CustomerID,
    CustomerName,
    Email,
    SignUpDate,
    FirstPurchaseDate,
    DaysSinceLastPurchase,
    TotalOrders,
    CAST(TotalRevenue AS DECIMAL(12,2)) AS TotalRevenue,
    CAST(AvgOrderValue AS DECIMAL(10,2)) AS AvgOrderValue,
    FirstOrderDate,
    LastOrderDate,
    DATEDIFF(DAY, FirstOrderDate, LastOrderDate) AS CustomerLifespanDays,
    ReturnedOrders,
    CancelledOrders,
    CAST((CAST(ReturnedOrders AS FLOAT) / NULLIF(TotalOrders, 0)) * 100 AS DECIMAL(5,2)) AS ReturnRate
FROM CustomerMetrics
WHERE TotalOrders > 0  -- Only customers who have made at least one purchase
ORDER BY TotalRevenue DESC;
GO

-- ================================================================
-- VALIDATION QUERY: Check data quality
-- ================================================================
PRINT '========== Data Quality Check ==========';

-- Total customers with purchases
PRINT 'Customers with purchases: ' + 
    CAST((SELECT COUNT(DISTINCT CustomerKey) FROM Fact_Sales WHERE OrderStatus = 'Completed') AS VARCHAR);

-- Total revenue
PRINT 'Total Revenue: $' + 
    CAST((SELECT SUM(TotalAmount) FROM Fact_Sales WHERE OrderStatus = 'Completed') AS VARCHAR);

-- Date range
PRINT 'Date Range: ' + 
    CAST((SELECT MIN(OrderDate) FROM Fact_Sales) AS VARCHAR) + ' to ' +
    CAST((SELECT MAX(OrderDate) FROM Fact_Sales) AS VARCHAR);

PRINT '========================================';
GO
