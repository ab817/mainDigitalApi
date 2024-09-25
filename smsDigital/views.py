import requests
from django.shortcuts import render, redirect
from .forms import UnicastSMSForm, BulkSMSForm
from .models import SMSLog
from django.contrib.auth.decorators import login_required

@login_required
#unicast
def send_unicast_sms(request):
    if request.method == 'POST':
        form = UnicastSMSForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            message = form.cleaned_data['message']
            # API call to send SMS
            url = (
                f"http://{os.getenv('SMS_API_IP')}/http.aspx?"
                f"guid={os.getenv('SMS_API_GUID')}&"
                f"username={os.getenv('SMS_API_USERNAME')}&"
                f"password={os.getenv('SMS_API_PASSWORD')}&"
                f"countryCode=np&"
                f"mobileNumber=%2b{mobile_number}&"
                f"message={message}"
            )
            response = requests.get(url)
            status = 'Sent' if response.status_code == 200 else 'Failed'
            # Log the SMS
            SMSLog.objects.create(
                mobile_number=mobile_number,
                message=message,
                status=status,
                response=response.text
            )
            return redirect('sms_report')  # Redirect to reporting page after sending
    else:
        form = UnicastSMSForm()

    return render(request, 'send_unicast_sms.html', {'form': form})


#bulkmessage
import pandas as pd

@login_required
def send_bulk_sms(request):
    if request.method == 'POST':
        form = BulkSMSForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                mobile_number = row['mobile_number']
                message = row['message']
                # Send SMS for each row
                # Construct the URL using environment variables
                url = (
                    f"http://{os.getenv('SMS_API_IP')}/http.aspx?"
                    f"guid={os.getenv('SMS_API_GUID')}&"
                    f"username={os.getenv('SMS_API_USERNAME')}&"
                    f"password={os.getenv('SMS_API_PASSWORD')}&"
                    f"countryCode=np&"
                    f"mobileNumber=%2b{mobile_number}&"
                    f"message={message}"
                )
                response = requests.get(url)
                status = 'Sent' if response.status_code == 200 else 'Failed'
                # Log the SMS
                SMSLog.objects.create(
                    mobile_number=mobile_number,
                    message=message,
                    status=status,
                    response=response.text
                )
            return redirect('sms_report')  # Redirect to reporting page after bulk SMS
    else:
        form = BulkSMSForm()

    return render(request, 'send_bulk_sms.html', {'form': form})

@login_required
#reporting
def sms_report(request):
    logs = SMSLog.objects.all().order_by('-sent_at')
    return render(request, 'sms_report.html', {'logs': logs})