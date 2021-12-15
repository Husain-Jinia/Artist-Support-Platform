from django.contrib import admin
from .models import Posts, Tagname, User
# Register your models here.

admin.site.register(Posts)
admin.site.register(Tagname)
admin.site.register(User)
