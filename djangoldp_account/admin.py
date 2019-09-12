from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LDPUser

admin.site.register(LDPUser, UserAdmin)