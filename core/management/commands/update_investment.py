# management/commands/update_investments.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import InvestmentPlan
from decimal import Decimal, getcontext
import logging

# Set higher precision for Decimal calculations
getcontext().prec = 10

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updates investment values daily according to plan-specific rates'

    def handle(self, *args, **options):
        investments = InvestmentPlan.objects.filter(status="Pending")
        
        for investment in investments:
            try:
                self.update_investment(investment)
            except Exception as e:
                logger.error(f"Error updating investment {investment.id}: {str(e)}")
                # Consider adding error notification here

    def get_plan_rates(self, plan_name):
        """Returns accurate daily, weekly, and monthly rates for each plan"""
        rates = {
            "quick-gain": {
                "daily": Decimal('0.02107'),  # 2.107% daily
                "weekly": Decimal('0.2'),     # 20% weekly
                "monthly": Decimal('0.866')   # 86.6% monthly
            },
            "rapid-growth": {
                "daily": Decimal('0.0251'),   # 2.51% daily
                "weekly": Decimal('0.25'),    # 25% weekly
                "monthly": Decimal('1.0')    # 100% monthly
            },
            "aggressive-boost": {
                "daily": Decimal('0.0251'),  # 2.51% daily
                "weekly": Decimal('0.25'),   # 25% weekly
                "monthly": Decimal('1.0825') # 108.25% monthly (corrected)
            },
            "accelerated-wealth": {
                "daily": Decimal('0.0287'),   # 2.87% daily
                "weekly": Decimal('0.3'),     # 30% weekly
                "monthly": Decimal('1.2')    # 120% monthly
            },
            "ultimate-prosperity": {
                "daily": Decimal('0.0287'),   # 2.87% daily
                "weekly": Decimal('0.3'),     # 30% weekly
                "monthly": Decimal('1.299')   # 129.9% monthly (corrected)
            }
        }
        return rates.get(plan_name, rates["quick-gain"])  # Default to quick-gain if plan not found

    def update_investment(self, investment):
        now = timezone.now()
        last_update = investment.daily_roi_date or investment.investment_date
        days_since_last_update = (now - last_update).days

        if days_since_last_update < 1:
            return  # No update needed yet

        # Get rates based on investment plan
        rates = self.get_plan_rates(investment.investment_plan)
        amount = Decimal(investment.amount)
        
        # Calculate current value with compound interest
        current_value = Decimal(investment.current_value or investment.amount)
        
        # Calculate daily interest (compounding)
        daily_interest = current_value * rates["daily"]
        new_value = current_value + daily_interest
        
        # Update investment fields
        investment.current_value = str(round(new_value, 2))
        investment.daily_interest = str(round(daily_interest, 2))
        investment.daily_roi = str(round(rates["daily"] * 100, 4))  # Show 4 decimal places for accuracy
        investment.daily_roi_date = now
        
        # Add to transactions history
        transaction_msg = (
            f"Daily ROI: ${round(float(daily_interest), 2)} "
            f"({rates['daily']*100:.4f}%) on {now.date()}"
        )
        investment.daily_transactions.append(transaction_msg)

        # Weekly update (every 7 days)
        if days_since_last_update % 7 == 0:
            weekly_interest = current_value * rates["weekly"]
            investment.weekly_interest = str(round(weekly_interest, 2))
            investment.weekly_roi = str(round(rates["weekly"] * 100, 2))
            investment.weekly_roi_date = now
            investment.daily_transactions.append(
                f"Weekly ROI: ${round(float(weekly_interest), 2)} "
                f"({rates['weekly']*100:.2f}%) on {now.date()}"
            )

        # Monthly update (after 30 days)
        days_invested = (now - investment.investment_date).days
        if days_invested >= 30 and (days_invested % 30 == 0 or not investment.monthly_roi_date):
            monthly_interest = amount * rates["monthly"]  # On principal amount
            investment.monthly_interest = str(round(monthly_interest, 2))
            investment.monthly_roi = str(round(rates["monthly"] * 100, 2))
            investment.monthly_roi_date = now
            investment.daily_transactions.append(
                f"Monthly ROI: ${round(float(monthly_interest), 2)} "
                f"({rates['monthly']*100:.2f}%) on {now.date()}"
            )

        # Check if investment duration has completed
        investment_duration = int(investment.investment_duration or 0)
        if investment_duration > 0 and days_invested >= investment_duration * 30:
            investment.status = "Completed"
            investment.daily_transactions.append(
                f"Investment completed on {now.date()} "
                f"with final value: ${round(float(new_value), 2)}"
            )

        investment.save()
        logger.info(f"Updated investment {investment.id} - New value: {investment.current_value}")