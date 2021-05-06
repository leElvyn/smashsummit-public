import asyncio
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required,  permission_required,  user_passes_test
from django.utils import timezone
from django.core import serializers

from .models import Member, Teams, Match
from .serializers import MemberSerializer, TeamsSerializer, RankingUpdateSerializer

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from trueskill import Rating, rate_1vs1

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




class MembersViewSet(viewsets.ModelViewSet): 
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]


class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = [IsAdminUser]


@api_view(["GET"])
@permission_classes([IsAdminUser])
def update_ranking(request):
    headers = request.GET
    body = request.data
    try:
        winner_id = headers["winner_id"]
        loser_id = headers["loser_id"]
        match_type = body["match_type"]
        winner = Member.objects.get(user_id=winner_id)
        loser = Member.objects.get(user_id=loser_id)
    except KeyError:
        return HttpResponse(status=400)
    if match_type == 1:
        ranking_generic_checks()
    elif match_type == 2:
        if winner.did_tournament == False: 
            winner.tournaments += 1
            winner.did_tournaments = True
        if loser.did_tournament == False:
            loser.tournaments += 1
            loser.did_tournaments = True

    return_dict = update(winner, loser, body)
    teams = Teams.objects.order_by("-team_points")[:999]
    data = serializers.serialize("json", teams)
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('bot_room', {
        'type': 'bot_room',
        'message': data
    })
    
    return Response(return_dict)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def end_tournament(request):
    objects = Member.objects.all()
    for i in objects:
        i.did_tournaments = False
        i.save()


def ranking_generic_checks():
    '''check for things like who's the fist of the ranking. 
    can only be executed at the end of a tournament or for freeplay'''
    pass

def member_ranking(request):
    print("request")
    ranking_list = Member.objects.exclude(team__isnull=True).order_by("-points")[:999]
    context = {"memberList": ranking_list, "memberLen": len(ranking_list)}
    return render(request, "ranking/member_ranking.html", context)


def teams_ranking(request):
    ranking_list = Teams.objects.order_by("-team_points")[:999]
    context = {"teamsList": ranking_list, "teamsLen": len(ranking_list)}
    return render(request, "ranking/teams_ranking.html", context)

@login_required
def member_detail(request, member_id):
    member = get_object_or_404(Member, user_id=member_id)
    return render(request, 'ranking/member_page.html', {"member": member})

@login_required
def invite_redirect(request):
    return redirect("https://discord.gg/ptmX4Nsp29")


#Utilities ------------------

def update(winner, loser, body):
    winner.write_previous()
    loser.write_previous()
    winner.is_winning, loser.is_winning = True, False
    winner_rate = Rating(winner.points_float, winner.sigma)
    loser_rate = Rating(loser.points_float, loser.sigma)
    winner_rate, loser_rate = rate_1vs1(winner_rate, loser_rate)
    winner.write_round(winner_rate)
    loser.write_round(loser_rate)
    winner_team = Teams.objects.get(id=winner.team.id)
    loser_team = Teams.objects.get(id=loser.team.id)
    winner_team.write_previous()
    loser_team.write_previous()
    winner_team_rate = Rating(winner_team.points_float, winner_team.sigma)
    loser_team_rate = Rating(loser_team.points_float, loser_team.sigma)
    winner_team_rate, loser_team_rate = rate_1vs1(winner_team_rate, loser_team_rate)
    winner_team.write_round(winner_team_rate)
    loser_team.write_round(loser_team_rate)
    match_object = Match(winner=winner, loser=loser, winner_score=1, loser_score=0, match_type=body["match_type"])
    match_object.save()
    return {
        "teams": {
            "winner_name": winner_team.name,
            "loser_name": loser_team.name,
            "winner_points": int(winner_team_rate.mu),
            "loser_points": int(loser_team_rate.mu),
        },
        "members": {
            "winner_name": winner.last_known_name,
            "loser_name": loser.last_known_name,
            "winner_points": int(winner_rate.mu),
            "loser_points": int(loser_rate.mu),
        },
    }


def update_status(member):
    """update if a user is winning or loosing"""
    last_matchs = Match.objects.filter(Q(winner=a) | Q(loser=a)).filter(date__gt=timezone.now())

