-- ================================================================
-- Consumer360: Sample Data Generation
-- Week 1: Data Engineering & Schema
-- ================================================================
-- This script generates realistic sample data for testing
-- Generates ~10,000 transactions across 500 customers and 100 products
-- ================================================================

SET NOCOUNT ON;
GO

-- ================================================================
-- 1. INSERT SAMPLE REGIONS
-- ================================================================
INSERT INTO Dim_Region (RegionID, RegionName, Country, State, City, RegionalManager)
VALUES
    ('R001', 'North Region', 'USA', 'New York', 'New York City', 'John Smith'),
    ('R002', 'South Region', 'USA', 'Texas', 'Houston', 'Sarah Johnson'),
    ('R003', 'East Region', 'USA', 'Florida', 'Miami', 'Michael Brown'),
    ('R004', 'West Region', 'USA', 'California', 'Los Angeles', 'Emily Davis'),
    ('R005', 'Central Region', 'USA', 'Illinois', 'Chicago', 'David Wilson');
GO

-- ================================================================
-- 2. INSERT SAMPLE CUSTOMERS
-- ================================================================
DECLARE @i INT = 1;
DECLARE @SignUpDate DATE;
DECLARE @FirstPurchaseDate DATE;

WHILE @i <= 500
BEGIN
    SET @SignUpDate = DATEADD(DAY, -FLOOR(RAND() * 730), GETDATE()); -- Random date in last 2 years
    SET @FirstPurchaseDate = DATEADD(DAY, FLOOR(RAND() * 30), @SignUpDate);
    
    INSERT INTO Dim_Customer (CustomerID, CustomerName, Email, SignUpDate, FirstPurchaseDate, PreferredChannel)
    VALUES (
        'CUST' + RIGHT('00000' + CAST(@i AS VARCHAR), 5),
        'Customer ' + CAST(@i AS VARCHAR),
        'customer' + CAST(@i AS VARCHAR) + '@email.com',
        @SignUpDate,
        @FirstPurchaseDate,
        CASE FLOOR(RAND() * 3)
            WHEN 0 THEN 'Online'
            WHEN 1 THEN 'Mobile App'
            ELSE 'In-Store'
        END
    );
    
    SET @i = @i + 1;
END;
GO

-- ================================================================
-- 3. INSERT SAMPLE PRODUCTS
-- ================================================================
DECLARE @Categories TABLE (Category VARCHAR(50), SubCategory VARCHAR(50));
INSERT INTO @Categories VALUES
    ('Electronics', 'Smartphones'),
    ('Electronics', 'Laptops'),
    ('Electronics', 'Accessories'),
    ('Clothing', 'Men''s Wear'),
    ('Clothing', 'Women''s Wear'),
    ('Clothing', 'Kids Wear'),
    ('Home & Kitchen', 'Cookware'),
    ('Home & Kitchen', 'Furniture'),
    ('Books', 'Fiction'),
    ('Books', 'Non-Fiction'),
    ('Grocery', 'Snacks'),
    ('Grocery', 'Beverages'),
    ('Sports', 'Fitness Equipment'),
    ('Sports', 'Outdoor Gear');

DECLARE @j INT = 1;
DECLARE @Cat VARCHAR(50), @SubCat VARCHAR(50);

WHILE @j <= 100
BEGIN
    -- Randomly select category
    SELECT TOP 1 @Cat = Category, @SubCat = SubCategory 
    FROM @Categories 
    ORDER BY NEWID();
    
    INSERT INTO Dim_Product (ProductID, ProductName, Category, SubCategory, Brand, UnitPrice, Cost)
    VALUES (
        'PROD' + RIGHT('00000' + CAST(@j AS VARCHAR), 5),
        @SubCat + ' Item ' + CAST(@j AS VARCHAR),
        @Cat,
        @SubCat,
        'Brand ' + CAST((@j % 10) + 1 AS VARCHAR),
        ROUND(RAND() * 490 + 10, 2), -- Price between $10 and $500
        ROUND((RAND() * 490 + 10) * 0.6, 2) -- Cost is ~60% of price
    );
    
    SET @j = @j + 1;
