'''The admin settings for the accounts app. Needs to be reconfigured because there is a custom user model'''
#to get the register function
from django.contrib import admin
#to help create our custom admin
from django.contrib.auth.admin import UserAdmin
#import the custom forms
from .forms import CustomUserCreationForm, CustomUserChangeForm
#import the custom model
from .models import CustomUser
#for translation
from django.utils.translation import gettext as _

#the custom user admin with new forms and model
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    #there is no username field, update attributes of parent class to account for this
    #the field sets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
        'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    #the add fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2')
        }),
    )
    #list_display
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    #search fields
    search_fields = ('email', 'first_name', 'last_name')
    #ordering
    ordering = ('email',)
    #primary key is readable
    readonly_fields = ('id',)


# Register models
admin.site.register(CustomUser, CustomUserAdmin)
