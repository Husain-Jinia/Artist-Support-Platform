from django.contrib import admin
from django.urls import path
from .views import home, adminpage, scrape

urlpatterns = [
    path('', home, name="homepage"),
    path('adminpage', adminpage, name="adminpage"),
    path('scrape', scrape, name="scrape"),

]