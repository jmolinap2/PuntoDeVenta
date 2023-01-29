from django.urls import path

from core.reports.views import *

urlpatterns = [
    # reports
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
    path('client/', ReportClientView.as_view(), name='client_report'),
]