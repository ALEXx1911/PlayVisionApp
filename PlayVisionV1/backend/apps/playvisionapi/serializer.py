from rest_framework import serializers
from .models import PlayerSeasonStats , Player, Team , Match, Competition , Country

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("title","stadium","logo_url","shortname","coach")

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

class CountryCompetitionSerializer(serializers.ModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True, source='competition_country')
    class Meta:
        model = Country
        fields = ("id", "country_name", "flag_url","competitions")
