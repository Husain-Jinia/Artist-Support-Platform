from django.contrib import admin
from django.urls import path
from .views import adminlogout, artpage, home, adminpage, scrape,about, adminlogin

urlpatterns = [
    path('', home, name="homepage"),
    path('adminpage', adminpage, name="adminpage"),
    path('scrape', scrape, name="scrape"),
    path('artpage', artpage, name="artpage"),
    path('about', about, name="about"),
    path('adminlogin', adminlogin, name="adminlogin"),
    path('adminlogout', adminlogout, name="adminlogout")
]