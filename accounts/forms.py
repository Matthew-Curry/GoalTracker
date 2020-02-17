'''File including relevant user forms'''

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_registration.forms import RegistrationForm

from .models import CustomUser

#user creation form with new model
class CustomUserCreationForm(UserCreationForm):
    #meta data to provide to the creation form
    class Meta(UserCreationForm.Meta):
        #the model is the custom model
        model = CustomUser
        fields = ('email', 'password1', 'password2')
        #fields = ('email', 'password1', 'password2')

#custom user change form
class CustomUserChangeForm(UserChangeForm):
    #meta data for the user change form
    class Meta:
        #the model is the custom model
        model = CustomUser
        fields = ('email', 'password','first_name', 'last_name')

#the custom registation form tied to the custom user model
class CustomRegistrationForm(RegistrationForm):
    #the meta class
    class Meta(RegistrationForm.Meta):
        model = CustomUser

    