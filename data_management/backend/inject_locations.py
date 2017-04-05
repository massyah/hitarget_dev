import os
import pandas as pd

import django

from helpers.iterators import grouper

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hitargetMVP.settings")
django.setup()

from data_management.models import Location
from helpers import path

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

pd.set_option("display.width", 0)

location_file = os.path.join(path.data_dir, "locations", "villes_france.csv")
department_file = os.path.join(path.data_dir, "locations", "departements.csv")

villes_colnames = [
    "id",
    "departement_code",
    "slug",
    "nom",
    "nom_simple",
    "nom_reel",
    "nom_soundex",
    "nom_metaphone",
    "code_postaux",
    "numero_commune",
    "code_insee",
    "arrondissement",
    "canton",
    "unk",
    "population_en_2010",
    "population_en_1999",
    "population_en_2012",
    "densite_en_2010",
    "surface",
    "long_deg",
    "lat_deg",
    "long_grd",
    "lat_grd",
    "long_dms",
    "lat_dms",
    "altitude_min",
    "altitude_max",
]

departement_colnames = [
    "departement_id",
    "departement_code",
    "departement_nom",
    "departement_nom_maj",
    "departement_slug",
    "departement_soundex"
]


def preprocess(row):
    pass


def inject_cities(n=1000):
    locations_df = pd.DataFrame.from_csv(location_file, header=None, index_col=None)
    locations_df.columns = villes_colnames
    locations_df['departement_code'] = locations_df['departement_code'].map(lambda i: str(i).zfill(2).lower())
    departement_df = pd.DataFrame.from_csv(department_file, header=None, index_col=None)
    departement_df.columns = departement_colnames
    # departement_df['departement_code'] = departement_df['departement_code']
    # locations_df['departement_code'] = locations_df['departement_code']
    locations_df_j = locations_df.merge(departement_df, on="departement_code")
    locations_df_j.head(2)
    locations_df_j[locations_df_j['nom'].str.contains("BORDEAUX")]

    # which one are missing
    missing_cities = set(locations_df['slug']).difference(locations_df_j['slug'])
    locations_df.query("slug in @missing_cities")
    # join by departement_code

    print(locations_df.dtypes)
    print(locations_df.head(5))
    # print(departement_df.dtypes)

    # print(locations_df.sort_values("population_en_2012", ascending=False).head(50))
    # print(locations_df.sort_values("canton", ascending=False).head(50))


    # split multiple arrondissement

    # prepare for injection

    # build the django model object



    django_objects = [
        Location(**row) for i, row in locations_df.head(n).iterrows()
        ]
    # print(django_objects)
    total_inserted = 0
    for batch in grouper(n=100, iterable=django_objects):
        Location.objects.bulk_create(batch)
        total_inserted += 100
        print("Inserted %d/%d location objects" % (total_inserted, len(django_objects)))
    print("Inserted %d location objects" % (len(django_objects)))


if __name__ == '__main__':
    inject_cities()
