import pytest
import factory
from apps.playvisionapi.models import Match
from factory.django import DjangoModelFactory
from .team_factory import TeamFactory
from .competition_factory import CompetitionFactory
from .season_factory import SeasonFactory

class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    match_date = factory.Faker('date_time')
    home_goals = factory.Faker('random_int', min=0, max=10)
    away_goals = factory.Faker('random_int', min=0, max=10)
    stadium = factory.Faker('city')
    start_time = factory.Faker('time')
    status = factory.Faker('random_element', elements=['scheduled', 'in_progress', 'finished'])
    round = factory.Faker('random_int', min=1, max=38)
    description = factory.Faker('sentence')

    home_team = factory.SubFactory(TeamFactory)
    away_team = factory.SubFactory(TeamFactory)
    competition = factory.SubFactory(CompetitionFactory)
    season = factory.SubFactory(SeasonFactory) 

@pytest.fixture
def match_factory(db):
    return MatchFactory