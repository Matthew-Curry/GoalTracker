"""goal_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
##############################################OLD STUFF###################################################################################################
#from django.views.generic.base import TemplateView #the generic template view for use as the homepage########was for the home page
#the imports below are for the REST implementation
###########################################################################################################################################################
from django_registration.backends.one_step.views import RegistrationView
#the custom user forms
from accounts.forms import CustomUserCreationForm
from accounts.forms import CustomUserChangeForm
from core.views import IndexTemplateView, null_view



urlpatterns = [
    #catch redirects after views
    path(r'^rest-auth/registration/account-email-verification-sent/', null_view, name='account_email_verification_sent'),
    path(r'^rest-auth/registration/account-confirm-email/', null_view, name='account_confirm_email'),
    path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', null_view, name='password_reset_confirm'),

    #path to admin site
    path('admin/', admin.site.urls),

    #the path to the accounts api, runs through accounts api folder, uses UserSerializer in the appropriate view
    path("api/", include("accounts.api.urls")),

    #path to the goals api, runs through the goals api folder, users GoalSerializer in appropriate view
    path('api/', include('goals.api.urls')),

    #the path to the score api, runs through score api foler, uses the total score and individual score serializers in appropriate view
    path('api/', include('scores.api.urls')),

    #Login Through Browsable API
    path("api-auth/", include("rest_framework.urls")), #login is now option in API

    #Login Through REST 
    path("api/rest-auth/", include("rest_auth.urls")), #/login/ to get to the login API MAKE CUSTOM USER MODEL, IS ASKING FOR USERNAME #could overwrite serializer
    #to solve this problem, couuld be serializer, view, form

    #Registration via rest
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")), ####linked with a model with username probably


##############################################################OLD STUFF#########################################################################################
    #catch all path for redirects
    #re_path("^.*$", IndexTemplateView.as_view(), name = 'entry-point')
    #path('accounts/', include('accounts.urls')), #path to users urls, to access signup page api
    #path('accounts/', include('django.contrib.auth.urls')), #path to auth api, has views and urls for login and logout
    #path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'), #url conf for the home page
    #path('goals/', include('goals.urls'))#path to access goal app urls, the survey page and main app functionality
]
