-- ================================================================
-- Consumer360: Star Schema Definition
-- Week 1: Data Engineering & Schema
-- ================================================================
-- This script creates the Star Schema with:
-- - Fact_Sales (central fact table)
-- - Dim_Customer (customer dimension)
-- - Dim_Product (product dimension)
-- - Dim_Date (date dimension)
-- - Dim_Region (geographical dimension)
-- ================================================================

-- Enable performance optimizations
SET NOCOUNT ON;
GO

-- ================================================================
-- 1. DIM_CUSTOMER - Customer Dimension
-- ================================================================
IF OBJECT_ID('Dim_Customer', 'U') IS NOT NULL
    DROP TABLE Dim_Customer;
GO

CREATE TABLE Dim_Customer (
    CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID VARCHAR(50) NOT NULL UNIQUE,
    CustomerName NVARCHAR(100),
    Email NVARCHAR(100),
    PhoneNumber VARCHAR(20),
    SignUpDate DATE,
    FirstPurchaseDate DATE,
    CustomerStatus VARCHAR(20) DEFAULT 'Active', -- Active, Inactive, Churned
    PreferredChannel VARCHAR(50),
    CreatedDate DATETIME DEFAULT GETDATE(),
    UpdatedDate DATETIME DEFAULT GETDATE(),
    -- Business key index for lookups
    INDEX IX_CustomerID NONCLUSTERED (CustomerID)
);
GO

-- ================================================================
-- 2. DIM_PRODUCT - Product Dimension
-- ================================================================
IF OBJECT_ID('Dim_Product', 'U') IS NOT NULL
    DROP TABLE Dim_Product;
GO

CREATE TABLE Dim_Product (
    ProductKey INT IDENTITY(1,1) PRIMARY KEY,
    ProductID VARCHAR(50) NOT NULL UNIQUE,
    ProductName NVARCHAR(200),
    Category NVARCHAR(100),
    SubCategory NVARCHAR(100),
    Brand NVARCHAR(100),
    UnitPrice DECIMAL(10,2),
    Cost DECIMAL(10,2),
    ProductStatus VARCHAR(20) DEFAULT 'Active', -- Active, Discontinued
    CreatedDate DATETIME DEFAULT GETDATE(),
    UpdatedDate DATETIME DEFAULT GETDATE(),
    -- Business key index
    INDEX IX_ProductID NONCLUSTERED (ProductID)
);
GO

-- ================================================================
-- 3. DIM_REGION - Geographical Dimension
-- ================================================================
IF OBJECT_ID('Dim_Region', 'U') IS NOT NULL
    DROP TABLE Dim_Region;
GO

CREATE TABLE Dim_Region (
    RegionKey INT IDENTITY(1,1) PRIMARY KEY,
    RegionID VARCHAR(50) NOT NULL UNIQUE,
    RegionName NVARCHAR(100),
    Country NVARCHAR(100),
    State NVARCHAR(100),
    City NVARCHAR(100),
    PostalCode VARCHAR(20),
    RegionalManager NVARCHAR(100),
    CreatedDate DATETIME DEFAULT GETDATE(),
    INDEX IX_RegionID NONCLUSTERED (RegionID)
);
GO

-- ================================================================
-- 4. DIM_DATE - Date Dimension (for time intelligence)
-- ================================================================
IF OBJECT_ID('Dim_Date', 'U') IS NOT NULL
    DROP TABLE Dim_Date;
GO

CREATE TABLE Dim_Date (
    DateKey INT PRIMARY KEY,
    FullDate DATE NOT NULL UNIQUE,
    DayOfWeek INT,
    DayName VARCHAR(10),
    DayOfMonth INT,
    DayOfYear INT,
    WeekOfYear INT,
    MonthNumber INT,
    MonthName VARCHAR(10),
    Quarter INT,
    Year INT,
    IsWeekend BIT,
    IsHoliday BIT DEFAULT 0,
    FiscalYear INT,
    FiscalQuarter INT
);
GO

-- ================================================================
-- 5. FACT_SALES - Central Fact Table
-- ================================================================
IF OBJECT_ID('Fact_Sales', 'U') IS NOT NULL
    DROP TABLE Fact_Sales;
