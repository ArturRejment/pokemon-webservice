from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "username",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": "email",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "re-password",
            }
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
