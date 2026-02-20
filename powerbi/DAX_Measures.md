# Consumer360: Power BI DAX Measures
# Week 3: Dashboard Construction
# ================================================================

## IMPORTANT: Copy these DAX measures into Power BI Desktop

---

## 1. BASIC CORE METRICS

### Total Revenue
```DAX
Total Revenue = 
SUM(Fact_Sales[TotalAmount])
```

### Total Orders
```DAX
Total Orders = 
COUNTROWS(Fact_Sales)
```

### Total Customers
```DAX
Total Customers = 
DISTINCTCOUNT(Fact_Sales[CustomerKey])
```

### Average Order Value
```DAX
Average Order Value = 
DIVIDE([Total Revenue], [Total Orders], 0)
```

### Total Profit
```DAX
Total Profit = 
SUM(Fact_Sales[Profit])
```

### Profit Margin %
```DAX
Profit Margin % = 
DIVIDE([Total Profit], [Total Revenue], 0) * 100
```

---

## 2. TIME INTELLIGENCE MEASURES

### Revenue Last Year
```DAX
Revenue LY = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(Dim_Date[FullDate])
)
```

### Revenue Year-over-Year Growth
```DAX
Revenue YoY Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue LY],
    [Revenue LY],
    0
) * 100
```

### Revenue Month-over-Month Growth
```DAX
Revenue MoM Growth % = 
VAR CurrentMonthRevenue = [Total Revenue]
VAR PreviousMonthRevenue = 
    CALCULATE(
        [Total Revenue],
        DATEADD(Dim_Date[FullDate], -1, MONTH)
    )
RETURN
    DIVIDE(
        CurrentMonthRevenue - PreviousMonthRevenue,
        PreviousMonthRevenue,
        0
    ) * 100
```

### Year-to-Date Revenue
```DAX
Revenue YTD = 
TOTALYTD(
    [Total Revenue],
    Dim_Date[FullDate]
)
```

### Moving Average (3 Month)
```DAX
Revenue 3M Moving Avg = 
AVERAGEX(
    DATESINPERIOD(
        Dim_Date[FullDate],
        LASTDATE(Dim_Date[FullDate]),
        -3,
        MONTH
    ),
    [Total Revenue]
)
```

---

## 3. RFM ANALYSIS MEASURES

### Average Recency Score
```DAX
Avg Recency Score = 
AVERAGE(RFM_Segmentation[R_Score])
```

### Average Frequency Score
```DAX
Avg Frequency Score = 
AVERAGE(RFM_Segmentation[F_Score])
```

### Average Monetary Score
```DAX
Avg Monetary Score = 
AVERAGE(RFM_Segmentation[M_Score])
```

### Champion Customers Count
```DAX
Champion Customers = 
CALCULATE(
    DISTINCTCOUNT(RFM_Segmentation[CustomerKey]),
    RFM_Segmentation[Segment] = "Champions"
)
```

### At Risk Customers Count
```DAX
At Risk Customers = 
CALCULATE(
    DISTINCTCOUNT(RFM_Segmentation[CustomerKey]),
    RFM_Segmentation[Segment] IN {"Can't Lose Them", "About To Sleep", "Hibernating"}
)
```

### Champion Revenue Contribution %
```DAX
Champion Revenue % = 
VAR ChampionRevenue = 
    CALCULATE(
        SUM(RFM_Segmentation[TotalRevenue]),
        RFM_Segmentation[Segment] = "Champions"
    )
VAR TotalRevenue = SUM(RFM_Segmentation[TotalRevenue])
RETURN
    DIVIDE(ChampionRevenue, TotalRevenue, 0) * 100
```

---

## 4. CUSTOMER METRICS

### Customer Lifetime Value (Simple)
```DAX
Customer LTV = 
CALCULATE(
    SUM(Fact_Sales[TotalAmount]),
    ALLEXCEPT(Fact_Sales, Fact_Sales[CustomerKey])
)
```

### Average Customer Lifespan (Days)
```DAX
Avg Customer Lifespan = 
AVERAGEX(
    VALUES(Dim_Customer[CustomerKey]),
    DATEDIFF(
        RELATED(Dim_Customer[FirstPurchaseDate]),
        TODAY(),
        DAY
    )
)
```

### Repeat Customer Rate %
```DAX
Repeat Customer Rate % = 
VAR RepeatCustomers = 
    CALCULATE(
        DISTINCTCOUNT(Fact_Sales[CustomerKey]),
        FILTER(
            SUMMARIZE(
                Fact_Sales,
                Fact_Sales[CustomerKey],
                "OrderCount", COUNTROWS(Fact_Sales)
            ),
            [OrderCount] > 1
        )
    )
VAR TotalCustomers = DISTINCTCOUNT(Fact_Sales[CustomerKey])
RETURN
    DIVIDE(RepeatCustomers, TotalCustomers, 0) * 100
```

### Customer Acquisition Cost (Placeholder)
```DAX
Customer Acquisition Cost = 
-- This would be calculated based on marketing spend data
-- Placeholder: Total Marketing Spend / New Customers
0  -- Update with actual marketing data
```

---

## 5. PRODUCT PERFORMANCE

