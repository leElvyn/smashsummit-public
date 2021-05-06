from .models import Member, Teams
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source='team.id', read_only=True)
    team_role = serializers.IntegerField(source='team.role', read_only=True)
    class Meta:
        model = Member
        fields = ('last_known_name', 'points', 'user_id', "PP_link", "team" , "team_id", "team_role")

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ("name", "short_name", "team_points", "id", "role")

class RankingUpdateSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   winnerId = serializers.IntegerField()
   looserId = serializers.IntegerField()