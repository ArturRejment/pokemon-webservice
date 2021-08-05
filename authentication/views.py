from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login

from .forms import RegisterForm


class CustomLoginView(LoginView):
	template_name = 'authentication/login.html'
	fields = '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('success')


class RegisterView(FormView):
	template_name = 'authentication/register.html'
	form_class = RegisterForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('success')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(RegisterView, self).form_valid(form)


def success(request):
	return render(request, 'authentication/success.html', {})