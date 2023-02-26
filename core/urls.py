from django.urls import path
from .views import (
    invest,
    DashboardView,
    profile,
    VerificationView,
    home,
    add_to_transaction
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('add-to-transaction/<slug>/', add_to_transaction, name='add-to-transactions'),
    path('dashboard/<slug>/', DashboardView.as_view(), name='profile'),
    path('start-investing/', invest, name='invest'),
    path('accounts/deposit/verification', VerificationView.as_view(), name='verification')
  
]
