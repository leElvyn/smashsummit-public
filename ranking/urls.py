from django.urls import path, include, re_path
from rest_framework import routers
from . import views
from oauth.views import discord_login

from . import consumers


router = routers.SimpleRouter()
router.register(r'members', views.MembersViewSet)
router.register(r'teams', views.TeamsViewSet)
##router.register(r'update_ranking', views.update_ranking, "update_ranking")




urlpatterns = [
    path('', views.member_ranking, name='member_ranking'),
    path('member/<int:member_id>/', views.member_detail, name="member_detail"),
    path("teams/", views.teams_ranking, name='teams_ranking'),
    path('invite/', views.invite_redirect, name='discord_invite'),
    path("api/update_ranking", views.update_ranking, name="update_ranking"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

"""
    path('api/members', views.MembersViewSet),
    path('api/teams', views.TeamsViewSet),
    """