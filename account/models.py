from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d',
                               blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
