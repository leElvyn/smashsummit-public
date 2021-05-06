from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.discord_login, name="login"),
    path('redirect/', views.login_redirect, name="redirect"),
    path('unothorized/', views.unothorized, name="unothorized")
]