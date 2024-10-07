from django.contrib import admin
from .models import SMSLog, UserProfile


class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'message', 'status', 'sent_at', 'user')
    search_fields = ('mobile_number', 'message', 'status')
    list_filter = ('status', 'sent_at')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sms_count')
    search_fields = ('user__username',)


admin.site.register(SMSLog, SMSLogAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
