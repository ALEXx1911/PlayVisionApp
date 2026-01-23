import pytest
import factory
from apps.playvisionapi.models import PlayerCompetitionStats
from .competition_factory import CompetitionFactory
from factory.django import DjangoModelFactory
from .player_factory import PlayerFactory
from .season_factory import SeasonFactory

class PlayerCompetitionStatsFactory(DjangoModelFactory):
    class Meta:
        model = PlayerCompetitionStats

    matches_played = factory.Faker('random_int', min=0, max=100)
    minutes_played = factory.Faker('random_int', min=0, max=9000)
    goals = factory.Faker('random_int', min=0, max=50)
    head_goals = factory.Faker('random_int', min=0, max=20)
    penalty_goals = factory.Faker('random_int', min=0, max=15)
    freekick_goals = factory.Faker('random_int', min=0, max=10)
    assists = factory.Faker('random_int', min=0, max=30)
    yellow_cards = factory.Faker('random_int', min=0, max=10)
    red_cards = factory.Faker('random_int', min=0, max=5)
    correct_passes_media = factory.Faker('random_int', min=0, max=100)
    tackles = factory.Faker('random_int', min=0, max=200)
    cleansheets = factory.Faker('random_int', min=0, max=30)
    media = factory.Faker('random_int', min=0, max=10)

    player = factory.SubFactory(PlayerFactory)
    competition = factory.SubFactory(CompetitionFactory)
    season = factory.SubFactory(SeasonFactory)

@pytest.fixture
def player_competition_stats_factory(db):
    return PlayerCompetitionStatsFactory