# -*- coding: utf-8 -*-

import datetime
import itertools
import random

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _

from data_management.models import Location


class Category(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Company(models.Model):
    title = models.CharField(max_length=250)
    sector = models.CharField(max_length=250)
    sector_entity = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True, related_name='companies')

    def __str__(self):
        return "%s -- %s" % (self.title, self.sector)


class Contact(models.Model):
    full_name = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    company_entity = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True, related_name='contacts')

    def __str__(self):
        return "%s (%s)" % (self.full_name, self.company)


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
    # internal
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default='validating', verbose_name=_("État"))
    expires_in = models.CharField(max_length=2, choices=EXPIRES_IN, default='1w', verbose_name=_("Durée de validité"))

    # public visbility
    date_publish = models.DateTimeField(default=timezone.now, verbose_name=_("Date de publication"))
    title = models.CharField(verbose_name=_("Titre du lead"), max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Auteur"), related_name='leads')
    description_short = models.TextField(verbose_name=_("Résumé du besoin"))
    maturity_level = models.CharField(verbose_name=_("Niveau de maturité"), max_length=10, choices=MATURITY_LEVELS, default='inform')
    date_expired = models.DateTimeField()

    # paywall
    description_full = models.TextField(verbose_name=_("Description complète"))
    # TODO substitute by tagit django model
    category = models.CharField(verbose_name=_("Les rubriques"), max_length=220)
    category_entity = models.ForeignKey(verbose_name=_("Rubriques liées"), to=Category, related_name="leads", on_delete=models.SET_NULL, blank=True,
                                        null=True)

    # TODO denormalize entries
    # contact = models.ForeignKey(Contact, related_name="leads", null=True)
    # location = models.ForeignKey(Location, related_name="leads", null=True)

    # TODO longueur maximale adresse postale francaise
    location = models.CharField(verbose_name=_("Lieu"), max_length=160)
    location_entity = models.ForeignKey(verbose_name=_("Lieux liés"), to=Location, on_delete=models.SET_NULL, blank=True, null=True, related_name="leads")

    contact_name = models.CharField(verbose_name=_("Nom du contact"), max_length=120)
    # TODO add a french phone number validator
    # TODO add an auto formatter
    # TODO add a phone classifier : mobile, etc.
    contact_phone_number = models.CharField(verbose_name=_("Son téléphone"), max_length=120)
    contact_email = models.EmailField(verbose_name=_("Son email"))

    # TODO add an auto-completion based on dynamic thesaurus, specific
    # E/s index
    contact_company = models.CharField(verbose_name=_("La société"), max_length=120)

    contact_company_entity = models.ForeignKey(verbose_name=_("Société liée"), to=Company, on_delete=models.SET_NULL, blank=True, null=True, related_name="leads")

    class Meta:
        ordering = ('-date_publish',)

    def get_absolute_url(self):
        return reverse('hitarget:lead_detail',
                       args=[self.slug])

    def get_absolute_url_full(self):
        return reverse('hitarget:lead_detail_full',
                       args=[self.slug])

    def get_absolute_url_edit(self):
        return reverse('hitarget:lead_edit',
                       args=[self.slug])

    def get_absolute_url_delete(self):
        return reverse('hitarget:lead_delete',
                       args=[self.slug])

    def update_expiration_date(self):
        self.date_expired = self.date_publish + datetime.timedelta(days=self.EXPIRES_IN_DAYS[self.expires_in])

    def generate_unique_slug(self):
        max_length = Lead._meta.get_field('slug').max_length

        self.slug = orig = slugify(self.title)[:max_length]
        for x in itertools.count(1):
            if not Lead.objects.filter(slug=self.slug).exists():
                break

            # Truncate the original slug dynamically. Minus 1 for the hyphen.
            self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

    def main_title(self):
        return self.title.capitalize()

    def author_avatar(self):
        # return "/static/hitarget/assets/avatar_128.jpg"
        if self.author.profile.avatar:
            return self.author.profile.avatar.url
        else:
            return "/static/hitarget/assets/blank_avatar.png"

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
        """.format(author=self.author.username.capitalize(), domain=self.category, location=self.location)
        return sample_text

    def description_short_text(self):
        return self.description_short

    def relative_date(self):
        return "le %s" % (self.date_publish.strftime("%Y-%m-%d"))

    # different actions for different state of the card
    def generate_action_buttons_mini(self, request):
        if request.user == self.author:
            return [
                # {"icon": "glyphicon-remove", "url": "XXX", "additional_class": "", "text": ""},
                {"icon": "", "url": self.get_absolute_url() + "full", "additional_class": "btn-info", "text": u"Voir mon lead"}
            ]
        else:
            return [
                # {"icon": "glyphicon-remove", "url": "XXX", "additional_class": "", "text": ""},
                {"icon": "", "url": self.get_absolute_url(), "additional_class": "btn-info", "text": "Voir plus"}
            ]

    def generate_action_buttons_maxi(self, request):
        print("Getting actions for user %s" % (request.user))
        if request.user == self.author:
            return [
                # {"icon": "glyphicon-remove", "url": "XXX", "additional_class": "", "text": ""},
                {"icon": "", "url": self.get_absolute_url_delete(), "additional_class": "btn-danger", "text": u"Supprimer"},
                {"icon": "", "url": self.get_absolute_url_edit(), "additional_class": "btn-info", "text": u"Éditer"}
            ]
        else:
            return [
                # {"icon": "glyphicon-remove", "url": "XXX", "additional_class": "", "text": ""},
                {"icon": "", "url": self.get_absolute_url_full(), "additional_class": "btn-info", "text": u"Acquérir"}
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
