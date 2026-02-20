# Consumer360: Power BI Dashboard Design Guide
# Week 3: Dashboard Construction
# ================================================================

## Dashboard Structure

The Consumer360 dashboard should consist of **4 main pages**:

### 1. **Executive Summary Dashboard**
### 2. **RFM Customer Segmentation**
### 3. **Product & Market Basket Analysis**
### 4. **Cohort & Retention Analysis**

---

## PAGE 1: Executive Summary Dashboard

### Layout:
```
┌─────────────────────────────────────────────────────────────────┐
│                    CONSUMER360 - EXECUTIVE SUMMARY              │
├──────────────┬──────────────┬──────────────┬──────────────────┤
│ Total Revenue│ Total Orders │ Avg Order Val│  Active Customers│
│   $XXX,XXX   │   XX,XXX     │   $XXX       │     XX,XXX       │
├──────────────┴──────────────┴──────────────┴──────────────────┤
│                                                                 │
│              Revenue Trend (Last 12 Months)                     │
│              [Line Chart with MoM Growth]                       │
│                                                                 │
├─────────────────────────────┬───────────────────────────────────┤
│                             │                                   │
│  Top 5 Products by Revenue  │   Revenue by Region (Map/Chart)  │
│  [Bar Chart]                │   [Filled Map or Bar Chart]      │
│                             │                                   │
├─────────────────────────────┼───────────────────────────────────┤
│                             │                                   │
│  Customer Segment Overview  │   At-Risk Customers Alert        │
│  [Donut Chart]              │   [Card with conditional format] │
│                             │                                   │
└─────────────────────────────┴───────────────────────────────────┘
```

### Key Visuals:
1. **KPI Cards (Top Row):**
   - Total Revenue (with YoY growth %)
   - Total Orders (with MoM change)
   - Average Order Value
   - Active Customers (purchased in last 30 days)

2. **Revenue Trend Line Chart:**
   - X-axis: Month
   - Y-axis: Revenue
   - Add: Goal line, Previous year comparison

3. **Top Products Bar Chart:**
   - Horizontal bar chart
   - Top 5-10 products by revenue
   - Color by category

4. **Regional Performance:**
   - Filled map showing revenue by region
   - Or stacked bar chart if map unavailable

5. **Customer Segments Donut:**
   - Slice by RFM segment
   - Show count or revenue %

6. **At-Risk Alert Card:**
   - Conditional formatting (Red if > threshold)
   - Count of "Can't Lose Them" + "About To Sleep"

### Filters/Slicers:
- Date Range (Calendar selector)
- Region (Dropdown)
- Product Category (Multi-select)

---

## PAGE 2: RFM Customer Segmentation

### Layout:
```
┌─────────────────────────────────────────────────────────────────┐
│             RFM CUSTOMER SEGMENTATION MATRIX                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    RFM Segment Matrix                           │
│                    [Heat Map Visual]                            │
│             Recency (X) vs Frequency & Monetary (Y)             │
│                                                                 │
├─────────────────────────────┬───────────────────────────────────┤
│                             │                                   │
│  Segment Breakdown          │   Champion Customer Details       │
│  [Table with metrics]       │   [Table/Card]                    │
│  - Segment                  │   - Top 10 Champions              │
│  - Customer Count           │   - Revenue contribution          │
│  - Revenue                  │   - Average spend                 │
│  - Avg Order Value          │                                   │
│                             │                                   │
├─────────────────────────────┼───────────────────────────────────┤
│                             │                                   │
│  R, F, M Score Distribution │   Segment Trend Over Time         │
│  [3 Gauge Charts]           │   [Stacked Area Chart]            │
│                             │                                   │
└─────────────────────────────┴───────────────────────────────────┘
```

### Key Visuals:

1. **RFM Matrix Heat Map:**
   - Custom visual showing RFM segments
   - Color-coded by segment value
   - Tooltips showing customer count and revenue

   **Color Scheme:**
   - Champions: #006400 (Dark Green)
   - Loyal Customers: #90EE90 (Light Green)
   - Potential Loyalist: #87CEEB (Sky Blue)
   - At Risk: #FFA500 (Orange)
   - Lost: #8B0000 (Dark Red)

2. **Segment Breakdown Table:**
   - Columns: Segment Name, Customer Count, Revenue, Avg Order Value, %
   - Conditional formatting on key metrics
   - Sparklines for trends

3. **Champion Details:**
   - Top 10 champions by revenue
   - Contact information
   - Last purchase date
   - Action buttons (if applicable)

4. **Score Distribution Gauges:**
   - Average R-Score (1-5)
   - Average F-Score (1-5)
   - Average M-Score (1-5)

5. **Segment Trend:**
   - Stacked area chart
   - X-axis: Month
   - Y-axis: Customer count
   - Layers: Each RFM segment

### Filters/Slicers:
- Segment (Multi-select)
- R/F/M Score range
- Date Range

### Actions:
- Click on segment to drill through to customer list
- Export customer lists for marketing campaigns

---

## PAGE 3: Product & Market Basket Analysis

