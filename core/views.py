import random
import string
from django.shortcuts import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, CreateView, TemplateView, UpdateView
from django.contrib import messages
from .models import Transaction, Deposits, Withdraw, Wallets
from accounts.models import  Profile
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from .serializers import DepositSerializer, WalletSerializer, TransactionSerializer

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class DashboardView(DetailView):
    context_object_name = 'profile'
    model = Profile
    template_name = 'account/profile.html'
    

class DepositFormView(CreateView):
    model = Deposits
    template_name = 'account/profile.html'
    


def invest(request, slug):
    profile = get_object_or_404(UserProfile, slug=slug)
    d_form = DepositForm()
    if request.method  == 'POST':
        d_form = DepositForm(request.POST)
        if d_form.is_valid():
            d_form.save()
            redirect('core:profile', slug=slug)

    return render(request, 'start_investing.html', {'profile':profile, 'd_form':d_form})


class BaseView(CreateView):
    context_object_name = "base"
    model = Wallets
    template_name = 'index.html'
    





'''class StartInvesting(CreateView):
    model = UserProfile
    template_name = 'start_investing.html'
    fields = ['quick_trade']
'''
class VerificationView(TemplateView):
    template_name = "account/verification.html"

"""class TermsAndConditionsView(TemplateView):
    template_name = "account/verification.html"

class PrivacyView(TemplateView):
    template_name = "account/verification.html"
"""
def profile(request, slug):
    profile = UserProfile.objects.filter(user=request.user, slug=slug)
    form = ProfileForm()
    d_form = DepositForm()
    w_form = WithdrawForm()
    if request.method  == 'POST':
        form = ProfileForm(request.POST)
        d_form = DepositForm(request.POST)
        w_form = WithdrawForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Your profile has been updated, successfully")
            return redirect('core:profile', slug=slug)

        if d_form.is_valid():
            deposit = d_form.save(commit=False)        
            deposit.user = request.user
            deposit.save()
            messages.success(request, "Your deposit was submitted and added to the queue")
            return redirect('core:profile', slug=slug)
        
        if w_form.is_valid():
            withdraw = w_form.save(commit=False)
            withdraw.user = request.user
            withdraw.save()
            messages.success(request, "You withdrawal is pending")
            return redirect('core:profile', slug=slug)
    return render(request, 'account/profile.html',  {
            'profile':profile, 'form':form, 'd_form':d_form, 'w_form':w_form
        })


def home(request):
    if request.user.is_authenticated:
        p_slug = slugify(request.user.email)
        link = (f'/dashboard/{p_slug}')
    else:
        link = '/'

    return render(request, 'index.html', {'link':link})
        

def withdraw(request, slug):
    withdraw = get_object_or_404(Withdraw, slug=slug)
    wallet = get_object_or_404(Wallets, slug=slug)
    profile = UserProfile.objects.all()
   
    if request.method == 'POST':        
        return HttpResponseRedirect(f"/dashboard/{profile.slug}/")

    else:
        return render(request, 'index.html')


@login_required
def add_to_transaction(request, slug):
    deposits = get_object_or_404(Deposits, slug=slug)
    withdraw = get_object_or_404(Withdraw, slug=slug)
    transaction, created = Transaction.objects.get_or_create(
        
        user=request.user,
        deposit=deposits,
        withdraw=withdraw,
        status='Pending'
    )
    transaction_qs = Transaction.objects.filter(user=request.user, status='Pending')
    if transaction_qs.exists():
        current_transaction = transaction_qs[0]

        if current_transaction.deposits.filter(deposits__amount=deposits.amount).exists():
            deposits.amount += current_transaction.amount
            deposits.save()
    else:
        transaction_date = timezone.now()
        current_transaction = Transaction.objects.create(
            user=request.user, date_created=transaction_date)
        transaction.deposits.add(current_transaction)
        messages.info(request, "A new transaction has been started, please wait for manual verification from our support")
        return redirect("core:profile")




 

class DepositViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Deposits.objects.all().order_by('-date_created')
    serializer_class = DepositSerializer
    #permission_classes = [permissions.IsAuthenticated]

class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    #permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    #permission_classes = [permissions.IsAuthenticated]
