from django.urls import path
from .views import MainPageView, DetailPageView

urlpatterns = [
	path('', MainPageView.as_view(), name='main_page'),
	path('pokemon/<int:id>/', DetailPageView.as_view(), name='pokemon_detail'),
]
