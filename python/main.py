"""
Consumer360: Main Orchestration Script
Week 2-4: Complete Pipeline

This script orchestrates the entire Consumer360 pipeline:
1. Data extraction from SQL
2. RFM analysis
3. Market Basket analysis
4. Report generation
"""

import logging
from datetime import datetime
from pathlib import Path
import sys

# Import analysis modules
from rfm_analysis import main as rfm_main
from market_basket_analysis import main as market_basket_main
from config import OUTPUT_DIR, LOG_FILE

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def main():
    """
    Main orchestration function
    """
    start_time = datetime.now()
    
    try:
        print_banner("CONSUMER360: Customer Segmentation & CLV Engine")
        logger.info(f"Pipeline started at: {start_time}")
        
        # Step 1: RFM Analysis
        print_banner("STEP 1: RFM SEGMENTATION ANALYSIS")
        logger.info("Starting RFM analysis...")
        rfm_df, rfm_summary = rfm_main()
        logger.info("✓ RFM analysis completed successfully")
        
        # Step 2: Market Basket Analysis
        print_banner("STEP 2: MARKET BASKET ANALYSIS")
        logger.info("Starting Market Basket analysis...")
        rules, report = market_basket_main()
        logger.info("✓ Market Basket analysis completed successfully")
        
        # Step 3: Generate Combined Report
        print_banner("STEP 3: GENERATING COMBINED INSIGHTS REPORT")
        generate_insights_report(rfm_summary, report)
        
        # Calculate execution time
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Success summary
        print_banner("PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"Start Time:     {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End Time:       {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration:       {duration:.2f} seconds")
        print(f"\nOutput Location: {OUTPUT_DIR.absolute()}")
        print("\nGenerated Files:")
        print(f"  • RFM Segmentation:     output/data/rfm_segmentation.csv")
        print(f"  • RFM Summary:          output/data/rfm_summary.csv")
        print(f"  • Market Basket Rules:  output/data/market_basket_rules.csv")
        print(f"  • Insights Report:      output/reports/insights_report.txt")
        print(f"  • Log File:             output/consumer360.log")
        print("\n" + "="*80)
        
        logger.info(f"Pipeline completed in {duration:.2f} seconds")
        
        return True
    
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        print(f"\n✗ ERROR: Pipeline failed - {e}")
        return False


def generate_insights_report(rfm_summary, market_basket_report):
    """
    Generate a combined insights report
    
    Args:
        rfm_summary (pd.DataFrame): RFM summary statistics
        market_basket_report (pd.DataFrame): Market basket rules
    """
    logger.info("Generating combined insights report...")
    
    report_file = OUTPUT_DIR / 'reports' / 'insights_report.txt'
    
    with open(report_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("CONSUMER360: ACTIONABLE INSIGHTS REPORT\n")
        f.write("Customer Segmentation & CLV Engine\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # RFM Insights
        f.write("1. CUSTOMER SEGMENTATION (RFM Analysis)\n")
        f.write("-"*80 + "\n\n")
        f.write(rfm_summary.to_string())
        f.write("\n\n")
        
        # Key RFM Insights
        f.write("KEY INSIGHTS:\n")
        f.write("-"*80 + "\n")
        
        # Champions
        if 'Champions' in rfm_summary.index:
            champ_pct = rfm_summary.loc['Champions', 'Percentage_of_Customers']
            champ_rev = rfm_summary.loc['Champions', 'Percentage_of_Revenue']
            f.write(f"• Champions represent {champ_pct}% of customers but contribute {champ_rev}% of revenue\n")
        
        # At Risk
        at_risk_segments = ["Can't Lose Them", "About To Sleep", "At Risk"]
        at_risk_count = sum([rfm_summary.loc[seg, 'Customer_Count'] for seg in at_risk_segments if seg in rfm_summary.index])
        if at_risk_count > 0:
            f.write(f"• {at_risk_count} customers are at risk of churning - immediate retention efforts needed\n")
        
        f.write("\n\n")
        
        # Market Basket Insights
        f.write("2. PRODUCT RECOMMENDATIONS (Market Basket Analysis)\n")
        f.write("-"*80 + "\n\n")
        f.write("Top 10 Product Association Rules:\n\n")
        f.write(market_basket_report.head(10).to_string(index=False))
        f.write("\n\n")
        
        # Cross-category opportunities
        cross_cat = market_basket_report[market_basket_report['Cross_Category'] == True]
        if len(cross_cat) > 0:
            f.write("Cross-Category Opportunities:\n\n")
            f.write(cross_cat.head(5).to_string(index=False))
            f.write("\n\n")
        
        # Action Items
        f.write("3. RECOMMENDED ACTIONS\n")
        f.write("-"*80 + "\n")
        f.write("• CHAMPIONS: Reward with exclusive offers, VIP programs, early access to new products\n")
        f.write("• LOYAL CUSTOMERS: Upsell premium products, request referrals and reviews\n")
        f.write("• AT RISK: Send personalized win-back campaigns with special discounts\n")
        f.write("• HIBERNATING: Re-engagement campaigns with strong incentives\n")
        f.write("• RECENT USERS: Onboarding sequences, product recommendations\n")
        f.write("• CROSS-SELL: Implement product recommendations based on association rules\n")
        f.write("\n" + "="*80 + "\n")
    
    logger.info(f"Insights report saved to: {report_file}")
    print(f"\n✓ Insights report generated: {report_file}")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
