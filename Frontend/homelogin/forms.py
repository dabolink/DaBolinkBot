from django.forms import ModelForm

from django import forms
from .models import Settings

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ('follow_message', 'timeout_time', 'freq_viewer_time')
    follow_message = forms.CharField(required=False)
    timeout_time = forms.IntegerField(required=False)
    freq_viewer_time = forms.IntegerField(required=False)