END;
GO

-- ================================================================
-- 4. INSERT SAMPLE SALES TRANSACTIONS
-- ================================================================
DECLARE @k INT = 1;
DECLARE @CustomerKey INT;
DECLARE @ProductKey INT;
DECLARE @RegionKey INT;
DECLARE @OrderDate DATETIME;
DECLARE @DateKey INT;
DECLARE @Quantity INT;
DECLARE @UnitPrice DECIMAL(10,2);
DECLARE @Cost DECIMAL(10,2);
DECLARE @Discount DECIMAL(5,2);

WHILE @k <= 10000
BEGIN
    -- Random customer (some customers will have multiple purchases)
    SELECT TOP 1 @CustomerKey = CustomerKey FROM Dim_Customer ORDER BY NEWID();
    
    -- Random product
    SELECT TOP 1 @ProductKey = ProductKey, @UnitPrice = UnitPrice, @Cost = Cost 
    FROM Dim_Product ORDER BY NEWID();
    
    -- Random region
    SELECT TOP 1 @RegionKey = RegionKey FROM Dim_Region ORDER BY NEWID();
    
    -- Random order date (last 2 years)
    SET @OrderDate = DATEADD(DAY, -FLOOR(RAND() * 730), GETDATE());
    SET @DateKey = CAST(FORMAT(@OrderDate, 'yyyyMMdd') AS INT);
    
    -- Random quantity (1-5)
    SET @Quantity = FLOOR(RAND() * 5) + 1;
    
    -- Random discount (0%, 5%, 10%, 15%, or 20%)
    SET @Discount = CASE FLOOR(RAND() * 5)
        WHEN 0 THEN 0
        WHEN 1 THEN 5
        WHEN 2 THEN 10
        WHEN 3 THEN 15
        ELSE 20
    END;
    
    INSERT INTO Fact_Sales (
        TransactionID, CustomerKey, ProductKey, RegionKey, DateKey, OrderDate,
        ShipDate, Quantity, UnitPrice, Discount, TotalAmount, Cost,
        ShippingCost, PaymentMethod, OrderStatus
    )
    VALUES (
        'TXN' + RIGHT('00000000' + CAST(@k AS VARCHAR), 8),
        @CustomerKey,
        @ProductKey,
        @RegionKey,
        @DateKey,
        @OrderDate,
        DATEADD(DAY, FLOOR(RAND() * 7) + 1, @OrderDate), -- Ship 1-7 days after order
        @Quantity,
        @UnitPrice,
        @Discount,
        (@UnitPrice * @Quantity) * (1 - @Discount / 100),
        @Cost * @Quantity,
        ROUND(RAND() * 20 + 5, 2), -- Shipping $5-$25
        CASE FLOOR(RAND() * 4)
            WHEN 0 THEN 'Credit Card'
            WHEN 1 THEN 'Debit Card'
            WHEN 2 THEN 'PayPal'
            ELSE 'Cash'
        END,
        CASE FLOOR(RAND() * 10)
            WHEN 0 THEN 'Cancelled'
            WHEN 1 THEN 'Returned'
            ELSE 'Completed'
        END
    );
    
    SET @k = @k + 1;
    
    -- Print progress every 1000 rows
    IF @k % 1000 = 0
        PRINT 'Inserted ' + CAST(@k AS VARCHAR) + ' transactions...';
END;
GO

PRINT 'Sample data generation complete!';
PRINT 'Regions: ' + CAST((SELECT COUNT(*) FROM Dim_Region) AS VARCHAR);
PRINT 'Customers: ' + CAST((SELECT COUNT(*) FROM Dim_Customer) AS VARCHAR);
PRINT 'Products: ' + CAST((SELECT COUNT(*) FROM Dim_Product) AS VARCHAR);
PRINT 'Transactions: ' + CAST((SELECT COUNT(*) FROM Fact_Sales) AS VARCHAR);
GO
