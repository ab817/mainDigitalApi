from django.urls import path
from . import views

urlpatterns = [
    path('send-unicast-sms/', views.send_unicast_sms, name='send_unicast_sms'),
    path('send-bulk-sms/', views.send_bulk_sms, name='send_bulk_sms'),
    path('sms-report/', views.sms_report, name='sms_report'),
]
