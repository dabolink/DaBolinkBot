from django.forms import ModelForm

from django import forms
from .models import Settings, Search

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ('follow_message', 'timeout_time', 'freq_viewer_time')
    follow_message = forms.CharField(required=False)
    timeout_time = forms.IntegerField(required=False)
    freq_viewer_time = forms.IntegerField(required=False)


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ('search_text',)
    search_text = forms.CharField(required=False)
