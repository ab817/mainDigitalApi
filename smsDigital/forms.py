from django import forms

class UnicastSMSForm(forms.Form):
    mobile_number = forms.CharField(max_length=15, label="Mobile Number")
    message = forms.CharField(widget=forms.Textarea, label="Message")

class BulkSMSForm(forms.Form):
    excel_file = forms.FileField(label="Upload Excel File")
