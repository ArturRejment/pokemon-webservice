from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
	""" Inherite from UserCreationForm in order to add
	new field "email", because UserCreationFrom does not
	support this field. """
	email = forms.EmailField(label = "Email")

	class Meta:
		model = User
		fields = ("username", "email",)

	def save(self, commit=True):
		""" Override save function to save also email """
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user