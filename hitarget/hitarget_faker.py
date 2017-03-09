import codecs
import random

from faker import Factory

fake = Factory.create('fr_FR')

with codecs.open("data/thesaurus/amazon.txt", encoding="utf-8") as f:
    FAKE_CATEGORIES = list(filter(lambda x: not x.startswith("#"), map(lambda x: x.strip(), f.readlines())))

with codecs.open("data/thesaurus/mano_mano.txt", encoding="utf-8") as f:
    FAKE_TITLE = list(filter(lambda x: not x.startswith("#"), map(lambda x: x.strip(), f.readlines())))


def fake_lead_add_form_data():
    return {
        "title": fake.catch_phrase(),
        "location": "%s (%s)" % (fake.city_prefix(), str(fake.postcode())),
        "contact_name": fake.name(),
        "contact_company": fake.company(),
        "contact_phone_number": fake.phone_number(),
        "contact_email": fake.company_email(),
        "category": random.choice(FAKE_CATEGORIES),
        "description_short":random.choice(FAKE_TITLE)+" "+fake.text(max_nb_chars=320),
        "description_full": random.choice(FAKE_TITLE)+" "+fake.text(max_nb_chars=320)
    }
