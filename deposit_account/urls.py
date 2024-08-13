from django.urls import path
from .views import *

app_name = 'deposit_account_urls'

urlpatterns = [
    path('create/', AccountDetails.as_view(), name='account-create'),
    path('view/', AccountDetails.as_view(), name='account-view'),
    path('transfer/<int:pk>/', TransferFunds, name='account-transfer'),
    path('view/', TransferHistory, name='account-transfer=history'),
]