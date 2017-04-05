from django.db import models


# Create your models here.

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    departement_code = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    nom_simple = models.CharField(max_length=100)
    nom_reel = models.CharField(max_length=100)
    nom_soundex = models.CharField(max_length=100)
    nom_metaphone = models.CharField(max_length=100)
    code_postaux = models.CharField(max_length=120)
    numero_commune = models.IntegerField()
    code_insee = models.CharField(max_length=5)
    arrondissement = models.IntegerField()
    canton = models.FloatField()
    unk = models.FloatField()
    population_en_2010 = models.IntegerField()
    population_en_1999 = models.IntegerField()
    population_en_2012 = models.IntegerField()
    densite_en_2010 = models.IntegerField()
    surface = models.FloatField(max_length=100)
    long_deg = models.FloatField(max_length=100)
    lat_deg = models.FloatField(max_length=100)
    long_grd = models.FloatField(max_length=100)
    lat_grd = models.FloatField(max_length=100)
    long_dms = models.FloatField(max_length=100)
    lat_dms = models.FloatField(max_length=100)
    altitude_min = models.FloatField(max_length=100)
    altitude_max = models.FloatField(max_length=100)

    departement_id = models.CharField(max_length=100)
    departement_nom = models.CharField(max_length=100)
    departement_nom_maj = models.CharField(max_length=100)
    departement_slug = models.CharField(max_length=100)
    departement_soundex = models.CharField(max_length=100)

    def __str__(self):
        return "%s (%s)" % (self.slug, self.nom)
