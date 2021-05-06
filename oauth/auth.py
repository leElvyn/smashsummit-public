from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth import login

class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, mail):
        user = User.objects.get(email=mail)
        if user is not None:
            return user