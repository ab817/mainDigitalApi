import os
import time
import requests
import pandas as pd
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import UnicastSMSForm, BulkSMSForm
from .models import SMSLog, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .decorators import role_required

@login_required
@role_required(allowed_roles=['RoleDepartment','RoleBranch','RoleDigital', 'super'])
def send_unicast_sms(request):
    if request.method == 'POST':
        form = UnicastSMSForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            message = form.cleaned_data['message']

            user_profile = UserProfile.objects.get(user=request.user)

            if user_profile.sms_count <= 0:
                return render(request, 'send_unicast_sms.html', {
                    'form': form,
                    'error': 'SMS limit reached. Please contact admin.'
                })

            # API call to send SMS
            url = (
                f"http://{os.getenv('SMS_API_IP')}/http.aspx?"
                f"guid={os.getenv('SMS_API_GUID')}&"
                f"username={os.getenv('SMS_API_USERNAME')}&"
                f"password={os.getenv('SMS_API_PASSWORD')}&"
                f"countryCode=np&"
                f"mobileNumber=%2b977{mobile_number}&"
                f"message={message}"
            )

            response = requests.get(url)
            response_text = response.text

            # Determine status based on response
            if "Message received" in response_text:
                status = 'Sent'
            elif "Invalid SMS123Go username or password" in response_text:
                status = 'Failed: Invalid credentials'
            elif "Failed sending message" in response_text:
                status = 'Failed: Invalid mobile number'
            else:
                status = 'Failed: Unknown error'

            # Log the SMS along with the user
            SMSLog.objects.create(
                mobile_number=mobile_number,
                message=message,
                status=status,
                response=response_text,
                user=request.user , # Log the user who sent the SMS
                sent_at = timezone.now()
            )

            if status == 'Sent':
                user_profile.sms_count -= 1  # Decrement sms_count
                user_profile.save()  # Save the updated count

            return redirect('sms_report')  # Redirect to reporting page after sending
    else:
        form = UnicastSMSForm()

    return render(request, 'send_unicast_sms.html', {'form': form})


# Bulk SMS
@login_required
@role_required(allowed_roles=['RoleDepartment','RoleDigital','RoleBranch', 'super'])
def send_bulk_sms(request):
    if request.method == 'POST':
        form = BulkSMSForm(request.POST, request.FILES)
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.sms_count <= 0:
            return render(request, 'send_bulk_sms.html', {
                'form': form,
                'error': 'SMS limit reached. Please contact admin.'
            })

        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                mobile_number = row['mobile_number']
                message = row['message']

                # Construct the URL using environment variables
                url = (
                    f"http://{os.getenv('SMS_API_IP')}/http.aspx?"
                    f"guid={os.getenv('SMS_API_GUID')}&"
                    f"username={os.getenv('SMS_API_USERNAME')}&"
                    f"password={os.getenv('SMS_API_PASSWORD')}&"
                    f"countryCode=np&"
                    f"mobileNumber=%2b977{mobile_number}&"
                    f"message={message}"
                )
                response = requests.get(url)
                response_text = response.text

                # Determine status based on response
                if "Message received" in response_text:
                    status = 'Sent'
                elif "Invalid SMS123Go username or password" in response_text:
                    status = 'Failed: Invalid credentials'
                elif "Failed sending message" in response_text:
                    status = 'Failed: Invalid mobile number'
                else:
                    status = 'Failed: Unknown error'

                # Log the SMS along with the user
                SMSLog.objects.create(
                    mobile_number=mobile_number,
                    message=message,
                    status=status,
                    response=response_text,
                    user=request.user,  # Log the user who sent the SMS
                    sent_at = timezone.now()
                )

                if status == 'Sent':
                    user_profile.sms_count -= 1
                    user_profile.save()

                # Introduce a 1-second delay before sending the next SMS
                time.sleep(1)

            return redirect('sms_report')  # Redirect to reporting page after bulk SMS
    else:
        form = BulkSMSForm()

    return render(request, 'send_bulk_sms.html', {'form': form})


@login_required
@role_required(allowed_roles=['super'])
def sms_report(request):
    logs = SMSLog.objects.all().order_by('-sent_at')
    paginator = Paginator(logs, 20)  # Show 20 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert the sent_at timestamps to local time
    for log in page_obj:
        log.sent_at = timezone.localtime(log.sent_at)

    context = {
        'logs_page_obj': page_obj,
    }
    return render(request, 'sms_report.html', context)

def logout(request):
    auth_logout(request)
    return redirect('login')