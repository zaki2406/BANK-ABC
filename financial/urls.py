# your_app/urls.py
from django.urls import path
from .views import FinancialDataView

urlpatterns = [
    path('api/financial-data/', FinancialDataView.as_view(), name='financial-data'),
]
