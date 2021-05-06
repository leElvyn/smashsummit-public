from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import time
import os
# Create your views here.
if os.environ.get('DEBUG_MODE') == None:
    oauth_url = 'https://discord.com/api/oauth2/authorize?client_id=771066899802882110&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth%2Fredirect&response_type=code&scope=identify%20email'
    red_url = 'http://127.0.0.1:8000'
else:
    oauth_url = "https://discord.com/api/oauth2/authorize?client_id=771066899802882110&redirect_uri=https%3A%2F%2Fleelvyn.me%2Fauth%2Fredirect&response_type=code&scope=identify%20email"
    red_url = 'https://leelvyn.me'

def discord_login(request):
    return redirect(oauth_url)

def login_redirect(request):
    code = request.GET.get('code')
    user = exchange_code(code)
    mail = user["email"]
    try:
        user = User.objects.get(email=mail)
    except User.DoesNotExist:
        return redirect('/auth/unothorized')
    if user is not None:
        login(request, user)
    return redirect('/')

def unothorized(request):
    return render(request, 'oauth/login.html')

def exchange_code(code):
    data = {
        "client_id": "",
        "client_secret": "",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{red_url}/auth/redirect",
        "scope": "identify messages.read",
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    r = requests.post('https://discord.com/api/v6/oauth2/token', data=data, headers=headers)
    credentials = r.json()
    access_token = credentials["access_token"]
    print(access_token)
    response = requests.get("https://discord.com/api/v6/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    user = response.json()
    return user