import pytest
import factory
from factory.django import DjangoModelFactory
from apps.playvisionapi.models import Team

class TeamFactory(DjangoModelFactory):
    class Meta: 
        model = Team
    
    slug = factory.Faker('slug')
    title = factory.Faker('company')
    logo_url = factory.Faker('image_url')
    shortname = factory.Faker('company_suffix')
    stadium = factory.Faker('company')
    coach = factory.Faker('name')
    preferred_formation = "4-4-2"

@pytest.fixture
def team_factory(db):
    return TeamFactory