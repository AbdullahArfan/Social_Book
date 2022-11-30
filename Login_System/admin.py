from django.contrib import admin

# Register your models here.
from .models import UserProfile, Follow

admin.site.register(UserProfile)
admin.site.register(Follow)