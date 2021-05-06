from django.contrib import admin
from . import views
from .models import Member, Teams, Match, Badge
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import time

def rollback(modeladmin, request, queryset):
    for i in queryset:
        i.rollback()

class WinnerInline(admin.TabularInline):
    model = Match
    fk_name = 'winner'
    extra = 0

class LoserInline(admin.TabularInline):
    model = Match
    fk_name = 'loser'
    extra = 0

class MemberAdmin(admin.ModelAdmin):
    actions = [rollback]
    inlines = [LoserInline, WinnerInline]
    fieldsets = [
        (None, { "fields": ['last_known_name', 'user_id','tournaments', 'did_tournament','is_winning' , 'points', 'team']}),
        ('Badges', {'fields': ['member_badges']}),
        ('Infos précédentes', {"fields": ["previous_points_float", "previous_sigma"]})
    ]
    filter_horizontal = ['member_badges']
    search_fields = ['last_known_name']


class TeamMemberInline(admin.StackedInline):
    model = Member
    extra = 0
    fieldsets = [
        (None, { "fields": ['last_known_name', 'user_id', 'points', 'team']})
    ]

class TeamAdmin(admin.ModelAdmin):
    actions = [rollback]
    inlines = [TeamMemberInline]

admin.site.register(Match)
admin.site.register(Member, MemberAdmin)
admin.site.register(Teams, TeamAdmin)
admin.site.register(Badge)
