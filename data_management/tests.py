from django.test import TestCase
import pprint as pp
from data_management.backend.inject_fake_ads import generate_combined_fake_data
from data_management.backend.inject_locations import inject_cities
from data_management.indexation import generate_lead_inverse_index
from data_management.models import Location

from hitarget.models import Lead
# Create your tests here.
from data_management.queries import search_location_by_name, cities_in_department


class LocationTestCase(TestCase):
    def setUp(self):
        inject_cities(n=500)

    def test_fetch_location_by_id(self):
        plagne_city = Location.objects.get(id__exact=3)
        self.assertEqual(plagne_city.nom, "PLAGNE")

    def test_fetch_by_name(self):
        plagne_city = search_location_by_name("plagne")
        self.assertEqual(plagne_city.nom, "PLAGNE")

    def test_fetch_by_department_name(self):
        city_ain = cities_in_department("ain")
        print(city_ain)


class FullTextSearchTestCase(TestCase):
    def setUp(self):
        leads = [generate_combined_fake_data() for i in range(2)]
        for l in leads:
            l['sample_user'].save()
            l['sample_lead'].author_id = l['sample_user'].id
            l['sample_lead'].update_expiration_date()
            l['sample_lead'].generate_unique_slug()
            l['sample_lead'].save()
            # Lead.objects.bulk_create(leads)

    def test_generate(self):
        pp.pprint(Lead.objects.all())


class IndexationTest(TestCase):
    def setUp(self):
        leads = [generate_combined_fake_data() for i in range(2)]
        for l in leads:
            l['sample_user'].save()
            l['sample_lead'].author_id = l['sample_user'].id
            l['sample_lead'].update_expiration_date()
            l['sample_lead'].generate_unique_slug()
            l['sample_lead'].save()
            # Lead.objects.bulk_create(leads)

    def test_index_is_not_empty(self):
        idx = generate_lead_inverse_index()
        pp.pprint(idx)