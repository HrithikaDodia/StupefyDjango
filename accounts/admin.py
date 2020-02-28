from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TwoFAUser
from .forms import RegistrationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserAdmin(BaseUserAdmin):
    add_form =  RegistrationForm

    list_display = ('username', 'email','phonenumber','is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'email','phonenumber','password')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields =  ('username','email')
    ordering = ('username','email')

    filter_horizontal = ()

admin.site.register(TwoFAUser,UserAdmin)
admin.site.unregister(Group)