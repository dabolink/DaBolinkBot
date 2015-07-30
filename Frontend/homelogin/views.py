from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse
from __init__ import d, features

import requests
import json

from .forms import SettingsForm, SearchForm


class Home(View):
    def post(self, request):
        username = request.session.get('username')
        if not username:
            return render(request, 'homelogin/home.html', {"backend_server_ip": d["backend_server_ip"], "features": features})
        botstatus = requests.get(d["backend_server_ip"] + "/dabolinkbot/api/v1.0/bot/status/" + username).json()["online"]
        if 'settings' in request.POST:
            form = SettingsForm(request.POST)
            form2 = SearchForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                channel = username
                follow_message = cd.get("follow_message")
                timeout_time = cd.get("timeout_time")
                freq_viewer_time = cd.get("freq_viewer_time")
                header = {'Content-Type': 'application/json'}
                j = dict()
                j["channel"] = channel
                if follow_message:
                    j["follow_message"] = follow_message
                if timeout_time:
                    j["timeout_time"] = timeout_time
                if freq_viewer_time:
                    j["freq_viewer_time"] = freq_viewer_time
                print j
                print requests.post("http://localhost:5000/dabolinkbot/api/v1.0/channel/settings/{}".format(channel), json=j, headers=header).text
        elif 'logout' in request.POST:
            request.session.flush()
            form = SettingsForm(request.POST)
            form2 = SearchForm(request.POST)
        buttonclass = "btn-success" if botstatus else "btn-danger"
        botstatus = "Online" if botstatus else "Offline"
        return render(request, 'homelogin/home.html',
              {"features": features, "username": username, "botstatus": botstatus, "buttonclass": buttonclass,
               "backend_server_ip": d["backend_server_ip"], "form": form, "form2": form2})

    def get(self, request):
        print request.method
        code = request.GET.get('code', '')
        if request.method == "GET":
            print "request GET", request.GET.get('?')
        username = None
        if request.session.get('username'):
            username = request.session.get('username')
        print username, code
        if code != "" or username:
            print "logged in"
            # Use the twitch supplied login code if it is present to get an access token
            payload = {"client_id": d["client_id"], "client_secret": d["client_secret"],
                       "grant_type": "authorization_code", "redirect_uri": d["redirect_uri"], "code": code}
            if not username:
                token_response = requests.post('https://api.twitch.tv/kraken/oauth2/token', data=payload)
                # Use access token to get user info
                token_response_json = json.loads(token_response.text)
                try:
                    authorization_header = {'Authorization': 'OAuth ' + token_response_json['access_token']}
                except KeyError:
                    print "error", token_response_json
                    return render(request, 'homelogin/home.html')
                username = requests.get('https://api.twitch.tv/kraken/user', headers=authorization_header).json()[
                "name"]
                request.session["username"] = username
                print "cookie set"
            userData = requests.get(d["backend_server_ip"] + "/dabolinkbot/api/v1.0/channel/settings/" + username).json()
            print userData["follow_message"]
            form = SettingsForm(request.POST)
            form2 = SearchForm(request.POST)
            for key in userData:
                if not key == "channel":
                    print key
                    form.data[key] = userData[key]
            print form.fields
            botstatus = requests.get(d["backend_server_ip"] + "/dabolinkbot/api/v1.0/bot/status/" + username).json()[
                "online"]
            buttonclass = "btn-success" if botstatus else "btn-danger"
            botstatus = "Online" if botstatus else "Offline"
            print userData
            print request.session
            return render(request, 'homelogin/home.html',
                          {"features": features, "username": username, "botstatus": botstatus, "buttonclass": buttonclass,
                           "backend_server_ip": d["backend_server_ip"], "form": form, "form2": form2})
        elif not username:
            print "no username"
            form2 = SearchForm(request.POST)
            return render(request, 'homelogin/home.html', {"backend_server_ip": d["backend_server_ip"], "features": features, "form2": form2})


class Twitch(View):
    def get(self, request):
        print repr(d["client_id"])
        print repr(d["redirect_uri"])
        redirectString = 'https://api.twitch.tv/kraken/oauth2/authorize?response_type=code&client_id=' + d["client_id"] + '&redirect_uri=' + d["redirect_uri"] + "&scope=user_read"
        return HttpResponseRedirect(redirectString)
        #  twitch also takes &scope= and &state=


class User(View):
    def get(self, request):
        return render(request, 'homelogin/user.html', {})

    def post(self, request):
        if 'user' in request.POST:
            search = SearchForm(request.POST)
            if search.is_valid():
                cd = search.cleaned_data
                user = cd.get("search_text")
                print user
        print "here"