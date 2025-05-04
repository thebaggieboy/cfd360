from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Wallets, Deposits, Transaction, InvestmentPlan

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
    
    
class DepositSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deposits
        fields = ['amount']
        

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'email', 'amount', 'type', 'status', 'transaction_date', 'transaction_id']
        

class InvestmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = ['id', 'email', 'amount', 'investment_plan', 'status', 'investment_duration', 'investment_date', 'daily_roi', 'weekly_roi', 'monthly_roi', 'weekly_roi_date', 'monthly_roi_date']
        
class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallets
        fields = ['id', 'user', 'balance', 'all_time_roi', 'this_week_roi', 'this_month_roi',  'profit_margin']
        

