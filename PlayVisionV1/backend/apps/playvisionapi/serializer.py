from rest_framework import serializers
from .models import PlayerSeasonStats , Player, Team, TeamInsights , TeamCompetitionStats , Match, MatchEvent, Competition , Country , PlayerCompetitionStats

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("title","stadium","logo_url","shortname","coach")

class TeamCompetitionStatSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False,read_only=True)
    class Meta:
        model = TeamCompetitionStats
        fields = ("team","matches_played","win","draw","lose","goals_for","goals_against","goal_difference","point")

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    class Meta:
        model = Player
        fields = "__all__"
        extra_field = ["team"]
    
    def get_fields(self):
        fields = super().get_fields()
        for f in getattr(self.Meta,"extra_fields",[]):
            fields[f] = self.fields[f]
        return fields

class PlayerListDataSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.title', read_only=True)
    team_logo_url = serializers.ImageField(source='team.logo_url', read_only=True)
    class Meta:
        model = Player
        fields = ("pname","lastname","nationality_flag","position","team_name","team_logo_url")

class PlayerSeasonStatsSerializer(serializers.ModelSerializer):
    player = PlayerListDataSerializer(read_only=True)
    class Meta:
        model = PlayerSeasonStats
        fields = "__all__"
        extra_field = ["player"]
    
    def get_fields(self):
        fields = super().get_fields()
        for f in getattr(self.Meta,"extra_fields",[]):
            fields[f] = self.fields[f]
        return fields

class PlayerCompetitionStatsSerializer(serializers.ModelSerializer):
    player = PlayerListDataSerializer(read_only=True)
    class Meta:
        model = PlayerCompetitionStats
        fields = "__all__"
        extra_field = ["player"]
    
    def get_fields(self):
        fields = super().get_fields()
        for f in getattr(self.Meta,"extra_fields",[]):
            fields[f] = self.fields[f]
        return fields


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ("id", "title", "country", "competition_type","logo_url")

class CompetitionMatchesListSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    class Meta:
        model = Match
        fields = ("id","match_date","home_goals","away_goals","stadium","description","status","home_team","away_team")

class CompetitionsMatchesSerializer(serializers.ModelSerializer):
    competition_matches = CompetitionMatchesListSerializer(many=True,read_only=True)
    class Meta:
        model = Competition
        fields = ("id", "title", "country","logo_url","competition_matches")

class CompetitonTeamStatSerializer(serializers.ModelSerializer):
    team_competition_stats = TeamCompetitionStatSerializer(many=True,read_only=True)
    class Meta:
        model = Competition
        fields = ("id", "title", "country", "competition_type","logo_url","team_competition_stats")


class CountryCompetitionSerializer(serializers.ModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True, source='competition_country')
    class Meta:
        model = Country
        fields = ("id", "country_name", "flag_url","competitions")

class CompetitionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ("title","logo_url")

class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    competition = CompetitionListSerializer(read_only=True)
    class Meta:
        model = Match
        fields = ("match_date","home_goals","away_goals","stadium","start_time","status","description","home_team","away_team","competition")

class MatchEventSerializer(serializers.ModelSerializer):
    player_name = PlayerListDataSerializer(read_only=True, source='player')
    assist_player = PlayerListDataSerializer(read_only=True, source='player_assist')
    out_player = PlayerListDataSerializer(read_only=True, source='player_out')
    class Meta:
        model = MatchEvent
        fields = ("event_type","minute","description","player_name","assist_player","out_player")

class PlayerLineupSerializer(serializers.ModelSerializer):
    pname= serializers.CharField(source='player.common_name', read_only=True)
    dorsal = serializers.IntegerField(source='player.team_dorsal', read_only=True)
    position = serializers.CharField(source='player.position', read_only=True)
    team_name = serializers.CharField(source='team.title', read_only=True)
    team_logo_url = serializers.CharField(source='team.logo_url', read_only=True)
    class Meta:
        model = PlayerSeasonStats
        fields = ("pname","position","dorsal","media","team_name","team_logo_url")

class TeamInsightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInsights
        fields = ("insight_type","title","description","category")
