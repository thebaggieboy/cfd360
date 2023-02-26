from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from django.contrib.auth.admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import UserProfile, BaseUserManager, AbstractBaseUser, Wallets, Deposits, Withdraw, CustomUser, Transaction, Banks




class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name','last_name')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()



class UserProfileAdmin():
    list_display = ['user', 'wallet', 'amount', 'date_created']
    search_fields = ['user']
    ordering = ['-date_created']

admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Banks)
admin.site.register(Wallets)
admin.site.register(Transaction)
admin.site.register(Deposits)
admin.site.register(Withdraw)
