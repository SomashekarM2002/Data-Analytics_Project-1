# Consumer360: Customer Segmentation & CLV Engine

## Project Overview
**Product Brand Name:** Consumer360

**Purpose:** A sophisticated data product to identify "High Value" (Champion) customers for premium engagement and flag "Churn Risk" customers for targeted retention efforts.

**Client:** Major mid-sized e-commerce retailer

## Use Case
The retailer is suffering from generic, ineffective marketing campaigns. This solution provides:
- Instant identification of "High Value" customers
- Detection of "Churn Risk" customers
- Automatic weekly updates from sales transaction data

## Features

### Basic Core Metrics
- Comprehensive tracking of sales trends over time
- Identification of top-selling products by volume and revenue
- Revenue breakdown by geographical region

### Deep (Production) Analytics
1. **RFM Segmentation**: Automated Recency, Frequency, and Monetary scoring (1-5 scale) for every customer
2. **Cohort Analysis**: Advanced visualization of customer retention rates, grouped and tracked based on initial sign-up/first purchase month
3. **Market Basket Analysis**: Association Rule Mining to uncover non-obvious purchase patterns (e.g., "People who bought Bread often bought Butter")

## Implementation Stack
- **SQL**: Initial Data Extraction/Cleansing
- **Python/Pandas**: Core RFM and Market Basket Logic
- **Power BI**: Dynamic Visualization
- **Key Library**: Lifetimes library for predictive Customer Lifetime Value modeling

## Project Timeline

### Week 1: Data Engineering & Schema
- Define and implement Star Schema (Fact Sales, Dim Customer, Dim Product)
- Write optimized, production-ready SQL scripts
- **Critical Review Point**: Ensure all core SQL queries run in under 2 seconds

### Week 2: The Logic Core (Python)
- Develop Python script to pull cleaned data from SQL
- Execute R, F, and M score calculations
- Assign segment labels (Champions, Hibernating, etc.)
- Implement Market Basket logic using mlxtend or custom Pandas
- **Validation Check**: Does the "Champion" segment genuinely represent top-spending customers?

### Week 3: Dashboard Construction
- Import processed, segmented data into Power BI
- Create critical DAX measures
- Build interactive RFM Matrix Visual
- Set up Row-Level Security (RLS) for regional managers
- **UX Review**: Is the dashboard intuitive, clutter-free, and does it answer the client's core use case?

### Week 4: Automation & Handoff
- Schedule end-to-end Python script to run automatically (cron or Windows Task Scheduler)
- Final Presentation Deck with key actionable insights
- **Full Automation Test**: Verify the entire pipeline executes error-free from data pull to dashboard refresh

## RFM Segments
- **Champions**: High recency, frequency, and monetary value
- **Loyal Customers**: Regular purchasers
- **Potential Loyalist**: Promising customers to nurture
- **Recent Users**: New customers to engage
- **Promising**: Good potential for growth
- **Needs Attention**: Declining engagement
- **About To Sleep**: At risk of churning
- **Can't Lose Them**: High-value customers showing churn signals
- **Hibernating**: Inactive but reachable
- **Lost**: Churned customers
- **Price Sensitive**: Respond to discounts

## Directory Structure
```
├── data/                    # Sample and raw data files
├── sql/                     # Week 1: SQL scripts for ETL
├── python/                  # Week 2: Python RFM & Market Basket scripts
├── powerbi/                 # Week 3: Power BI files and DAX measures
├── automation/              # Week 4: Scheduling and automation scripts
├── docs/                    # Documentation and presentation
└── README.md               # This file
```

## Getting Started
1. Review the SQL scripts in the `sql/` folder
2. Run the Python scripts in the `python/` folder after connecting to your database
3. Import the output into Power BI using the templates in `powerbi/`
4. Set up automation using the scripts in `automation/`

## Author
Zaalima Development Pvt. Ltd  
*Confidential Document*
