import pytest
import factory
from apps.playvisionapi.models import Player
from factory.django import DjangoModelFactory
from .team_factory import TeamFactory

class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    slug = factory.Faker('slug')
    common_name = factory.Faker('name')
    pname = factory.Faker('name')
    lastname = factory.Faker('last_name')
    age = factory.Faker('random_int', min=16, max=40)
    height = factory.Faker('random_int', min=160, max=200)
    nationality = factory.Faker('country')
    nationality_flag = factory.Faker('image_url')
    position = factory.Faker('random_element', elements=['Goalkeeper', 'Defender', 'Midfielder', 'Forward'])
    foot = factory.Faker('random_element', elements=['left', 'right'])
    team_dorsal = factory.Faker('random_int', min=1, max=99)

    team = factory.SubFactory(TeamFactory)

@pytest.fixture
def player_factory(db):
    return PlayerFactory