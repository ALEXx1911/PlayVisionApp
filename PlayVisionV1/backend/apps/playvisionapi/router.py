from rest_framework import routers
from .admin_api.viewsets.team_viewset import TeamViewSet
from .admin_api.viewsets.player_viewset import PlayerViewSet
from .admin_api.viewsets.competition_viewset import CompetitionViewSet
from .admin_api.viewsets.match_viewset import MatchViewSet
from .admin_api.viewsets.season_viewset import SeasonViewSet
from .admin_api.viewsets.country_viewset import CountryViewSet
from .admin_api.viewsets.player_season_stats_viewset import PlayerCompetitionStatsViewSet
from .admin_api.viewsets.match_event_viewset import MatchEventViewSet
from .admin_api.viewsets.match_stats_viewset import MatchStatsViewSet
from .admin_api.viewsets.team_insights_viewset import TeamInsightsViewSet
from .admin_api.viewsets.team_competition_stats_viewset import TeamCompetitionStatsViewSet

router = routers.DefaultRouter()

router.register(r'teams', TeamViewSet, basename='team')
router.register(r'teams-insights', TeamInsightsViewSet, basename='team-insights')
router.register(r'team-competition-stats', TeamCompetitionStatsViewSet, 
                basename='team-competition-stats')
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'player-competition-stats', PlayerCompetitionStatsViewSet, 
                basename='player-competition-stats')
router.register(r'player-season-stats', PlayerCompetitionStatsViewSet,
                basename='player-season-stats')
router.register(r'competitions', CompetitionViewSet, basename='competition')
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'match-events', MatchEventViewSet, basename='match-event')
router.register(r'match-stats', MatchStatsViewSet, basename='match-stats')