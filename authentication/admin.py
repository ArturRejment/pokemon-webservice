from django.contrib import admin

from .models import Pokemon, User

admin.site.register(User)
admin.site.register(Pokemon)
