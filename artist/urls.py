from django.contrib import admin
from django.urls import path
from .views import adminlogout, artpage, contact, home, adminpage, scrape,about, adminlogin,logout, Signup,Login

urlpatterns = [
    path('', home, name="homepage"),
    path('adminpage', adminpage, name="adminpage"),
    path('scrape', scrape, name="scrape"),
    path('artpage', artpage, name="artpage"),
    path('about', about, name="about"),
    path('adminlogin', adminlogin, name="adminlogin"),
    path('adminlogout', adminlogout, name="adminlogout"),
    path('contact', contact, name='contact'),
    path('signup', Signup.as_view(), name="signup"),
    path('login', Login.as_view(),  name="login"),
    path('logout', logout,  name="logout"),
    # path('like/<int:pk>', LikeView, name='like_post'),
]