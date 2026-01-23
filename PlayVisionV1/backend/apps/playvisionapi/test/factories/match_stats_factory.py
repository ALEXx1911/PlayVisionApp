import pytest
import factory
from apps.playvisionapi.models import MatchStats
from factory.django import DjangoModelFactory
from .match_factory import MatchFactory

class MatchStatsFactory(DjangoModelFactory):
    class Meta:
        model = MatchStats

    home_shots = factory.Faker('random_int', min=0, max=20)
    home_shots_ontarget = factory.Faker('random_int', min=0, max=15)
    home_corners = factory.Faker('random_int', min=0, max=10)
    home_possession = factory.Faker('random_int', min=30, max=70)
    home_passes = factory.Faker('random_int', min=100, max=800)
    home_fouls = factory.Faker('random_int', min=0, max=30)
    home_yellow_cards = factory.Faker('random_int', min=0, max=5)
    home_red_cards = factory.Faker('random_int', min=0, max=2)
    home_offsides = factory.Faker('random_int', min=0, max=5)

    away_shots = factory.Faker('random_int', min=0, max=20)
    away_shots_ontarget = factory.Faker('random_int', min=0, max=15)
    away_corners = factory.Faker('random_int', min=0, max=10)
    away_possession = factory.Faker('random_int', min=30, max=70)
    away_passes = factory.Faker('random_int', min=100, max=800)
    away_fouls = factory.Faker('random_int', min=0, max=30)
    away_yellow_cards = factory.Faker('random_int', min=0, max=5)
    away_red_cards = factory.Faker('random_int', min=0, max=2)
    away_offsides = factory.Faker('random_int', min=0, max=5)

    match = factory.SubFactory(MatchFactory)  

@pytest.fixture
def match_stats_factory(db):
    return MatchStatsFactory