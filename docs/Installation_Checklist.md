# Consumer360: Installation Checklist

Use this checklist to track your installation progress.

## Pre-Installation
- [ ] Windows 10/11 or Linux/Mac OS available
- [ ] Administrator access to install software
- [ ] At least 5GB free disk space
- [ ] Internet connection available

## Software Installation
- [ ] Python 3.8+ installed
- [ ] Python added to PATH
- [ ] SQL Server installed (or planning to use SQLite)
- [ ] Power BI Desktop installed
- [ ] Text editor installed (VS Code, Notepad++, etc.)

## Database Setup
- [ ] Database created (Consumer360)
- [ ] Star schema tables created (Dim_*, Fact_Sales)
- [ ] Sample data generated (or real data imported)
- [ ] All SQL queries execute successfully
- [ ] Data extraction queries tested

## Python Environment
- [ ] Virtual environment created
- [ ] Dependencies installed (pandas, numpy, etc.)
- [ ] Database connection configured in config.py
- [ ] Connection test successful (python db_utils.py)
- [ ] RFM thresholds reviewed and adjusted if needed

## Analysis Execution
- [ ] RFM analysis runs successfully
- [ ] Market Basket analysis runs successfully
- [ ] Output CSV files generated
- [ ] Insights report generated
- [ ] No errors in console output

## Power BI Setup
- [ ] Data imported into Power BI
- [ ] Table relationships created
- [ ] DAX measures added
- [ ] Dashboard pages created
- [ ] Visualizations formatted
- [ ] Filters/slicers configured
- [ ] Row-Level Security configured (if needed)

## Automation
- [ ] Scheduler script configured
- [ ] Windows Task Scheduler task created (or cron job)
- [ ] Scheduled task tested manually
- [ ] Logs verified
- [ ] Email notifications configured (optional)

## Testing & Validation
- [ ] Run complete pipeline end-to-end
- [ ] Verify all output files
- [ ] Check Power BI dashboard updates
- [ ] Test RLS (if configured)
- [ ] Performance test (queries under 2 seconds)
- [ ] Test automation schedule

## Documentation & Training
- [ ] README.md reviewed
- [ ] Setup guide available
- [ ] DAX measures documented
- [ ] User training scheduled/completed
- [ ] Support contact information shared

## Production Deployment
- [ ] Backup all configuration files
- [ ] Production database connected
- [ ] Real data loaded and tested
- [ ] Scheduled tasks running
- [ ] Monitoring set up
- [ ] Stakeholders notified

## Post-Deployment
- [ ] First automated run successful
- [ ] Dashboard shared with users
- [ ] Feedback collected
- [ ] Performance monitoring active
- [ ] Maintenance plan established

---

## Notes:

**Installation Date:** _______________  
**Installed By:** _______________  
**Production Go-Live Date:** _______________

**Issues Encountered:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Resolution:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

**Status:** 
- [ ] Installation Complete
- [ ] Testing Phase
- [ ] Production Ready
- [ ] Deployed to Production
