# Consumer360: Quick Start Guide
# Get Up and Running in 15 Minutes!
# ================================================================

This guide will help you get Consumer360 running quickly for testing purposes.

---

## Prerequisites

- ✅ Windows 10/11 (for Linux/Mac, see full Setup_Guide.md)
- ✅ Internet connection

---

## Step-by-Step Quick Start

### 1. Download and Install Python (5 minutes)

1. Go to: https://www.python.org/downloads/
2. Click **Download Python 3.12.x** (or latest)
3. Run the installer
4. ⚠️ **IMPORTANT:** Check ✅ "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete

**Verify:**
Open Command Prompt and type:
```bash
python --version
```
You should see something like: `Python 3.12.x`

---

### 2. Install Required Python Libraries (3 minutes)

1. Open Command Prompt
2. Navigate to the project folder:
   ```bash
   cd "C:\Users\Somashekar M\OneDrive\Desktop\Data Analytics Project -1\python"
   ```
3. Install dependencies:
   ```bash
   pip install pandas numpy mlxtend schedule
   ```

---

### 3. Configure for Quick Testing (2 minutes)

1. Open `python/config.py` in Notepad or any text editor
2. Find this line:
   ```python
   USE_SQLITE = False
   ```
3. Change it to:
   ```python
   USE_SQLITE = True
   ```
4. Save and close the file

This will use SQLite (no SQL Server needed) for quick testing!

---

### 4. Generate Sample Data (1 minute)

We'll create sample data directly in Python for quick testing.

Create a file `python/generate_sample_data.py` with this content:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Generate sample customers
num_customers = 500
customers = pd.DataFrame({
    'CustomerID': [f'CUST{i:05d}' for i in range(1, num_customers+1)],
    'CustomerName': [f'Customer {i}' for i in range(1, num_customers+1)],
    'Email': [f'customer{i}@email.com' for i in range(1, num_customers+1)]
})

# Generate sample transactions
num_transactions = 10000
transactions = []

product_names = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
                 'Webcam', 'USB Cable', 'Phone', 'Tablet', 'Charger']

for i in range(num_transactions):
    customer_id = random.choice(customers['CustomerID'].tolist())
    product = random.choice(product_names)
    quantity = random.randint(1, 3)
    unit_price = random.uniform(10, 500)
    order_date = datetime.now() - timedelta(days=random.randint(0, 730))
    
    transactions.append({
        'TransactionID': f'TXN{i:08d}',
        'CustomerID': customer_id,
        'ProductName': product,
        'OrderDate': order_date,
        'Quantity': quantity,
        'UnitPrice': unit_price,
        'TotalAmount': quantity * unit_price,
        'OrderStatus': 'Completed'
    })

transactions_df = pd.DataFrame(transactions)

# Calculate RFM metrics
from datetime import datetime

rfm_data = transactions_df.groupby('CustomerID').agg({
    'OrderDate': lambda x: (datetime.now() - x.max()).days,
    'TransactionID': 'count',
    'TotalAmount': 'sum'
}).reset_index()

rfm_data.columns = ['CustomerID', 'DaysSinceLastPurchase', 'TotalOrders', 'TotalRevenue']

# Merge with customer data
rfm_data = rfm_data.merge(customers, on='CustomerID')

# Save to CSV
rfm_data.to_csv('test_rfm_data.csv', index=False)
transactions_df.to_csv('test_transactions.csv', index=False)

print("✓ Sample data generated successfully!")
print(f"  - {len(customers)} customers")
print(f"  - {len(transactions)} transactions")
print(f"  - Files saved: test_rfm_data.csv, test_transactions.csv")
```

Run it:
```bash
cd python
python generate_sample_data.py
```

---

### 5. Run the Analysis (2 minutes)

⚠️ **Note:** For quick testing without database setup, we'll use a simplified version.

Create `python/quick_test.py`:

```python
import pandas as pd
import numpy as np

print("="*60)
print("Consumer360: Quick RFM Analysis Test")
print("="*60)

# Load sample data
print("\n1. Loading sample data...")
df = pd.read_csv('test_rfm_data.csv')
print(f"   ✓ Loaded {len(df)} customers")

# Calculate RFM scores
print("\n2. Calculating RFM scores...")

# R Score (lower days = higher score)
df['R_Score'] = pd.qcut(df['DaysSinceLastPurchase'], q=5, labels=[5,4,3,2,1], duplicates='drop').astype(int)

# F Score (higher orders = higher score)
df['F_Score'] = pd.qcut(df['TotalOrders'], q=5, labels=[1,2,3,4,5], duplicates='drop').astype(int)

# M Score (higher revenue = higher score)
df['M_Score'] = pd.qcut(df['TotalRevenue'], q=5, labels=[1,2,3,4,5], duplicates='drop').astype(int)

print("   ✓ RFM scores calculated")

# Assign segments
print("\n3. Assigning customer segments...")

def assign_segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif f >= 4 and m >= 4:
        return 'Loyal Customers'
    elif r >= 4:
        return 'Recent Users'
    elif r <= 2 and f >= 4:
        return "Can't Lose Them"
    elif r <= 2:
        return 'At Risk'
    else:
        return 'Other'

df['Segment'] = df.apply(assign_segment, axis=1)
print("   ✓ Segments assigned")

# Display results
print("\n4. RESULTS:")
print("-"*60)
summary = df.groupby('Segment').agg({
    'CustomerID': 'count',
    'TotalRevenue': 'sum'
}).round(2)
summary.columns = ['Customer_Count', 'Total_Revenue']
summary['Revenue_%'] = (summary['Total_Revenue'] / summary['Total_Revenue'].sum() * 100).round(1)
print(summary.to_string())

# Save results
df.to_csv('quick_rfm_results.csv', index=False)
print("\n✓ Results saved to: quick_rfm_results.csv")

print("\n" + "="*60)
print("SUCCESS! Quick test completed.")
print("="*60)
```

Run it:
```bash
python quick_test.py
```

---

### 6. View Results (2 minutes)

Open `quick_rfm_results.csv` in Excel to see your customer segments!

You should see columns:
- CustomerID
- CustomerName
- Email
- DaysSinceLastPurchase
- TotalOrders
- TotalRevenue
- R_Score, F_Score, M_Score
- Segment

---

## What's Next?

This quick test showed you the core RFM analysis in action!

**To run the FULL Consumer360 system:**

1. Follow the complete **Setup_Guide.md** to:
   - Set up SQL Server database
   - Load real transaction data
   - Run Market Basket Analysis
   - Build Power BI dashboards

2. Set up automation for weekly updates

3. Deploy to production

---

## Troubleshooting Quick Start

### Error: "pip is not recognized"

**Solution:**
```bash
python -m pip install pandas numpy mlxtend schedule
```

### Error: "No module named 'pandas'"

**Solution:**
Make sure you ran the pip install command in Step 2.

### Error: "File not found"

**Solution:**
Make sure you're in the correct directory:
```bash
cd "C:\Users\Somashekar M\OneDrive\Desktop\Data Analytics Project -1\python"
```

---

## Quick Commands Reference

```bash
# Install dependencies
pip install pandas numpy mlxtend schedule

# Run quick test
python quick_test.py

# Run full pipeline (after setup)
python main.py

# Run RFM analysis only
python rfm_analysis.py

# Run Market Basket analysis only
python market_basket_analysis.py
```

---

**You're all set! Happy analyzing! 🚀**

For full implementation, see: `docs/Setup_Guide.md`