### Top Product by Revenue
```DAX
Top Product = 
TOPN(
    1,
    VALUES(Dim_Product[ProductName]),
    [Total Revenue],
    DESC
)
```

### Product Sold Count
```DAX
Products Sold = 
SUM(Fact_Sales[Quantity])
```

### Inventory Turnover Ratio
```DAX
Inventory Turnover = 
-- Cost of Goods Sold / Average Inventory Value
DIVIDE(
    SUM(Fact_Sales[Cost]),
    AVERAGE(Dim_Product[Cost]),
    0
)
```

---

## 6. REGIONAL PERFORMANCE

### Revenue by Region (Top)
```DAX
Top Region Revenue = 
CALCULATE(
    [Total Revenue],
    TOPN(
        1,
        ALL(Dim_Region[RegionName]),
        [Total Revenue],
        DESC
    )
)
```

### Regional Market Share %
```DAX
Regional Market Share % = 
DIVIDE(
    [Total Revenue],
    CALCULATE(
        [Total Revenue],
        ALL(Dim_Region)
    ),
    0
) * 100
```

---

## 7. COHORT ANALYSIS

### Cohort Size
```DAX
Cohort Size = 
CALCULATE(
    DISTINCTCOUNT(Dim_Customer[CustomerKey]),
    FILTER(
        Dim_Customer,
        FORMAT(Dim_Customer[FirstPurchaseDate], "YYYY-MM") = SELECTEDVALUE(Dim_Date[MonthName])
    )
)
```

### Cohort Retention Rate
```DAX
Cohort Retention Rate = 
VAR CohortMonth = SELECTEDVALUE(Dim_Date[MonthName])
VAR InitialCustomers = [Cohort Size]
VAR ActiveCustomers = 
    CALCULATE(
        DISTINCTCOUNT(Fact_Sales[CustomerKey]),
        Fact_Sales[OrderDate] >= TODAY() - 30
    )
RETURN
    DIVIDE(ActiveCustomers, InitialCustomers, 0) * 100
```

---

## 8. CHURN METRICS

### Churned Customers
```DAX
Churned Customers = 
CALCULATE(
    DISTINCTCOUNT(Fact_Sales[CustomerKey]),
    FILTER(
        VALUES(Fact_Sales[CustomerKey]),
        DATEDIFF(
            CALCULATE(MAX(Fact_Sales[OrderDate])),
            TODAY(),
            DAY
        ) > 90  -- No purchase in last 90 days
    )
)
```

### Churn Rate %
```DAX
Churn Rate % = 
DIVIDE(
    [Churned Customers],
    [Total Customers],
    0
) * 100
```

---

## 9. ADVANCED CALCULATIONS

### Running Total Revenue
```DAX
Running Total Revenue = 
CALCULATE(
    [Total Revenue],
    FILTER(
        ALL(Dim_Date[FullDate]),
        Dim_Date[FullDate] <= MAX(Dim_Date[FullDate])
    )
)
```

### Pareto 80/20 Analysis
```DAX
Top 20% Customers Revenue = 
VAR TotalCustomers = [Total Customers]
VAR Top20PercentCount = TotalCustomers * 0.2
VAR Top20Customers = 
    TOPN(
        Top20PercentCount,
        VALUES(Fact_Sales[CustomerKey]),
        [Customer LTV],
        DESC
    )
RETURN
    CALCULATE(
        [Total Revenue],
        Top20Customers
    )
```

---

## 10. KPI INDICATORS

### Revenue Target Achievement %
```DAX
Revenue Target Achievement = 
VAR MonthlyTarget = 1000000  -- Update with actual target
VAR ActualRevenue = [Total Revenue]
RETURN
    DIVIDE(ActualRevenue, MonthlyTarget, 0) * 100
```

### Traffic Light - Revenue Performance
```DAX
Revenue Performance Indicator = 
VAR Achievement = [Revenue Target Achievement]
RETURN
    SWITCH(
        TRUE(),
        Achievement >= 100, "🟢 Excellent",
        Achievement >= 80, "🟡 On Track",
        Achievement >= 60, "🟠 Needs Attention",
        "🔴 Critical"
    )
```

---

## NOTES FOR POWER BI IMPLEMENTATION:

1. **Import Data Sources:**
   - Import CSV files from `output/data/` folder:
     - rfm_segmentation.csv
     - market_basket_rules.csv
     - cohort_analysis.csv
   - Or connect directly to SQL Server database

2. **Create Relationships:**
   - Link Fact_Sales to Dim_Customer, Dim_Product, Dim_Region, Dim_Date
   - Use CustomerKey, ProductKey, RegionKey, DateKey

3. **Row-Level Security (RLS):**
   ```DAX
   [RegionalManager] = USERNAME()
   ```

4. **Create Hierarchies:**
   - Date: Year > Quarter > Month > Day
   - Geography: Country > State > City
   - Product: Category > SubCategory > Product

5. **Format Measures:**
   - Currency: #,##0.00
   - Percentage: 0.00%
   - Whole Numbers: #,##0

6. **Color Coding for RFM Segments:**
   - Champions: Dark Green
   - Loyal Customers: Light Green
   - At Risk: Orange/Red
   - Lost: Dark Red
