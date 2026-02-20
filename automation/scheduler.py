"""
Consumer360: Automated Pipeline Scheduler
Week 4: Automation & Handoff

This script runs the entire Consumer360 pipeline automatically on a schedule.
For Windows: Use Windows Task Scheduler
For Linux/Mac: Use cron
"""

import schedule
import time
import logging
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path to import main module
sys.path.append(str(Path(__file__).parent.parent / 'python'))

from main import main as run_pipeline
from config import LOG_FILE

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


def scheduled_job():
    """
    Run the Consumer360 pipeline as a scheduled job
    """
    logger.info("="*80)
    logger.info(f"SCHEDULED PIPELINE STARTED: {datetime.now()}")
    logger.info("="*80)
    
    try:
        success = run_pipeline()
        
        if success:
            logger.info("✓ Scheduled pipeline completed successfully")
        else:
            logger.error("✗ Scheduled pipeline failed")
    
    except Exception as e:
        logger.error(f"✗ Scheduled pipeline error: {e}", exc_info=True)


def run_scheduler_continuous():
    """
    Run scheduler continuously (for testing or server deployment)
    """
    # Schedule the job to run every Sunday at 6:00 AM
    schedule.every().sunday.at("06:00").do(scheduled_job)
    
    # Alternative schedules (uncomment as needed):
    # schedule.every().day.at("06:00").do(scheduled_job)  # Daily at 6 AM
    # schedule.every().monday.at("06:00").do(scheduled_job)  # Every Monday at 6 AM
    # schedule.every(7).days.at("06:00").do(scheduled_job)  # Every 7 days at 6 AM
    
    logger.info("Scheduler started. Waiting for scheduled time...")
    logger.info("Next run scheduled for: Sunday at 06:00 AM")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def run_once_now():
    """
    Run the pipeline immediately (for manual/test execution)
    """
    logger.info("Running pipeline immediately (manual execution)...")
    scheduled_job()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Consumer360 Pipeline Scheduler')
    parser.add_argument(
        '--mode',
        choices=['continuous', 'once'],
        default='once',
        help='Run mode: continuous (scheduled) or once (immediate)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'continuous':
        print("Starting scheduler in continuous mode...")
        print("Press Ctrl+C to stop")
        try:
            run_scheduler_continuous()
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
    else:
        run_once_now()
