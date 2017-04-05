import collections
import os
import pandas as pd
from django.db import models
import django
from django.conf import settings
from helpers.iterators import grouper
from hitarget.hitarget_faker import fake_lead_add_form_data, fake_user_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hitargetMVP.settings")
django.setup()

from django.contrib.auth.models import User
from hitarget.models import Lead


def generate_author_inverse_index():
    pass


def generate_lead_inverse_index():
    lead_inverse_index = collections.defaultdict(set)
    for l in Lead.objects.all():
        lead_inverse_index[l.author.username].add(l.slug)
        lead_inverse_index[l.category].add(l.slug)
        lead_inverse_index[l.location].add(l.slug)
        lead_inverse_index[l.maturity_level].add(l.slug)
        # leads recent
        # leads bientôt expirés
    return lead_inverse_index