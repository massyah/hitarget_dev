from data_management.models import Location
from django.contrib.postgres.search import TrigramSimilarity


def search_location_by_name(name):
    return Location.objects.filter(nom__search=name)[0]


def cities_in_department(departement_name):
    return Location.objects.filter(departement_nom__search=departement_name)
