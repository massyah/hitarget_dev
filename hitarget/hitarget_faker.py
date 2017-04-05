import codecs
import random

from faker import Factory

fake = Factory.create('fr_FR')

with codecs.open("data/thesaurus/amazon.txt", encoding="utf-8") as f:
    FAKE_CATEGORIES = list(filter(lambda x: not x.startswith("#"), map(lambda x: x.strip(), f.readlines())))

with codecs.open("data/thesaurus/mano_mano.txt", encoding="utf-8") as f:
    FAKE_TITLE = list(filter(lambda x: not x.startswith("#"), map(lambda x: x.strip(), f.readlines())))


def fake_user_data():
    base_doc = {
        'username': fake.name(),
        'first_name': fake.name(),
        'email': fake.company_email()

    }
    return base_doc


def fake_lead_add_form_data():
    base_doc = {
        "title": fake.catch_phrase(),
        "location": "%s (%s)" % (fake.city_prefix(), str(fake.postcode())),
        "contact_name": fake.name(),
        "contact_company": fake.company(),
        "contact_phone_number": fake.phone_number(),
        "contact_email": fake.company_email(),
        "category": random.choice(FAKE_CATEGORIES),
        "description_short": random.choice(FAKE_TITLE) + " " + fake.text(max_nb_chars=320),
        "description_full": random.choice(FAKE_TITLE) + " " + fake.text(max_nb_chars=320)
    }
    base_doc['title'] = "Maintenance d'espaces verts"
    base_doc['category'] = "Entretien, jardinerie"
    base_doc['description_short'] = """
    Pour des contrats d'entretien d'espaces verts d'un lotissement en cours de construction.
    """.strip()
    base_doc['description_full'] = """
    123 Immo recherche pour son dernier lotissement un sous-traitant qui prendrait en charge l'entretien de 50 000 m2 d'espace vert, contrat de 3 ans renouvelable. Le décideur à une apétence pour les prix bas, mais ne néglige pas l'importance de la dimension écologique de la maintenance.
    """.strip()

    return base_doc
