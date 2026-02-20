"""
Consumer360: Database Connection Utilities
Week 2: Python Logic Core
"""

import pyodbc
import pandas as pd
import sqlite3
from config import DB_CONFIG, USE_SQLITE, SQLITE_DB_PATH
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_sql_server_connection():
    """
    Create connection to SQL Server database
    
    Returns:
        pyodbc.Connection: Database connection object
    """
    try:
        if DB_CONFIG.get('trusted_connection') == 'yes':
            conn_str = (
                f"DRIVER={{{DB_CONFIG['driver']}}};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{{DB_CONFIG['driver']}}};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"UID={DB_CONFIG['username']};"
                f"PWD={DB_CONFIG['password']};"
            )
        
        conn = pyodbc.connect(conn_str)
        logger.info("Successfully connected to SQL Server")
        return conn
    
    except Exception as e:
        logger.error(f"Error connecting to SQL Server: {e}")
        raise


def get_sqlite_connection():
    """
    Create connection to SQLite database
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        logger.info(f"Successfully connected to SQLite database: {SQLITE_DB_PATH}")
        return conn
    
    except Exception as e:
        logger.error(f"Error connecting to SQLite: {e}")
        raise


def get_connection():
    """
    Get database connection based on configuration
    
    Returns:
        Connection object (pyodbc or sqlite3)
    """
    if USE_SQLITE:
        return get_sqlite_connection()
    else:
        return get_sql_server_connection()


def execute_query(query, params=None):
    """
    Execute a SQL query and return results as a pandas DataFrame
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters for parameterized queries
    
    Returns:
        pd.DataFrame: Query results
    """
    try:
        conn = get_connection()
        
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        logger.info(f"Query executed successfully. Returned {len(df)} rows.")
        return df
    
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise


def execute_sql_file(file_path):
    """
    Execute SQL commands from a file
    
    Args:
        file_path (str): Path to SQL file
    
    Returns:
        bool: True if successful
    """
    try:
        with open(file_path, 'r') as file:
            sql_script = file.read()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Split script by GO statements (SQL Server)
        commands = sql_script.split('GO')
        
        for command in commands:
            command = command.strip()
            if command:
                cursor.execute(command)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"Successfully executed SQL file: {file_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error executing SQL file {file_path}: {e}")
        raise


def get_rfm_data():
    """
    Extract RFM data from database
    
    Returns:
        pd.DataFrame: Customer RFM metrics
    """
    query = """
    WITH CustomerMetrics AS (
        SELECT 
            c.CustomerKey,
            c.CustomerID,
            c.CustomerName,
            c.Email,
            c.SignUpDate,
            c.FirstPurchaseDate,
            DATEDIFF(DAY, MAX(s.OrderDate), GETDATE()) AS DaysSinceLastPurchase,
            COUNT(DISTINCT CASE WHEN s.OrderStatus = 'Completed' THEN s.TransactionID END) AS TotalOrders,
            SUM(CASE WHEN s.OrderStatus = 'Completed' THEN s.TotalAmount ELSE 0 END) AS TotalRevenue,
            AVG(CASE WHEN s.OrderStatus = 'Completed' THEN s.TotalAmount END) AS AvgOrderValue,
            MIN(s.OrderDate) AS FirstOrderDate,
            MAX(s.OrderDate) AS LastOrderDate
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
        DaysSinceLastPurchase,
        TotalOrders,
        CAST(TotalRevenue AS DECIMAL(12,2)) AS TotalRevenue,
        CAST(AvgOrderValue AS DECIMAL(10,2)) AS AvgOrderValue,
        FirstOrderDate,
        LastOrderDate
    FROM CustomerMetrics
    WHERE TotalOrders > 0
    ORDER BY TotalRevenue DESC
    """
    
    return execute_query(query)


def get_market_basket_data():
    """
    Extract transaction data for market basket analysis
    
    Returns:
        pd.DataFrame: Transaction-product pairs
    """
    query = """
    SELECT 
        s.TransactionID,
        p.ProductName,
        p.Category,
        p.SubCategory
    FROM Fact_Sales s
    INNER JOIN Dim_Product p ON s.ProductKey = p.ProductKey
    WHERE s.OrderStatus = 'Completed'
    ORDER BY s.TransactionID
    """
    
    return execute_query(query)


if __name__ == "__main__":
    # Test database connection
    print("Testing database connection...")
    try:
        conn = get_connection()
        print("✓ Connection successful!")
        conn.close()
    except Exception as e:
        print(f"✗ Connection failed: {e}")
