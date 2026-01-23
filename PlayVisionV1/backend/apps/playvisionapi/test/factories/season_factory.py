import pytest
import factory
from apps.playvisionapi.models import Season
from factory.django import DjangoModelFactory

class SeasonFactory(DjangoModelFactory):
    class Meta:
        model = Season

    year_start = factory.Faker('year')
    year_end = factory.LazyAttribute(lambda obj: str(int(obj.year_start) + 1))

@pytest.fixture
def season_factory(db):
    return SeasonFactory