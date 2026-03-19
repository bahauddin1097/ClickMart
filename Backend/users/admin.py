from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ['name', 'username', 'email', 'id', 'is_active']
    fieldsets = ()

    def name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


# Register your models here.
admin.site.register(User, UserAdmin)