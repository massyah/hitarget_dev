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

from data_management.models import Location
from helpers import path

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

pd.set_option("display.width", 0)


def generate_combined_fake_data():
    sample_user = User(**fake_user_data())
    sample_lead = Lead(**fake_lead_add_form_data())
    sample_lead.author = sample_user
    return {
        "sample_user": sample_user,
        "sample_lead": sample_lead
    }
