from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(label="Votre nom")
    email = forms.EmailField(label="Votre mail")
    message = forms.CharField(label="Votre message", widget=forms.Textarea())


class CommentForm(forms.Form):
    name = forms.CharField(label="Votre nom")
    email = forms.EmailField(label="Votre mail")
    body = forms.CharField(label="Votre commentaire", widget=forms.Textarea())


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class InscriptionForm(forms.ModelForm):
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password2(self):
        form = self.cleaned_data
        if form["password"] != form["password2"]:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return form["password2"]