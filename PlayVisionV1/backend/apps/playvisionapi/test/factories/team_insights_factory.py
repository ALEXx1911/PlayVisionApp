import pytest
import factory
from factory.django import DjangoModelFactory
from apps.playvisionapi.models import TeamInsights
from .team_factory import TeamFactory
from .season_factory import SeasonFactory

class TeamInsightsFactory(DjangoModelFactory):
    class Meta:
        model = TeamInsights
    
    insight_type = factory.Faker('word')
    title = factory.Faker('sentence')
    category = factory.Faker('word')
    description = factory.Faker('paragraph')

    created_at = factory.Faker('date_time_this_decade')
    updated_at = factory.Faker('date_time_this_decade')

    team = factory.SubFactory(TeamFactory)
    season = factory.SubFactory(SeasonFactory)

@pytest.fixture
def team_insights_factory(db):
    return TeamInsightsFactory