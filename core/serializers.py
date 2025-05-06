from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Wallets, Deposits, Transaction, InvestmentPlan, Banks

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
    
class BankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Banks
        fields = ['bank_name', 'bank_address', 'account_number', 'account_name', 'swift_code', 'routing_number', 'state', 'slug']
        read_only_fields = ['slug']
class DepositSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deposits
        fields = ['amount']
        

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'email', 'amount', 'type', 'status', 'transaction_date', 'transaction_id', 'payment_method', 'crypto_currrency', 'slug', ]
        

class InvestmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = ['id', 'email', 'amount', 'investment_plan', 'status', 'investment_duration', 'investment_date', 'current_value', 'average_return', 'daily_roi', 'weekly_roi', 'monthly_roi',  'daily_roi_date', 'weekly_roi_date', 'monthly_roi_date', 'daily_interest', 'weekly_interest', 'monthly_interest', 'expected_return', ]
        
class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallets
        fields = ['id', 'user', 'balance', 'all_time_roi', 'this_week_roi', 'this_month_roi',  'profit_margin']
        

