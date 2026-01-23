import pytest
import factory
from apps.playvisionapi.models import Competition , Country
from factory.django import DjangoModelFactory

class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    country_name = factory.Faker('country')
    flag_url = factory.Faker('image_url')

class CompetitionFactory(DjangoModelFactory):
    class Meta:
        model = Competition

    slug = factory.Faker('slug')
    title = factory.Faker('company')
    competition_type = 'league'
    logo_url = factory.Faker('image_url')
    country = factory.SubFactory(CountryFactory)

@pytest.fixture
def competition_factory(db):
    return CompetitionFactory
