#!/bin/bash
# ================================================================
# Consumer360: Cron Setup Script (Linux/Mac)
# Week 4: Automation & Handoff
# ================================================================
# This script sets up a cron job to run the Consumer360 pipeline
# automatically every Sunday at 6:00 AM
# ================================================================

echo "Setting up Consumer360 Automated Cron Job..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCHEDULER_SCRIPT="$SCRIPT_DIR/scheduler.py"
PYTHON_CMD=$(which python3 || which python)

# Check if Python is available
if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: Python not found. Please install Python first."
    exit 1
fi

echo "Script Directory: $SCRIPT_DIR"
echo "Scheduler Script: $SCHEDULER_SCRIPT"
echo "Python Command: $PYTHON_CMD"
echo ""

# Create log directory
mkdir -p "$SCRIPT_DIR/../output/logs"

# Cron job command
CRON_CMD="0 6 * * 0 cd $SCRIPT_DIR/.. && $PYTHON_CMD $SCHEDULER_SCRIPT --mode once >> $SCRIPT_DIR/../output/logs/cron.log 2>&1"

# Check if cron job already exists
crontab -l 2>/dev/null | grep -q "Consumer360"
if [ $? -eq 0 ]; then
    echo "Existing Consumer360 cron job found. Removing..."
    crontab -l 2>/dev/null | grep -v "Consumer360" | crontab -
fi

# Add new cron job
echo "Adding cron job..."
(crontab -l 2>/dev/null; echo "# Consumer360: Weekly Pipeline Update"; echo "$CRON_CMD") | crontab -

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "SUCCESS! Cron job created successfully."
    echo "========================================"
    echo ""
    echo "Schedule: Every Sunday at 6:00 AM"
    echo "Log file: $SCRIPT_DIR/../output/logs/cron.log"
    echo ""
    echo "To view current cron jobs:"
    echo "  crontab -l"
    echo ""
    echo "To edit cron jobs:"
    echo "  crontab -e"
    echo ""
    echo "To remove this cron job:"
    echo "  crontab -l | grep -v 'Consumer360' | crontab -"
    echo ""
    echo "To run the pipeline manually:"
    echo "  $PYTHON_CMD $SCHEDULER_SCRIPT --mode once"
    echo ""
else
    echo ""
    echo "ERROR: Failed to create cron job."
    echo ""
    exit 1
fi
