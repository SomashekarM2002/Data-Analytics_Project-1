"""
Consumer360: Market Basket Analysis
Week 2: Python Logic Core

This script performs Market Basket Analysis using the Apriori algorithm
to discover association rules (e.g., "People who bought Bread often bought Butter")
"""

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import logging
from config import MARKET_BASKET_CONFIG, MARKET_BASKET_OUTPUT_FILE
from db_utils import get_market_basket_data

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def prepare_transactions(df):
    """
    Convert transaction data into format suitable for market basket analysis
    
    Args:
        df (pd.DataFrame): Transaction-product data
    
    Returns:
        pd.DataFrame: One-hot encoded transaction matrix
        list: List of transactions (for reference)
    """
    logger.info("Preparing transactions for market basket analysis...")
    
    # Group products by transaction
    transactions = df.groupby('TransactionID')['ProductName'].apply(list).values.tolist()
    
    logger.info(f"Total transactions: {len(transactions)}")
    logger.info(f"Sample transaction: {transactions[0][:5]}")
    
    # One-hot encode transactions
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    logger.info(f"Encoded matrix shape: {df_encoded.shape}")
    logger.info(f"Unique products: {len(te.columns_)}")
    
    return df_encoded, transactions


def find_frequent_itemsets(df_encoded, min_support):
    """
    Find frequent itemsets using Apriori algorithm
    
    Args:
        df_encoded (pd.DataFrame): One-hot encoded transaction matrix
        min_support (float): Minimum support threshold
    
    Returns:
        pd.DataFrame: Frequent itemsets
    """
    logger.info(f"Finding frequent itemsets (min_support={min_support})...")
    
    frequent_itemsets = apriori(
        df_encoded,
        min_support=min_support,
        use_colnames=True,
        low_memory=True
    )
    
    logger.info(f"Found {len(frequent_itemsets)} frequent itemsets")
    
    # Add itemset length
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    
    return frequent_itemsets


def generate_association_rules(frequent_itemsets, min_confidence, min_lift):
    """
    Generate association rules from frequent itemsets
    
    Args:
        frequent_itemsets (pd.DataFrame): Frequent itemsets
        min_confidence (float): Minimum confidence threshold
        min_lift (float): Minimum lift threshold
    
    Returns:
        pd.DataFrame: Association rules
    """
    logger.info(f"Generating association rules (min_confidence={min_confidence}, min_lift={min_lift})...")
    
    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )
    
    # Filter by lift
    rules = rules[rules['lift'] >= min_lift]
    
    logger.info(f"Generated {len(rules)} association rules")
    
    # Convert frozensets to strings for readability
    rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    
    # Sort by lift descending
    rules = rules.sort_values('lift', ascending=False)
    
    return rules


def analyze_rules_by_category(df_transactions, rules):
    """
    Analyze association rules by product category
    
    Args:
        df_transactions (pd.DataFrame): Original transaction data
        rules (pd.DataFrame): Association rules
    
    Returns:
        pd.DataFrame: Category-level insights
    """
    logger.info("Analyzing rules by product category...")
    
    # Get product-category mapping
    product_category = df_transactions[['ProductName', 'Category']].drop_duplicates()
    product_category_dict = dict(zip(product_category['ProductName'], product_category['Category']))
    
    # Add categories to rules
    def get_categories(itemset):
        categories = set()
        for item in itemset:
            if item in product_category_dict:
                categories.add(product_category_dict[item])
        return ', '.join(sorted(categories))
    
    rules['antecedent_categories'] = rules['antecedents'].apply(get_categories)
    rules['consequent_categories'] = rules['consequents'].apply(get_categories)
    
    # Flag cross-category rules (more interesting!)
    rules['is_cross_category'] = rules['antecedent_categories'] != rules['consequent_categories']
    
    return rules


