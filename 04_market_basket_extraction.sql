-- ================================================================
-- Consumer360: Market Basket Analysis Data Extraction
-- Week 1: Data Engineering & Schema
-- ================================================================
-- This script extracts transactional data for Market Basket Analysis
-- Format: Transaction ID with all products purchased together
-- ================================================================

SET NOCOUNT ON;
GO

-- ================================================================
-- Extract Transaction-Product Pairs for Market Basket Analysis
-- ================================================================

SELECT 
    s.TransactionID,
    s.OrderDate,
    c.CustomerID,
    p.ProductID,
    p.ProductName,
    p.Category,
    p.SubCategory,
    s.Quantity,
    s.TotalAmount
FROM Fact_Sales s
INNER JOIN Dim_Customer c ON s.CustomerKey = c.CustomerKey
INNER JOIN Dim_Product p ON s.ProductKey = p.ProductKey
WHERE s.OrderStatus = 'Completed'
ORDER BY s.TransactionID, p.ProductID;
GO

-- ================================================================
-- Product Co-occurrence Matrix (for quick insights)
-- Shows which products are frequently bought together
-- ================================================================

WITH ProductPairs AS (
    SELECT 
        s1.TransactionID,
        p1.ProductName AS Product1,
        p2.ProductName AS Product2,
        p1.Category AS Category1,
        p2.Category AS Category2
    FROM Fact_Sales s1
    INNER JOIN Fact_Sales s2 ON s1.TransactionID = s2.TransactionID AND s1.ProductKey < s2.ProductKey
    INNER JOIN Dim_Product p1 ON s1.ProductKey = p1.ProductKey
    INNER JOIN Dim_Product p2 ON s2.ProductKey = p2.ProductKey
    WHERE s1.OrderStatus = 'Completed' AND s2.OrderStatus = 'Completed'
)
SELECT 
    Product1,
    Product2,
    Category1,
    Category2,
    COUNT(*) AS CoOccurrenceCount,
    CAST(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT TransactionID) FROM Fact_Sales WHERE OrderStatus = 'Completed') AS DECIMAL(5,2)) AS CoOccurrencePercentage
FROM ProductPairs
GROUP BY Product1, Product2, Category1, Category2
HAVING COUNT(*) >= 3  -- Only show pairs that occur at least 3 times
ORDER BY CoOccurrenceCount DESC;
GO

PRINT 'Market Basket data extracted successfully!';
GO
