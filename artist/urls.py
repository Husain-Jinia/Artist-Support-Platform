from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name="homepage"),
    path('adminpage', adminpage, name="adminpage"),
    path('scrape', scrape, name="scrape"),
    path('artpage', artpage, name="artpage"),
    path('about', about, name="about"),
    # path('adminlogin', adminlogin, name="adminlogin"),
    # path('adminlogout', adminlogout, name="adminlogout"),
    path('contact', contact, name='contact'),
    path('logout', logout,  name="logout"),
    path('favourites/<int:pk>', favourite, name='favourite'),
    path('register/',register, name='register'),
    path('favouritepage', favouriteArtists, name="favourite-page"),
    path('login/',auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'logout.html'), name='logout'),
]