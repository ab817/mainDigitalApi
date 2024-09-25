from django.contrib import admin
from .models import SMSLog

class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'message', 'status', 'sent_at')
    search_fields = ('mobile_number', 'message', 'status')
    list_filter = ('status', 'sent_at')

admin.site.register(SMSLog, SMSLogAdmin)
