import pytest
import factory
from apps.playvisionapi.models import MatchEvent
from factory.django import DjangoModelFactory
from .match_factory import MatchFactory
from .player_factory import PlayerFactory

class MatchEventFactory(DjangoModelFactory):
    class Meta:
        model = MatchEvent

    event_type = factory.Faker('random_element', elements=['goal', 'yellow_card', 'red_card', 'substitution'])
    minute = factory.Faker('random_int', min=1, max=120)
    description = factory.Faker('sentence', nb_words=6)
    
    match = factory.SubFactory(MatchFactory)
    player = factory.SubFactory(PlayerFactory)


@pytest.fixture
def match_event_factory(db):
    return MatchEventFactory