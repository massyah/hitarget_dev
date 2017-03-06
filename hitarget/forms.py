import itertools
import re

from django import forms
from django.utils.text import slugify

from .models import Lead
from django.utils.translation import ugettext as _


class AddLeadForm(forms.ModelForm):
    # title = forms.CharField()
    # location = forms.CharField()
    # description_short = forms.CharField()
    # categories = forms.CharField()
    # contact_name = forms.CharField()
    # contact_phone = forms.CharField()
    # contact_email = forms.EmailField()
    # description_full = forms.CharField()
    title = forms.CharField(max_length=180,
                            min_length=8, strip=True,
                            # initial=_("Infrastructure d'impression laser"),
                            widget=forms.TextInput(attrs={'placeholder': _("Infrastructure d'impression laser")}),
                            help_text="Donnez un titre court, incisif et direct. 140 caractères semble être une bonne pratique",
                            label=_("Un titre"),
                            error_messages={
                                "required": _("Il faut donner un titre!"),
                                "min_length": _("Un peu plus d'informations dans le titre")
                            })

    location = forms.CharField(max_length=120,
                               min_length=2, strip=True,
                               # initial=_("Infrastructure d'impression laser"),
                               widget=forms.TextInput(attrs={'placeholder': _("Martillac")}),
                               help_text="Un code postal, une région, une grande ville ou un petit village: on arrivera toujours à le localiser",
                               label=_("Un lieu"),
                               error_messages={
                                   "required": _("Il nous faut un lieu!"),
                                   "min_length": _("Plus d'informations sur le lieu ?")
                               })
    description_short = forms.CharField(max_length=720,
                                        min_length=30, strip=True,
                                        # initial=_("Infrastructure d'impression laser"),
                                        widget=forms.Textarea(attrs={'placeholder': _(
                                            "Un très bon client dans le secteur agro-alimentaire cherche à moderniser ses 250 centres d'impressions.")}),
                                        help_text="",
                                        label=_("Un résumé du besoin"),
                                        error_messages={
                                            "min_length": _("Au moins une trentaine de caractères pour la description?"),
                                            "required": _("Décrivez-nous le besoin pour que tout le monde puisse le trouver.")
                                        })

    category = forms.CharField(max_length=120,
                               min_length=3, strip=True,
                               # initial=_("Infrastructure d'impression laser"),
                               widget=forms.TextInput(
                                   attrs={'placeholder': _("Informatique; Agro-alimentaire; Boulangerie")}),
                               help_text="",
                               label=_("Des rubriques"),
                               error_messages={
                                   "required": _("Décrivez-vous nous dans quel grand secteur trier votre opportunité"),
                                   "min_length": _("Descriptif des rubriques trop courte")
                               })

    contact_name = forms.CharField(max_length=120,
                                   min_length=3, strip=True,
                                   # initial=_("Infrastructure d'impression laser"),
                                   widget=forms.TextInput(
                                       attrs={'placeholder': _("Jean-Pierre Petit")}),
                                   help_text="",
                                   label=_("Comment s'appelle le contact ?"),
                                   error_messages={
                                       "required": _("Décrivez-vous nous le nom de la personne à contacter"),
                                       "min_length": _("Nom trop court, êtes vous-sûr de l'avoir bien renseigné?"),
                                   })

    contact_company = forms.CharField(max_length=120,
                                      min_length=3, strip=True,
                                      # initial=_("Infrastructure d'impression laser"),
                                      widget=forms.TextInput(
                                          attrs={'placeholder': _("Boulangeries Le Petit")}),
                                      help_text="",
                                      label=_("Quel est le nom de la société ?"),
                                      error_messages={
                                          "required": _("Décrivez-vous nous le nom de la société à contacter"),
                                          "min_length": _("Nom trop court, êtes vous-sûr de l'avoir bien renseigné?"),
                                      })

    contact_phone_number = forms.CharField(min_length=6, max_length=20,
                                           strip=True,
                                           # initial=_("Infrastructure d'impression laser"),
                                           widget=forms.TextInput(
                                               attrs={'placeholder': _("06 01 02 03 04")}),
                                           help_text="",
                                           label=_("Son téléphone?"),
                                           error_messages={
                                               "required": _("Indiquez soit un e-mail soit un numéro de téléphone pour le contact"),
                                               "invalid": _("Numéro invalide, êtes vous-sûr de l'avoir bien renseigné?"),
                                           })
    contact_email = forms.EmailField(min_length=6,
                                     strip=True,
                                     # initial=_("Infrastructure d'impression laser"),
                                     widget=forms.TextInput(
                                         attrs={'placeholder': _("jean.pierre.petit@gmail.com")}),
                                     help_text="",
                                     label=_("Son email?"),
                                     error_messages={
                                         "required": _("Indiquez soit un e-mail soit un numéro de téléphone pour le contact"),
                                         "min_length": _("L'email est trop court!"),
                                         "invalid": _("Email invalide, êtes vous-sûr de l'avoir bien renseigné?"),
                                     })


    description_full = forms.CharField(max_length=720,
                                       min_length=30, strip=True,
                                       # initial=_("Infrastructure d'impression laser"),
                                       widget=forms.Textarea(attrs={'placeholder': _(
                                           "M. Petit m'a indiqué rechercher une société pour l'accompagner dans le renouvellement de son parc d'impression, il semble être préssé !")}),
                                       help_text="",
                                       label=_("Un descriptif complet du besoin"),
                                       error_messages={
                                           "min_length": _("Au moins une trentaine de caractères pour la description?"),
                                           "required": _("Décrivez-nous totalement le besoin pour que vos collègues soient le plus informés possible.")
                                       })

    class Meta:
        fields = ['title', 'location', 'description_short', 'category','contact_name','contact_company','contact_phone_number','contact_email','description_full']
        exclude = ['date_expired', 'slug',
                   'category_entity',
                   'location_entity',
                   'contact_company_entity'
                   ]

        model = Lead

    # we customize the save method to automatically populate some fields
    def save(self, commit=True):
        print("in save")
        instance = super(AddLeadForm, self).save(commit=False)

        max_length = Lead._meta.get_field('slug').max_length
        instance.slug = orig = slugify(instance.title)[:max_length]

        for x in itertools.count(1):
            if not Lead.objects.filter(slug=instance.slug).exists():
                break

            # Truncate the original slug dynamically. Minus 1 for the hyphen.
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        # assign author to current logged in user
        instance.author_id=1
        # compute expiration date
        instance.update_expiration_date()
        instance.save()

        return instance