def generate_market_basket_report(rules):
    """
    Generate summary report of market basket analysis
    
    Args:
        rules (pd.DataFrame): Association rules
    
    Returns:
        pd.DataFrame: Top rules summary
    """
    logger.info("Generating market basket report...")
    
    # Select key columns for report
    report = rules[[
        'antecedents_str',
        'consequents_str',
        'support',
        'confidence',
        'lift',
        'antecedent_categories',
        'consequent_categories',
        'is_cross_category'
    ]].copy()
    
    # Round numeric columns
    report['support'] = (report['support'] * 100).round(2)
    report['confidence'] = (report['confidence'] * 100).round(2)
    report['lift'] = report['lift'].round(2)
    
    # Rename columns for clarity
    report.columns = [
        'If_Customer_Buys',
        'Then_Also_Buys',
        'Support_%',
        'Confidence_%',
        'Lift',
        'Antecedent_Category',
        'Consequent_Category',
        'Cross_Category'
    ]
    
    return report


def main():
    """
    Main execution function for Market Basket Analysis
    """
    try:
        logger.info("="*60)
        logger.info("Starting Market Basket Analysis")
        logger.info("="*60)
        
        # 1. Extract data from database
        logger.info("Step 1: Extracting transaction data from database...")
        df_transactions = get_market_basket_data()
        logger.info(f"Loaded {df_transactions['TransactionID'].nunique()} transactions")
        
        # 2. Prepare transactions
        logger.info("Step 2: Preparing transaction matrix...")
        df_encoded, transactions = prepare_transactions(df_transactions)
        
        # 3. Find frequent itemsets
        logger.info("Step 3: Finding frequent itemsets...")
        frequent_itemsets = find_frequent_itemsets(
            df_encoded,
            MARKET_BASKET_CONFIG['min_support']
        )
        
        # 4. Generate association rules
        logger.info("Step 4: Generating association rules...")
        rules = generate_association_rules(
            frequent_itemsets,
            MARKET_BASKET_CONFIG['min_confidence'],
            MARKET_BASKET_CONFIG['min_lift']
        )
        
        # 5. Analyze by category
        logger.info("Step 5: Analyzing rules by category...")
        rules = analyze_rules_by_category(df_transactions, rules)
        
        # 6. Generate report
        logger.info("Step 6: Generating summary report...")
        report = generate_market_basket_report(rules)
        
        # 7. Save results
        logger.info("Step 7: Saving results...")
        report.to_csv(MARKET_BASKET_OUTPUT_FILE, index=False)
        logger.info(f"Market basket rules saved to: {MARKET_BASKET_OUTPUT_FILE}")
        
        # Save frequent itemsets
        itemsets_file = MARKET_BASKET_OUTPUT_FILE.parent / 'frequent_itemsets.csv'
        frequent_itemsets.to_csv(itemsets_file, index=False)
        logger.info(f"Frequent itemsets saved to: {itemsets_file}")
        
        # 8. Display top results
        print("\n" + "="*120)
        print("TOP 20 ASSOCIATION RULES (Ordered by Lift)")
        print("="*120)
        print(report.head(20).to_string(index=False))
        print("\n" + "="*120)
        
        # Display cross-category rules
        cross_category = report[report['Cross_Category'] == True].head(10)
        if len(cross_category) > 0:
            print("\nTOP 10 CROSS-CATEGORY RECOMMENDATIONS")
            print("="*120)
            print(cross_category.to_string(index=False))
            print("\n" + "="*120)
        
        # Statistics
        print(f"\nSTATISTICS:")
        print(f"✓ Total association rules found: {len(rules)}")
        print(f"✓ Cross-category rules: {rules['is_cross_category'].sum()}")
        print(f"✓ Average lift: {rules['lift'].mean():.2f}")
        print(f"✓ Max lift: {rules['lift'].max():.2f}")
        
        logger.info("="*60)
        logger.info("Market Basket Analysis Completed Successfully!")
        logger.info("="*60)
        
        return rules, report
    
    except Exception as e:
        logger.error(f"Error in market basket analysis: {e}")
        raise


if __name__ == "__main__":
    rules, report = main()
