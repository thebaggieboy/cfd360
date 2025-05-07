#!/bin/bash
# /path/to/your/project/run_investment_updater.sh

# Set environment variables
export DJANGO_SETTINGS_MODULE="cfd360.settings"
export PYTHONPATH="/path/to/your/project"

# Activate virtual environment (if using one)
source /path/to/venv/bin/activate

# Navigate to project directory
cd /path/to/your/project

# Run the command with logging
python manage.py update_investments >> /var/log/investment_updater.log 2>&1