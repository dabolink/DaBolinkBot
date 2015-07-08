from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse
import requests
import json


class Home(View):
    def get(self, request):
        code = request.GET.get('code', '')
        if code != '':
            # Use the twitch supplied login code if it is present to get an access token
            payload = {"client_id": "hkqcg5olgs65atdx08q516aqm154c9a", "client_secret": "3tmlse74r6z2yj95omk9kc3h8oah6d9", "grant_type": "authorization_code", "redirect_uri": "http://localhost:8000", "code": code}
            token_response = requests.post('https://api.twitch.tv/kraken/oauth2/token', data=payload)
            # Use access token to get user info
            token_response_json = json.loads(token_response.text)
            try:
                authorization_header = {'Authorization': 'OAuth ' + token_response_json['access_token']}
            except KeyError:
                return render(request, 'homelogin/home.html')
            username = requests.get('https://api.twitch.tv/kraken/user', headers=authorization_header).json()["display_name"]
            botstatus = requests.get('http://localhost:5000/dabolinkbot/api/v1.0/bot/status/'+username).json()["online"]            
            buttonclass = "btn-success" if botstatus else "btn-danger"
            botstatus = "Online" if botstatus else "Offline"
            return render(request, 'homelogin/home.html', {"username": username, "botstatus": botstatus, "buttonclass": buttonclass})
        else:
            return render(request, 'homelogin/home.html')


class Twitch(View):
    def get(self, request):
        return HttpResponseRedirect(
            'https://api.twitch.tv/kraken/oauth2/authorize?response_type=code&client_id=hkqcg5olgs65atdx08q516aqm154c9a&redirect_uri=http://localhost:8000&scope=user_read'
        )
        #  twitch also takes &scope= and &state=