from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOriginal
from .models import User


# Register your models here.
class UserAdmin(UserAdminOriginal):
    model = User


admin.site.register(User, UserAdmin)
