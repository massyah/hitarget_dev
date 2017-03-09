from unittest import TestCase

from hitarget.hitarget_faker import fake_lead_add_form_data


class TestFake_lead_add_form_data(TestCase):
    def test_fake_lead_add_form_data(self):
        fake_doc = fake_lead_add_form_data()
        print(fake_doc)
