from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

User = settings.AUTH_USER_MODEL
CRYPTOCURRENCY_CHOICES = (
  
    ("Bitcoin", "Bitcoin"),
    ("Ethereum", "Ethereum"),
    ("USDC", "USDC"),
    ("Litecoin", "Litecoin"),  
    ("Tether", "Tether"),
    ("Solana", "Solana"),
    ("Tron", "Tron"),
    ("Polygon", "Polygon"),
  
)


 
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
STATUS = (
	('Pending', 'Pending'), 
	('Completed', 'Completed')
)
VERIFICATION_STATUS = (
	('Pending', 'Pending'), 
	('Verified', 'Verified')
)

TRANSACTION_PAYMENT_METHOD = (
    ('Bank', 'Bank'), 
    ('Crypto', 'Crypto'),
    ('Card', 'Card'),
   
)

WITHDRAW_CHOICE = (
    
	('Bank', 'Bank'), 
    ('Crypto', 'Crypto'),
    
)



class Wallets(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True)
    
    address = models.CharField(max_length=250, null=True, blank=True, default='')
    balance = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    profit_margin = models.FloatField(max_length=250, null=True, blank=True, default=0.0)
    transactions = models.ForeignKey('Transaction', null=True, blank=True, on_delete=models.CASCADE)
    
    slug = models.SlugField(max_length=250,null=True, blank=True)
    today = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    this_week = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    this_month = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    today_roi = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    this_week_roi = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    this_month_roi = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    all_time_roi = models.CharField(max_length=250, blank=True, null=True, default=0.0)
    
    date_created = models.DateTimeField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} Wallet')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})
	
    def __str__(self):
        return f'{self.user} wallet'

class Banks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True)
    bank_name = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    bank_address = models.CharField(max_length=250, null=True, blank=True)
    account_number = models.CharField(max_length=250, null=True, blank=True)
    account_name = models.CharField(max_length=250, null=True, blank=True)
    swift_code = models.CharField(max_length=250, null=True, blank=True)
    routing_number = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250,null=True, blank=True, )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} bank')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def __str__(self):
	    return f'{self.user.email} banks'


class Deposits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True, )
    amount = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    quick_trade = models.CharField(max_length=250, null=True, blank=True)
    payment_method = models.CharField(max_length=250, null=True, blank=True, choices=WITHDRAW_CHOICE, default='Bitcoin')
    crypto_currrency = models.CharField(max_length=250, null=True, blank=True, choices=CRYPTOCURRENCY_CHOICES, default='Bitcoin')
    
    slug = models.SlugField(max_length=250,null=True, blank=True, )
    status = models.CharField(choices=STATUS, default="Pending", max_length=250, null=True, blank=True)
    date_created = models.DateTimeField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.user.email} ${self.amount} {self.status} {self.date_created}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def __str__(self):
	    return f'{self.user} deposited ${self.amount}'  

class Transaction(models.Model):
    email = models.CharField(max_length=250, null=True, blank=True, default='')
    amount = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.DateTimeField(max_length=250, null=True, blank=True)
    transaction_id = models.CharField(max_length=250, null=True, blank=True, default='')
    payment_method = models.CharField(max_length=250, null=True, blank=True, choices=TRANSACTION_PAYMENT_METHOD, default='Crypto')
    crypto_currrency = models.CharField(max_length=250, null=True, blank=True, choices=CRYPTOCURRENCY_CHOICES, default='Bitcoin')
    
    slug = models.SlugField(max_length=250,blank=True, null=True)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def get_add_to_transaction_url(self):
        return reverse("core:add-to-transaction", kwargs={
            'slug': self.slug
        })

    def __str__(self):
	    return f'{self.user.email} {self.date_created}'

class InvestmentPlan(models.Model):
   
    email = models.CharField(max_length=250, null=True, blank=True)
    amount = models.IntegerField()
    investment_plan = models.CharField(max_length=250, null=True, blank=True)
    investment_duration = models.CharField(max_length=250, null=True, blank=True)
    investment_date = models.DateTimeField(max_length=250, null=True, blank=True)
    status = models.CharField(choices=STATUS, default="Pending", max_length=250, null=True, blank=True)
    expected_return = models.CharField(max_length=250, null=True, blank=True)
    current_value = models.CharField(max_length=250, null=True, blank=True)
    average_return = models.CharField(max_length=250, null=True, blank=True)
    
    daily_roi = models.CharField(max_length=250, null=True, blank=True)
    weekly_roi = models.CharField(max_length=250, null=True, blank=True)
    monthly_roi = models.CharField(max_length=250, null=True, blank=True)
    
    daily_interest = models.CharField(max_length=250, null=True, blank=True)
    weekly_interest = models.CharField(max_length=250, null=True, blank=True)
    monthly_interest = models.CharField(max_length=250, null=True, blank=True)
    daily_roi_date = models.DateTimeField(max_length=250, null=True, blank=True)
    weekly_roi_date = models.DateTimeField(max_length=250, null=True, blank=True)
    monthly_roi_date = models.DateTimeField(max_length=250, null=True, blank=True)
    
    daily_interest_date = models.DateTimeField(max_length=250, null=True, blank=True)
    daily_transactions = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
                                             
    slug = models.SlugField(max_length=250,null=True, blank=True)


    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def __str__(self):
	    return f'{self.user.email} investment plans'



class Withdraw(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,max_length=250, null=True, blank=True,)
    amount = models.CharField(max_length=250, null=True, blank=True)
    withdrawal_method = models.CharField(choices=WITHDRAW_CHOICE, default='Bitcoin', max_length=250, null=True, blank=True)
    status = models.CharField(choices=STATUS, default="Pending", max_length=250, null=True, blank=True)
    withdrawal_date = models.DateTimeField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=250,null=True, blank=True)


    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug":self.slug})

    def __str__(self):
	    return f'{self.user.email} withdrawals'





class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


