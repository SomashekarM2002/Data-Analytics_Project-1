"""
Consumer360: Database Configuration
Week 2: Python Logic Core
"""

import os
from pathlib import Path

# Database Connection Settings
# Update these with your actual database credentials
DB_CONFIG = {
    'server': 'localhost',  # or your SQL Server instance
    'database': 'Consumer360',
    'driver': 'ODBC Driver 17 for SQL Server',  # or 'SQL Server'
    'trusted_connection': 'yes',  # Set to 'no' if using SQL authentication
    
    # If using SQL authentication, uncomment and fill these:
    # 'username': 'your_username',
    # 'password': 'your_password',
}

# Alternative: SQLite for local testing
USE_SQLITE = False  # Set to True to use SQLite instead of SQL Server
SQLITE_DB_PATH = 'data/consumer360.db'

# RFM Scoring Thresholds (can be tuned based on business requirements)
RFM_THRESHOLDS = {
    'recency_days': [30, 90, 180, 365],  # Days for R-score 5, 4, 3, 2, 1
    'frequency_orders': [10, 7, 4, 2, 1],  # Orders for F-score 5, 4, 3, 2, 1
    'monetary_revenue': [5000, 2000, 500, 100, 0],  # Revenue for M-score 5, 4, 3, 2, 1
}

# Market Basket Analysis Settings
MARKET_BASKET_CONFIG = {
    'min_support': 0.01,  # Minimum support (1% of transactions)
    'min_confidence': 0.3,  # Minimum confidence (30%)
    'min_lift': 1.2,  # Minimum lift (20% increase over random)
    'max_length': 3,  # Maximum items in a rule
}

# Output Directories
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)

REPORTS_DIR = OUTPUT_DIR / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)

DATA_DIR = OUTPUT_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# File Paths
RFM_OUTPUT_FILE = DATA_DIR / 'rfm_segmentation.csv'
MARKET_BASKET_OUTPUT_FILE = DATA_DIR / 'market_basket_rules.csv'
COHORT_OUTPUT_FILE = DATA_DIR / 'cohort_analysis.csv'

# Logging Configuration
LOG_FILE = OUTPUT_DIR / 'consumer360.log'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
