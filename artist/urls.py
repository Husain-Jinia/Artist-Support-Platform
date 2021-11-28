from django.contrib import admin
from django.urls import path
from .views import artpage, home, adminpage, scrape

urlpatterns = [
    path('', home, name="homepage"),
    path('adminpage', adminpage, name="adminpage"),
    path('scrape', scrape, name="scrape"),
    path('artpage', artpage, name="artpage"),


]