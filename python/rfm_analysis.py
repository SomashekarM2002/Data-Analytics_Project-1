"""
Consumer360: RFM Segmentation Analysis
Week 2: Python Logic Core

This script performs RFM (Recency, Frequency, Monetary) analysis to segment customers
into actionable groups like Champions, Loyal Customers, At Risk, etc.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
from config import RFM_THRESHOLDS, RFM_OUTPUT_FILE
from db_utils import get_rfm_data

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def calculate_rfm_scores(df):
    """
    Calculate R, F, M scores (1-5 scale) for each customer
    
    Args:
        df (pd.DataFrame): Customer data with Recency, Frequency, Monetary values
    
    Returns:
        pd.DataFrame: Data with R, F, M scores added
    """
    logger.info("Calculating RFM scores...")
    
    # Recency Score (lower days = higher score)
    # Score 5: Most recent, Score 1: Least recent
    df['R_Score'] = pd.cut(
        df['DaysSinceLastPurchase'],
        bins=[-1] + RFM_THRESHOLDS['recency_days'] + [float('inf')],
        labels=[5, 4, 3, 2, 1]
    ).astype(int)
    
    # Frequency Score (higher orders = higher score)
    # Using quantiles for more balanced distribution
    df['F_Score'] = pd.qcut(
        df['TotalOrders'],
        q=5,
        labels=[1, 2, 3, 4, 5],
        duplicates='drop'
    ).astype(int)
    
    # Monetary Score (higher revenue = higher score)
    # Using quantiles for more balanced distribution
    df['M_Score'] = pd.qcut(
        df['TotalRevenue'],
        q=5,
        labels=[1, 2, 3, 4, 5],
        duplicates='drop'
    ).astype(int)
    
    # Combined RFM Score
    df['RFM_Score'] = df['R_Score'].astype(str) + df['F_Score'].astype(str) + df['M_Score'].astype(str)
    
    # Overall RFM Value (simple average)
    df['RFM_Value'] = (df['R_Score'] + df['F_Score'] + df['M_Score']) / 3
    
    logger.info("RFM scores calculated successfully")
    return df


def assign_segments(df):
    """
    Assign customer segments based on RFM scores
    
    Args:
        df (pd.DataFrame): Data with RFM scores
    
    Returns:
        pd.DataFrame: Data with segments assigned
    """
    logger.info("Assigning customer segments...")
    
    def segment_customer(row):
        """Determine segment based on R, F, M scores"""
        r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
        
        # Champions: High R, F, M
        if r >= 4 and f >= 4 and m >= 4:
            return 'Champions'
        
        # Loyal Customers: High F and M, moderate R
        elif f >= 4 and m >= 4:
            return 'Loyal Customers'
        
        # Potential Loyalist: Recent customers with good frequency
        elif r >= 4 and f >= 3:
            return 'Potential Loyalist'
        
        # Recent Users: Very recent, low frequency
        elif r >= 4 and f <= 2:
            return 'Recent Users'
        
        # Promising: Recent with moderate spending
        elif r >= 3 and m >= 3:
            return 'Promising'
        
        # Needs Attention: Above average recency, frequency, and monetary
        elif r >= 3 and f >= 2 and m >= 2:
            return 'Needs Attention'
        
        # About To Sleep: Below average recency and frequency
        elif r <= 2 and f >= 2:
            return 'About To Sleep'
        
        # At Risk (Can't Lose Them): High spenders who haven't purchased recently
        elif r <= 2 and f >= 4 and m >= 4:
            return "Can't Lose Them"
        
        # Hibernating: Low recency, frequency, monetary
        elif r <= 2 and f <= 2 and m >= 2:
            return 'Hibernating'
        
        # Price Sensitive: Low monetary value regardless of recency
        elif m <= 2:
            return 'Price Sensitive'
        
        # Lost: Very low scores across the board
        elif r == 1 and f <= 2:
            return 'Lost'
        
        else:
            return 'Other'
    
    df['Segment'] = df.apply(segment_customer, axis=1)
    
    logger.info("Customer segments assigned successfully")
    return df


def generate_rfm_report(df):
    """
    Generate summary report of RFM analysis
    
    Args:
        df (pd.DataFrame): RFM segmented data
    
    Returns:
        pd.DataFrame: Summary statistics by segment
    """
    logger.info("Generating RFM summary report...")
    
    summary = df.groupby('Segment').agg({
        'CustomerKey': 'count',
        'TotalRevenue': ['sum', 'mean'],
        'TotalOrders': 'mean',
        'DaysSinceLastPurchase': 'mean',
        'AvgOrderValue': 'mean',
        'R_Score': 'mean',
        'F_Score': 'mean',
        'M_Score': 'mean'
    }).round(2)
    
    summary.columns = [
        'Customer_Count',
        'Total_Revenue',
        'Avg_Revenue_Per_Customer',
        'Avg_Orders',
        'Avg_Days_Since_Purchase',
        'Avg_Order_Value',
        'Avg_R_Score',
        'Avg_F_Score',
        'Avg_M_Score'
    ]
    
    # Calculate percentage of total customers
    summary['Percentage_of_Customers'] = (summary['Customer_Count'] / summary['Customer_Count'].sum() * 100).round(2)
    
    # Calculate percentage of total revenue
    summary['Percentage_of_Revenue'] = (summary['Total_Revenue'] / summary['Total_Revenue'].sum() * 100).round(2)
    
    # Sort by total revenue descending
    summary = summary.sort_values('Total_Revenue', ascending=False)
    
    logger.info("RFM summary report generated successfully")
    return summary


def main():
    """
    Main execution function for RFM analysis
    """
    try:
        logger.info("="*60)
        logger.info("Starting RFM Segmentation Analysis")
        logger.info("="*60)
        
        # 1. Extract data from database
        logger.info("Step 1: Extracting customer data from database...")
        df = get_rfm_data()
        logger.info(f"Loaded {len(df)} customers")
        
        # 2. Calculate RFM scores
        logger.info("Step 2: Calculating RFM scores...")
        df = calculate_rfm_scores(df)
        
        # 3. Assign segments
        logger.info("Step 3: Assigning customer segments...")
        df = assign_segments(df)
        
        # 4. Generate summary report
        logger.info("Step 4: Generating summary report...")
        summary = generate_rfm_report(df)
        
        # 5. Save results
        logger.info("Step 5: Saving results...")
        df.to_csv(RFM_OUTPUT_FILE, index=False)
        logger.info(f"RFM segmentation saved to: {RFM_OUTPUT_FILE}")
        
        summary_file = RFM_OUTPUT_FILE.parent / 'rfm_summary.csv'
        summary.to_csv(summary_file)
        logger.info(f"RFM summary saved to: {summary_file}")
        
        # 6. Display results
        print("\n" + "="*80)
        print("RFM SEGMENTATION SUMMARY")
        print("="*80)
        print(summary.to_string())
        print("\n" + "="*80)
        
        # Validation Check
        champions = df[df['Segment'] == 'Champions']
        print(f"\nVALIDATION CHECK:")
        print(f"✓ Champions segment has {len(champions)} customers")
        print(f"✓ Champions contribute ${champions['TotalRevenue'].sum():,.2f} in revenue")
        print(f"✓ Champions average order value: ${champions['AvgOrderValue'].mean():,.2f}")
        
        logger.info("="*60)
        logger.info("RFM Analysis Completed Successfully!")
        logger.info("="*60)
        
        return df, summary
    
    except Exception as e:
        logger.error(f"Error in RFM analysis: {e}")
        raise


if __name__ == "__main__":
    df, summary = main()
