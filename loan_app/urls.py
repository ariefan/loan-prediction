from django.urls import path
from .views import PredictLoan

urlpatterns = [
    path('predict/', PredictLoan.as_view(), name='predict_loan'),
]