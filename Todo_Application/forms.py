from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.forms import SplitDateTimeField

class DTForms(forms.Form):
    title = forms.CharField(max_length=64)
    date_time_input = SplitDateTimeField(widget=AdminSplitDateTime())