GO

CREATE TABLE Fact_Sales (
    SalesKey BIGINT IDENTITY(1,1) PRIMARY KEY,
    TransactionID VARCHAR(50) NOT NULL,
    CustomerKey INT NOT NULL,
    ProductKey INT NOT NULL,
    RegionKey INT NOT NULL,
    DateKey INT NOT NULL,
    OrderDate DATETIME NOT NULL,
    ShipDate DATETIME,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    Discount DECIMAL(5,2) DEFAULT 0,
    TotalAmount DECIMAL(12,2) NOT NULL,
    Cost DECIMAL(12,2),
    Profit AS (TotalAmount - Cost) PERSISTED,
    ShippingCost DECIMAL(8,2),
    PaymentMethod VARCHAR(50),
    OrderStatus VARCHAR(20), -- Completed, Cancelled, Returned
    CreatedDate DATETIME DEFAULT GETDATE(),
    
    -- Foreign Key Constraints
    CONSTRAINT FK_Sales_Customer FOREIGN KEY (CustomerKey) 
        REFERENCES Dim_Customer(CustomerKey),
    CONSTRAINT FK_Sales_Product FOREIGN KEY (ProductKey) 
        REFERENCES Dim_Product(ProductKey),
    CONSTRAINT FK_Sales_Region FOREIGN KEY (RegionKey) 
        REFERENCES Dim_Region(RegionKey),
    CONSTRAINT FK_Sales_Date FOREIGN KEY (DateKey) 
        REFERENCES Dim_Date(DateKey),
    
    -- Performance Indexes (critical for sub-2-second queries)
    INDEX IX_Sales_Customer NONCLUSTERED (CustomerKey) INCLUDE (TotalAmount, OrderDate),
    INDEX IX_Sales_Product NONCLUSTERED (ProductKey) INCLUDE (Quantity, TotalAmount),
    INDEX IX_Sales_Date NONCLUSTERED (DateKey) INCLUDE (TotalAmount),
    INDEX IX_Sales_OrderDate NONCLUSTERED (OrderDate) INCLUDE (CustomerKey, TotalAmount)
);
GO

-- ================================================================
-- UTILITY: Populate Dim_Date (2020-2030)
-- ================================================================
DECLARE @StartDate DATE = '2020-01-01';
DECLARE @EndDate DATE = '2030-12-31';

WHILE @StartDate <= @EndDate
BEGIN
    INSERT INTO Dim_Date (
        DateKey, FullDate, DayOfWeek, DayName, DayOfMonth, DayOfYear,
        WeekOfYear, MonthNumber, MonthName, Quarter, Year, IsWeekend,
        FiscalYear, FiscalQuarter
    )
    VALUES (
        CAST(FORMAT(@StartDate, 'yyyyMMdd') AS INT),
        @StartDate,
        DATEPART(WEEKDAY, @StartDate),
        DATENAME(WEEKDAY, @StartDate),
        DAY(@StartDate),
        DATEPART(DAYOFYEAR, @StartDate),
        DATEPART(WEEK, @StartDate),
        MONTH(@StartDate),
        DATENAME(MONTH, @StartDate),
        DATEPART(QUARTER, @StartDate),
        YEAR(@StartDate),
        CASE WHEN DATEPART(WEEKDAY, @StartDate) IN (1, 7) THEN 1 ELSE 0 END,
        CASE WHEN MONTH(@StartDate) >= 4 THEN YEAR(@StartDate) ELSE YEAR(@StartDate) - 1 END,
        CASE 
            WHEN MONTH(@StartDate) IN (4, 5, 6) THEN 1
            WHEN MONTH(@StartDate) IN (7, 8, 9) THEN 2
            WHEN MONTH(@StartDate) IN (10, 11, 12) THEN 3
            ELSE 4
        END
    );
    
    SET @StartDate = DATEADD(DAY, 1, @StartDate);
END;
GO

PRINT 'Star Schema created successfully!';
PRINT 'Tables created: Dim_Customer, Dim_Product, Dim_Region, Dim_Date, Fact_Sales';
GO
