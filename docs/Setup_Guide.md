# Consumer360: Complete Setup Guide
# Getting Started with Customer Segmentation & CLV Engine
# ================================================================

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Database Setup](#database-setup)
4. [Python Environment Setup](#python-environment-setup)
5. [Running the Pipeline](#running-the-pipeline)
6. [Power BI Setup](#power-bi-setup)
7. [Automation Setup](#automation-setup)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software:
- **SQL Server** (2016 or later) or **SQLite** (for testing)
  - Download: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
- **Python** (3.8 or later)
  - Download: https://www.python.org/downloads/
- **Power BI Desktop** (latest version)
  - Download: https://powerbi.microsoft.com/downloads/
- **Git** (optional, for version control)
  - Download: https://git-scm.com/downloads

### Recommended Skills:
- Basic SQL knowledge
- Understanding of Python basics
- Familiarity with Power BI
- Basic understanding of RFM analysis concepts

---

## Installation Steps

### Step 1: Clone or Download the Project

**Option A: Using Git**
```bash
git clone <repository-url>
cd "Data Analytics Project -1"
```

**Option B: Manual Download**
- Download the project as a ZIP file
- Extract to a folder on your computer

### Step 2: Verify Project Structure

Your folder should look like this:
```
Data Analytics Project -1/
├── README.md
├── sql/
│   ├── 01_create_star_schema.sql
│   ├── 02_sample_data_generation.sql
│   ├── 03_rfm_data_extraction.sql
│   ├── 04_market_basket_extraction.sql
│   └── 05_cohort_analysis_extraction.sql
├── python/
│   ├── config.py
│   ├── db_utils.py
│   ├── rfm_analysis.py
│   ├── market_basket_analysis.py
│   ├── main.py
│   └── requirements.txt
├── powerbi/
│   ├── DAX_Measures.md
│   └── Dashboard_Design_Guide.md
├── automation/
│   ├── scheduler.py
│   ├── setup_windows_task.bat
│   └── setup_cron.sh
└── docs/
    └── Setup_Guide.md (this file)
```

---

## Database Setup

### Option A: SQL Server (Production)

#### 1. Create Database
Open SQL Server Management Studio (SSMS) and run:
```sql
CREATE DATABASE Consumer360;
GO

USE Consumer360;
GO
```

#### 2. Run Schema Creation Scripts
Execute the SQL scripts in order:

1. **Create Star Schema:**
   ```bash
   File -> Open -> sql/01_create_star_schema.sql
   Execute (F5)
   ```

2. **Generate Sample Data:**
   ```bash
   File -> Open -> sql/02_sample_data_generation.sql
   Execute (F5)
   ```
   
   *Note: This generates ~10,000 sample transactions. For production, replace with your actual data import process.*

3. **Verify Installation:**
   ```sql
   -- Check tables
   SELECT * FROM INFORMATION_SCHEMA.TABLES
   WHERE TABLE_TYPE = 'BASE TABLE';
   
   -- Check record counts
   SELECT 
       'Dim_Customer' AS TableName, COUNT(*) AS RecordCount FROM Dim_Customer
   UNION ALL
   SELECT 'Dim_Product', COUNT(*) FROM Dim_Product
   UNION ALL
   SELECT 'Dim_Region', COUNT(*) FROM Dim_Region
   UNION ALL
   SELECT 'Fact_Sales', COUNT(*) FROM Fact_Sales;
   ```

#### 3. Configure Database Connection
Edit `python/config.py`:
```python
DB_CONFIG = {
    'server': 'your_server_name',  # e.g., 'localhost' or 'SERVER\\INSTANCE'
    'database': 'Consumer360',
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': 'yes',  # Windows Authentication
}
```

For SQL Server Authentication:
```python
DB_CONFIG = {
    'server': 'your_server_name',
    'database': 'Consumer360',
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': 'no',
    'username': 'your_username',
    'password': 'your_password',
}
```

### Option B: SQLite (Testing/Development)

For quick testing without SQL Server:

1. Edit `python/config.py`:
   ```python
   USE_SQLITE = True
   SQLITE_DB_PATH = 'data/consumer360.db'
   ```

2. The database will be created automatically when you run the Python scripts.

---

## Python Environment Setup

### 1. Install Python

Download and install Python 3.8+ from https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation!

### 2. Create Virtual Environment (Recommended)

Open Command Prompt or Terminal in the project folder:

**Windows:**
```bash
cd "Data Analytics Project -1"
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd "Data Analytics Project -1"
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

### 3. Install Dependencies

```bash
cd python
pip install -r requirements.txt
```

This will install:
- pandas
- numpy
- pyodbc (SQL Server connection)
- mlxtend (Market Basket Analysis)
- lifetimes (CLV modeling)
- schedule (automation)

### 4. Verify Installation

```bash
python db_utils.py
```

Expected output:
```
Testing database connection...
✓ Connection successful!
```

---

## Running the Pipeline

### Manual Execution

#### Run Complete Pipeline:
```bash
cd python
python main.py
```

This will:
1. Extract data from database
2. Perform RFM analysis
3. Perform Market Basket analysis
4. Generate reports
5. Save CSV files in `output/data/`

#### Run Individual Modules:

**RFM Analysis Only:**
```bash
python rfm_analysis.py
```

**Market Basket Analysis Only:**
```bash
python market_basket_analysis.py
```

### Output Files

After successful execution, you'll find:

```
output/
├── data/
│   ├── rfm_segmentation.csv       # Customer segments
│   ├── rfm_summary.csv             # Segment statistics
│   ├── market_basket_rules.csv     # Association rules
│   └── frequent_itemsets.csv       # Frequent product combinations
├── reports/
│   └── insights_report.txt         # Executive summary
└── consumer360.log                 # Execution log
```

---

## Power BI Setup

### 1. Install Power BI Desktop

Download from: https://powerbi.microsoft.com/downloads/

### 2. Import Data

**Option A: Import CSV Files (Recommended for beginners)**

1. Open Power BI Desktop
2. Click **Get Data** → **Text/CSV**
3. Navigate to `output/data/` and select:
   - `rfm_segmentation.csv`
   - `market_basket_rules.csv`
4. Click **Load**

**Option B: Direct SQL Server Connection (Production)**

1. Click **Get Data** → **SQL Server**
2. Enter:
   - **Server:** your_server_name
   - **Database:** Consumer360
3. Select tables:
   - Fact_Sales
   - Dim_Customer
   - Dim_Product
   - Dim_Region
   - Dim_Date
4. Click **Load**

### 3. Create Relationships

In Power BI, go to **Model View** and verify relationships:

```
Fact_Sales[CustomerKey] → Dim_Customer[CustomerKey]
Fact_Sales[ProductKey] → Dim_Product[ProductKey]
Fact_Sales[RegionKey] → Dim_Region[RegionKey]
Fact_Sales[DateKey] → Dim_Date[DateKey]
```

### 4. Add DAX Measures

Open `powerbi/DAX_Measures.md` and copy the DAX measures into Power BI:

1. In **Data View**, right-click on a table
2. Click **New Measure**
3. Paste the DAX formula
4. Repeat for all measures

### 5. Build Dashboard

Follow the instructions in `powerbi/Dashboard_Design_Guide.md` to create:

- Page 1: Executive Summary
- Page 2: RFM Segmentation Matrix
- Page 3: Product & Market Basket Analysis
- Page 4: Cohort & Retention Analysis

### 6. Publish to Power BI Service (Optional)

1. Click **Publish** in Power BI Desktop
2. Select your workspace
3. Set up scheduled refresh (if using DirectQuery or Import mode)

---

## Automation Setup

### Windows: Task Scheduler

1. Navigate to `automation/` folder
2. Right-click `setup_windows_task.bat`
3. Select **Run as Administrator**
4. Follow the prompts

This creates a scheduled task to run every **Sunday at 6:00 AM**.

**Verify:**
1. Open Task Scheduler (`Win + R`, type `taskschd.msc`)
2. Look for "Consumer360_Weekly_Update"

**Manual Run:**
```bash
schtasks /Run /TN "Consumer360_Weekly_Update"
```

### Linux/Mac: Cron

1. Navigate to `automation/` folder
2. Make the script executable:
   ```bash
   chmod +x setup_cron.sh
   ```
3. Run the setup script:
   ```bash
   ./setup_cron.sh
   ```

**Verify:**
```bash
crontab -l
```

You should see the Consumer360 job listed.

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed

**Error:** `pyodbc.Error: ('IM002', ...)`

**Solution:**
- Install ODBC Driver 17 for SQL Server
- Download: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

**Alternative:** Change driver in `config.py`:
```python
'driver': 'SQL Server'  # Try this if ODBC Driver 17 doesn't work
```

#### 2. Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```bash
pip install -r requirements.txt
```

Make sure you're in the virtual environment (`venv`).

#### 3. SQL Query Timeout

**Error:** Query execution taking too long

**Solution:**
- Add indexes to tables (already included in schema)
- Reduce sample data size
- Optimize queries in `db_utils.py`

#### 4. Market Basket Analysis Returns No Rules

**Error:** `Generated 0 association rules`

**Solution:**
- Lower `min_support` and `min_confidence` in `config.py`:
```python
MARKET_BASKET_CONFIG = {
    'min_support': 0.005,  # Lower from 0.01
    'min_confidence': 0.2,  # Lower from 0.3
    'min_lift': 1.0,  # Lower from 1.2
}
```

#### 5. Power BI: Cannot Load CSV

**Error:** File not found

**Solution:**
- Ensure you've run `python main.py` first
- Check that `output/data/` folder exists and contains CSV files
- Use absolute path in Power BI if needed

#### 6. Scheduled Task Not Running

**Windows:**
- Check Task Scheduler history
- Verify Python path is correct
- Run task manually to test

**Linux/Mac:**
- Check cron logs: `grep CRON /var/log/syslog`
- Verify Python path: `which python3`
- Test cron job manually

---

## Performance Optimization

### For Large Datasets (100K+ transactions):

1. **Optimize SQL Queries:**
   - Use indexed columns for JOINs
   - Add WHERE clauses to filter data
   - Use TOP/LIMIT for testing

2. **Python Performance:**
   - Process data in chunks
   - Use `low_memory=True` in pandas
   - Consider Dask for very large datasets

3. **Power BI:**
   - Use Import mode for < 1GB data
   - Use DirectQuery for real-time data
   - Use Aggregations for large datasets

---

## Next Steps

1. ✅ **Verify Installation:** Run the pipeline manually
2. ✅ **Review Outputs:** Check CSV files and reports
3. ✅ **Build Dashboard:** Create Power BI visualizations
4. ✅ **Set Up Automation:** Schedule weekly updates
5. ✅ **Train Users:** Share dashboard with stakeholders
6. ✅ **Monitor Performance:** Check logs regularly
7. ✅ **Iterate:** Adjust thresholds and segments based on business needs

---

## Support & Resources

### Documentation:
- `README.md` - Project overview
- `powerbi/Dashboard_Design_Guide.md` - Dashboard design
- `powerbi/DAX_Measures.md` - All DAX formulas

### Key Configuration Files:
- `python/config.py` - Database connection, thresholds
- `sql/01_create_star_schema.sql` - Database structure

### Logs:
- `output/consumer360.log` - Application logs
- `output/logs/cron.log` - Scheduled job logs (Linux/Mac)

---

## Frequently Asked Questions

**Q: Can I use my own data instead of sample data?**  
A: Yes! Replace the sample data generation script with your own data import process. Ensure your data matches the schema structure.

**Q: How do I change the RFM scoring thresholds?**  
A: Edit `python/config.py` → `RFM_THRESHOLDS` section.

**Q: Can I change the automation schedule?**  
A: Yes! Edit the schedule in `automation/scheduler.py` or modify the Task Scheduler/cron settings.

**Q: How do I add more customer segments?**  
A: Edit the `assign_segments()` function in `python/rfm_analysis.py`.

**Q: Is this scalable for millions of rows?**  
A: For very large datasets, consider using PySpark or optimizing with database-level aggregations. The current setup works well for up to 1 million transactions.

---

## Credits

**Product:** Consumer360 - Customer Segmentation & CLV Engine  
**Developed by:** Zaalima Development Pvt. Ltd  
**Documentation Version:** 1.0  
**Last Updated:** February 2026

---

**Happy Analyzing! 🚀**
