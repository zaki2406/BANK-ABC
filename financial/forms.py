# financial/forms.py

from django import forms

class ReportUploadForm(forms.Form):
    file = forms.FileField(label='Select a file')