### Layout:
```
┌─────────────────────────────────────────────────────────────────┐
│           PRODUCT PERFORMANCE & RECOMMENDATIONS                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│              Top Products Performance                           │
│              [Clustered Bar Chart]                              │
│              Revenue vs Profit by Product                       │
│                                                                 │
├─────────────────────────────┬───────────────────────────────────┤
│                             │                                   │
│  Product Categories         │   Market Basket Rules             │
│  [Treemap]                  │   [Table with conditional format] │
│  Size by Revenue            │   IF Buys → THEN Buys             │
│  Color by Profit Margin     │   Confidence, Lift                │
│                             │                                   │
├─────────────────────────────┼───────────────────────────────────┤
│                             │                                   │
│  Cross-Category Bundles     │   Recommendation Engine           │
│  [Network Diagram]          │   [Card/Visual]                   │
│  or [Sankey Diagram]        │   "Customers who bought X         │
│                             │    often bought Y"                │
└─────────────────────────────┴───────────────────────────────────┘
```

### Key Visuals:

1. **Top Products Bar Chart:**
   - Clustered bars: Revenue vs Profit
   - Top 20 products
   - Sort by revenue descending

2. **Product Category Treemap:**
   - Rectangle size = Revenue
   - Color intensity = Profit margin %
   - Click to drill down to subcategory/product

3. **Market Basket Rules Table:**
   - Columns: If Buys, Then Buys, Support %, Confidence %, Lift
   - Conditional formatting:
     - Lift > 2.0: Green
     - Lift 1.5-2.0: Yellow
     - Lift < 1.5: Gray
   - Top 50 rules

4. **Cross-Category Network:**
   - Shows product relationships
   - Nodes: Products
   - Edges: Association strength (lift)
   - Alternative: Sankey diagram from category to category

5. **Recommendation Card:**
   - Smart recommendations based on selection
   - "If customer selects [Product], recommend [Products]"
   - Can be used by sales team

### Filters/Slicers:
- Category
- Subcategory
- Min Lift threshold
- Date Range

---

## PAGE 4: Cohort & Retention Analysis

### Layout:
```
┌─────────────────────────────────────────────────────────────────┐
│              COHORT RETENTION ANALYSIS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│              Cohort Retention Matrix                            │
│              [Heat Map Table]                                   │
│              Rows: Cohort Month | Cols: Months Since Join       │
│                                                                 │
├─────────────────────────────┬───────────────────────────────────┤
│                             │                                   │
│  Retention Curve            │   Churn Analysis                  │
│  [Line Chart]               │   [Funnel Chart]                  │
│  Retention % by Month       │   Active → At Risk → Churned      │
│                             │                                   │
├─────────────────────────────┼───────────────────────────────────┤
│                             │                                   │
│  Customer Lifetime Value    │   Win-Back Campaign Targets       │
│  [Histogram]                │   [Table]                         │
│  Distribution of CLV        │   Recently churned high-value     │
│                             │                                   │
└─────────────────────────────┴───────────────────────────────────┘
```

### Key Visuals:

1. **Cohort Retention Heat Map:**
   - Rows: Sign-up month cohorts
   - Columns: Months 0, 1, 2, 3, 4, 5, 6+
   - Values: % of cohort still active
   - Color scale: Red (low) to Green (high)

2. **Retention Curve:**
   - Line chart
   - X-axis: Months since first purchase
   - Y-axis: Retention %
   - Multiple lines for different cohorts
   - Benchmark line (industry average)

3. **Churn Funnel:**
   - Stages: All Customers → Active → At Risk → Churned
   - Shows conversion/drop-off at each stage

4. **CLV Distribution:**
   - Histogram
   - X-axis: CLV buckets ($0-100, $100-500, etc.)
   - Y-axis: Customer count
   - Helps identify high-value segments

5. **Win-Back Targets:**
   - Table of customers who churned in last 60 days
   - Filter: Previous spend > $1000
   - Columns: Name, Last Purchase, Total Spend, Days Since Purchase

### Filters/Slicers:
- Cohort Month
- Customer Status (Active/Churned)
- CLV Range

---

## Row-Level Security (RLS) Implementation

### Setup:
1. Create role: "Regional Manager"
2. DAX Filter on Dim_Region table:
   ```DAX
   [RegionalManager] = USERNAME()
   ```
3. Assign users to roles in Power BI Service

### Result:
- North Region manager only sees North Region data
- South Region manager only sees South Region data
- Executives see all regions (assign to no role)

---

## Design Best Practices

### Color Palette (Consumer360 Brand):
- Primary: #2C3E50 (Dark Blue-Gray)
- Secondary: #3498DB (Blue)
- Success: #27AE60 (Green)
- Warning: #F39C12 (Orange)
- Danger: #E74C3C (Red)
- Neutral: #95A5A6 (Gray)

### Fonts:
- Headers: Segoe UI Bold, 16-20pt
- Body: Segoe UI Regular, 10-12pt
- Numbers: Segoe UI Semibold, 12-14pt

### Formatting:
- Currency: $#,##0
- Percentages: 0.0%
- Large numbers: #,##0
- Decimals: Only when necessary

### Interactivity:
- Enable cross-filtering between visuals
- Add bookmarks for common views
- Drill-through pages for detailed analysis
- Tooltips with additional context

---

## Data Refresh Schedule

1. **Development/Testing**: Manual refresh
2. **Production**: 
   - Daily refresh at 6:00 AM (after overnight data processing)
   - Or real-time DirectQuery if performance allows

---

## Publishing Checklist

- [ ] Test all visuals with sample data
- [ ] Verify RLS is working correctly
- [ ] Optimize DAX queries for performance
- [ ] Add tooltips and descriptions
- [ ] Create mobile layout version
- [ ] Set up automatic refresh in Power BI Service
- [ ] Share with stakeholders and gather feedback
- [ ] Document any custom visuals used
- [ ] Create user guide/training materials
