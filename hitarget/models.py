import datetime
import random

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Company(models.Model):
    title = models.CharField(max_length=250)
    sector = models.ForeignKey(Category, related_name='companies')

    def __str__(self):
        return "%s -- %s" % (self.title, self.sector)


class Contact(models.Model):
    full_name = models.CharField(max_length=250)
    company = models.ForeignKey(Company, related_name='contacts')

    def __str__(self):
        return "%s (%s)" % (self.full_name, self.company)


class Location(models.Model):
    display_name = models.CharField(max_length=250)

    def __str__(self):
        return self.display_name


class Card(models.Model):
    pass


class Lead(Card):
    EXPIRES_IN = (
        ('1d', 'Un jour'),
        ('1w', 'Une semaine'),
        ('2w', 'Deux semaines'),
        ('1m', 'Un mois'),
    )
    EXPIRES_IN_D = dict(EXPIRES_IN)

    EXPIRES_IN_DAYS = {
        '1d': 1,
        '1w': 7,
        '2w': 14,
        '1m': 31
    }
    MATURITY_LEVELS = (
        ('inform', 'Se renseigne'),
        ('eval', 'Évalue des opportunités'),
        ('search', "Cherche à s'équipper"),
    )
    MATURITY_LEVELS_DICT = dict(MATURITY_LEVELS)
    STATUS = (
        ('validating', 'En cours de validation'),
        ('offline', 'Inactif'),
        ('online', 'Actif'),
        ('expired', 'Expiré'),
        ('acquired', 'Déjà acquis'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique=True)
    author = models.ForeignKey(User,
                               related_name='leads')
    description_short = models.TextField()
    description_full = models.TextField()
    date_publish = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    expires_in = models.CharField(max_length=2, choices=EXPIRES_IN, default='1w')
    status = models.CharField(max_length=10, choices=STATUS, default='validating')
    maturity_level = models.CharField(max_length=10, choices=MATURITY_LEVELS, default='inform')
    date_expired = models.DateTimeField()
    category = models.ForeignKey(Category, related_name="leads")
    contact = models.ForeignKey(Contact, related_name="leads", null=True)
    location = models.ForeignKey(Location, related_name="leads", null=True)

    class Meta:
        ordering = ('-date_publish',)

    def get_absolute_url(self):
        return reverse('hitarget:lead_detail',
                       args=[self.slug])

    def update_expiration_date(self):
        self.date_expired = self.date_publish + datetime.timedelta(days=self.EXPIRES_IN_DAYS[self.expires_in])

    def main_title(self):
        return self.title.title()

    def author_avatar(self):
        return "/static/hitarget/assets/avatar_128.jpg"

    def author_avatar_alt(self):
        return "arthur-g-avatar"

    def media_heading(self):
        new_leads_headings = [
            "Tout nouveau!++",
            "ça vient de sortir",
            "Une nouvelle offre !",

        ]
        return random.choice(new_leads_headings).title()

    def expires_in_full(self):
        return self.EXPIRES_IN_D[self.expires_in]

    def introductory_text(self):
        sample_text = """
        {author} vient de poster un nouveau lead dans le domaine {domain}, pour une société basé à {location}. Intéréssé ?
        """.format(author=self.author, domain=self.category, location=self.location)
        return sample_text

    def description_short_text(self):
        return self.description_short

    def relative_date(self):
        return "le %s" % (self.date_publish.strftime("%Y-%m-%d"))

    # different actions for different state of the card
    def action_buttons_mini(self):
        return [
            # {"icon": "glyphicon-remove", "url": "XXX", "additional_class": "", "text": ""},
            {"icon": "", "url": self.get_absolute_url(), "additional_class": "btn-info", "text": "Voir plus"}
        ]

    def action_buttons_maxi(self):
        return [
            # {"icon": "glyphicon-remove", "url": "XXX", "additional_class": "", "text": ""},
            {"icon": "", "url": self.get_absolute_url() + "full", "additional_class": "btn-info", "text": u"Acquérir"}
        ]

    def action_buttons_full(self):
        return [
            # {"icon": "glyphicon-remove", "url": "XXX", "additional_class": "", "text": ""},
            # {"icon": "", "url": self.get_absolute_url()+"/buy", "additional_class": "btn-info", "text": u"Acquérir"}
        ]

    def prospect_maturity(self):
        return self.MATURITY_LEVELS_DICT[self.maturity_level]

    def __str__(self):
        return self.title
