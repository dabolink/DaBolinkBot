from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect


class Features(View):
    def get(self, request):
        return render(request, 'homelogin/features.html')


class Contact(View):
    def get(self, request):
        return render(request, 'homelogin/contact.html')


class Home(View):
    def get(self, request):
        return render(request, 'homelogin/home.html')


class Twitch(View):
    def get(self, request):
        return HttpResponseRedirect(
            'https://api.twitch.tv/kraken/oauth2/authorize?response_type=code&client_id=hkqcg5olgs65atdx08q516aqm154c9a&redirect_uri=http://localhost:8000'
        )
        #  twitch also takes &scope= and &state=