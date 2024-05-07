from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class":"form-control"}))


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        labels = {
        "username": "Geopřezdívka"
        }

        help_texts = {
            "username": "<ul><li>Pouze písmena, číslice a znaky @/./+/-/_</li></ul>",
        }


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].help_text = ""
    

    def clean(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Tento email {email} už je zaregistrován.")
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Geopřezdívka', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Heslo", widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class':'form-control'}))

        # vycházím ze zdrojového kódu pro Django na Githubu
    error_messages = {
        "invalid_login": "Zadej správné uživatelské jméno a heslo. Pozor na velká a malá písmena."
     }

    class Meta:
        model = User
        fields = "__all__"
        labels = {
            "username": "Geopřezdívka"
        }


class ResetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class":"form-control"}))