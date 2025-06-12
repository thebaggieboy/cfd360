# management/commands/update_investments.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import InvestmentPlan
from decimal import Decimal, getcontext
import logging
from datetime import timedelta

# Configure decimal precision
getcontext().prec = 8

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update investment values with detailed verbose output'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update regardless of last update time',
        )
        parser.add_argument(
            '--simulate',
            action='store_true',
            help='Run in simulation mode (no database changes)',
        )

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        self.verbose = verbosity > 1
        self.simulate = options['simulate']
        
        self.log("=== INVESTMENT UPDATE PROCESS STARTED ===", level=1)
        self.log(f"Current time: {timezone.now()}", level=2)
        self.log(f"Options: {options}", level=2)
        
        try:
            self.process_investments(options)
        except Exception as e:
            self.error(f"Fatal error: {str(e)}")
            logger.exception("Command failed")
            raise

        self.log("=== PROCESS COMPLETED ===", level=1)

    def process_investments(self, options):
        """Main processing method"""
        investments = InvestmentPlan.objects.filter(status="Pending")
        count = investments.count()
        
        self.log(f"\nFound {count} active investments", level=1)
        
        if count == 0:
            self.log("No active investments found. Nothing to do.", level=1)
            return
            
        updated_count = 0
        
        for investment in investments:
            try:
                self.log(f"\nProcessing investment ID: {investment.id}", level=1)
                self.log(f"Plan: {investment.investment_plan}", level=2)
                
                if self.process_single_investment(investment, options):
                    updated_count += 1
                    
            except Exception as e:
                self.error(f"Failed to process investment {investment.id}: {str(e)}")
                logger.error(f"Error processing investment {investment.id}", exc_info=True)
                continue
                
        self.log(f"\nSummary: Updated {updated_count}/{count} investments", level=1)

    def process_single_investment(self, investment, options):
        """Process an individual investment"""
        # Initial debug info
        self.log_debug_info(investment)
        
        # Check if update is needed
        if not self.should_update(investment, options):
            return False
            
        # Get rates and calculate values
        rates = self.get_plan_rates(investment.investment_plan)
        calculations = self.calculate_values(investment, rates)
        
        # Update the investment
        if not self.simulate:
            self.apply_updates(investment, calculations)
            
        self.log_update_summary(investment, calculations)
        return True

    def log_debug_info(self, investment):
        """Log initial investment state"""
        self.log("\nCurrent investment state:", level=2)
        self.log(f"Amount: {investment.amount}", level=2)
        self.log(f"Current value: {investment.current_value}", level=2)
        self.log(f"Investment date: {investment.investment_date}", level=2)
        self.log(f"Last daily update: {investment.daily_roi_date}", level=2)
        self.log(f"Status: {investment.status}", level=2)

    def should_update(self, investment, options):
        """Determine if investment needs updating"""
        now = timezone.now()
        last_update = investment.daily_roi_date or investment.investment_date
        time_diff = now - last_update
        
        self.log("\nUpdate timing check:", level=2)
        self.log(f"Current time: {now}", level=2)
        self.log(f"Last update: {last_update}", level=2)
        self.log(f"Time since last update: {time_diff}", level=2)
        
        if options['force']:
            self.log("FORCE UPDATE requested", level=1)
            return True
            
        if time_diff < timedelta(days=1):
            self.log("Skipping - less than 1 day since last update", level=1)
            return False
            
        return True

    def get_plan_rates(self, plan_name):
        """Get rates with validation"""
        rates = {
            "quick-gain": {'daily': Decimal('0.02107'), 'weekly': Decimal('0.2'), 'monthly': Decimal('0.866')},
            "rapid-growth": {'daily': Decimal('0.0251'), 'weekly': Decimal('0.25'), 'monthly': Decimal('1.0')},
            "aggressive-boost": {'daily': Decimal('0.0251'), 'weekly': Decimal('0.25'), 'monthly': Decimal('1.0825')},
            "accelerated-wealth": {'daily': Decimal('0.0287'), 'weekly': Decimal('0.3'), 'monthly': Decimal('1.2')},
            "ultimate-prosperity": {'daily': Decimal('0.0287'), 'weekly': Decimal('0.3'), 'monthly': Decimal('1.299')},
        }
        
        if plan_name not in rates:
            self.log(f"Warning: Unknown plan '{plan_name}' - using 'quick-gain' rates", level=1)
            
        return rates.get(plan_name, rates["quick-gain"])

    def calculate_values(self, investment, rates):
        """Perform all calculations with logging"""
        calculations = {}
        
        try:
            amount = Decimal(str(investment.amount))
            current_value = Decimal(str(investment.current_value or investment.amount))
            
            self.log("\nCalculations:", level=2)
            
            # Daily calculation
            calculations['daily_interest'] = current_value * rates['daily']
            calculations['new_value'] = current_value + calculations['daily_interest']
            
            self.log(f"Daily rate: {rates['daily']}%", level=2)
            self.log(f"Daily interest: {calculations['daily_interest']}", level=2)
            
            # Weekly calculation (if needed)
            if self.is_weekly_update(investment):
                calculations['weekly_interest'] = current_value * rates['weekly']
                self.log(f"Weekly interest: {calculations['weekly_interest']}", level=2)
                
            # Monthly calculation (if needed)
            if self.is_monthly_update(investment):
                calculations['monthly_interest'] = amount * rates['monthly']
                self.log(f"Monthly interest: {calculations['monthly_interest']}", level=2)
                
        except Exception as e:
            self.error(f"Calculation error: {str(e)}")
            raise
            
        return calculations

    def apply_updates(self, investment, calculations):
        """Apply updates to the investment"""
        now = timezone.now()
        
        investment.current_value = str(round(calculations['new_value'], 2))
        investment.daily_interest = str(round(calculations['daily_interest'], 2))
        investment.daily_roi_date = now
        
        if 'weekly_interest' in calculations:
            investment.weekly_interest = str(round(calculations['weekly_interest'], 2))
            investment.weekly_roi_date = now
            
        if 'monthly_interest' in calculations:
            investment.monthly_interest = str(round(calculations['monthly_interest'], 2))
            investment.monthly_roi_date = now
            
        investment.save()

    def log_update_summary(self, investment, calculations):
        """Log the results of the update"""
        self.log("\nUPDATE SUMMARY:", level=1)
        self.log(f"New value: {calculations['new_value']}", level=1)
        self.log(f"Daily interest applied: {calculations['daily_interest']}", level=2)
        
        if self.simulate:
            self.log("SIMULATION MODE - No changes saved", level=1)
        else:
            self.log("Changes saved to database", level=2)

    def is_weekly_update(self, investment):
        """Check if weekly update is needed"""
        last_weekly = investment.weekly_roi_date or investment.investment_date
        return (timezone.now() - last_weekly).days >= 7

    def is_monthly_update(self, investment):
        """Check if monthly update is needed"""
        last_monthly = investment.monthly_roi_date or investment.investment_date
        return (timezone.now() - last_monthly).days >= 30

    def log(self, message, level=1):
        """Helper for consistent logging"""
        if self.verbose or level == 1:
            self.stdout.write(message)

    def error(self, message):
        """Helper for error logging"""
        self.stderr.write(f"ERROR: {message}")