from django.forms import ModelForm

from django import forms
from .models import Settings, Search, Title

class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ('follow_message', 'timeout_time', 'freq_viewer_time')
    follow_message = forms.CharField(label="Follow Message", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Follow Message'}))
    timeout_time = forms.IntegerField(label="Timeout time", label_suffix="(seconds)", required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Timeout Time'}))
    freq_viewer_time = forms.IntegerField(label="Frequent Viewer Time", label_suffix="(hours)", required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Frequent Viewer Time'}))


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ('search_text',)
    search_text = forms.CharField(required=False)

class TitleForm(ModelForm):
    class Meta:
        model = Title
        fields = ('broadcast_title', 'game')
    broadcast_title = forms.CharField(required=False)
    game = forms.CharField(required=False)