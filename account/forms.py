from django import forms
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Votre nom d'utilisateur"), )
    password = forms.CharField(widget=forms.PasswordInput, label=_("Votre mot de passe"), )

    class Meta:
        fields = ("username", "password")


from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Votre mot de passe'),
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Répétez votre mot de passe'),
                                widget=forms.PasswordInput)
    username = forms.CharField(label=_("Un nom d'utilisateur"))
    first_name = forms.CharField(label=_("Un prénom"))
    email = forms.CharField(label=_("Une adresse mail"))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


# user profile edit

from .models import Profile


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label=_("Un prénom"), required=False)
    last_name = forms.CharField(label=_("Un nom de famille"), required=False)
    email = forms.CharField(label=_("Une adresse mail"), help_text=_("Parce qu'il bien vous joindre"))
    username = forms.CharField(label=_("Un nom d'utilisateur"))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        readonly_fields = ('username',)


class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(label=_("Une numéro de téléphone"), required=False,

                            help_text=_("On ne le partage avec personne, promis!"))
    avatar = forms.FileField(label=_("Votre photo de profil"),required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'avatar')
