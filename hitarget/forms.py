import itertools
from django import forms
from django.utils.text import slugify

from .models import Lead


class AddLeadForm(forms.ModelForm):
    # title = forms.CharField()
    # location = forms.CharField()
    # description_short = forms.CharField()
    # categories = forms.CharField()
    # contact_name = forms.CharField()
    # contact_phone = forms.CharField()
    # contact_email = forms.EmailField()
    # description_full = forms.CharField()

    class Meta:
        # fields = '__all__'
        exclude = ['date_expired', 'slug', ]

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
        # compute expiration date
        instance.update_expiration_date()
        instance.save()

        return instance
