import pytest
from faker import Faker
from apps.playvisionapi.models import Team , Season , Competition , Country
from factory.django import DjangoModelFactory

@pytest.fixture
def team_factory(db):
    def create_team(**kwargs):
        defaults = {
            'title': 'Default Team',
            'slug': 'default-team',
            'logo_url': 'http://example.com/logo.png',
        }
        defaults.update(kwargs)
        return Team.objects.create(**defaults)
    return create_team

@pytest.fixture
def season_factory(db):
    def create_season(**kwargs):
        defaults = {
            'year_start': '2024',
            'year_end': '2025',
        }
        defaults.update(kwargs)
        return Season.objects.create(**defaults)
    return create_season

@pytest.fixture
def competition_factory(db):
    class CompetitionFactory(DjangoModelFactory):
        class Meta:
            model = Competition

        title = Faker().company()
        slug = Faker().slug()
        competition_type = 'league'
        country = Country.objects.first() or Country.objects.create(country_name='Spain')
    return CompetitionFactory