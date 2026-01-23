import pytest
import factory
from apps.playvisionapi.models import PlayerSeasonStats
from factory.django import DjangoModelFactory
from .player_factory import PlayerFactory
from .team_factory import TeamFactory
from .season_factory import SeasonFactory

class PlayerSeasonStatsFactory(DjangoModelFactory):
    class Meta:
        model = PlayerSeasonStats

    matches_played = factory.Faker('random_int', min=0, max=38)
    minutes_played = factory.Faker('random_int', min=0, max=3420)
    goals = factory.Faker('random_int', min=0, max=50)
    head_goals = factory.Faker('random_int', min=0, max=20)
    penalty_goals = factory.Faker('random_int', min=0, max=15)
    freekick_goals = factory.Faker('random_int', min=0, max=10)
    assists = factory.Faker('random_int', min=0, max=30)
    yellow_cards = factory.Faker('random_int', min=0, max=10)
    red_cards = factory.Faker('random_int', min=0, max=5)
    tackles = factory.Faker('random_int', min=0, max=200)
    cleansheets = factory.Faker('random_int', min=0, max=20)
    correct_passes_media = factory.Faker('random_int', min=0, max=100)
    recoveries_media = factory.Faker('random_int', min=0, max=100)
    media = factory.Faker('random_int', min=0, max=10)

    player = factory.SubFactory(PlayerFactory)
    team = factory.SubFactory(TeamFactory)
    season = factory.SubFactory(SeasonFactory)

@pytest.fixture
def player_season_stats_factory(db):
    return PlayerSeasonStatsFactory