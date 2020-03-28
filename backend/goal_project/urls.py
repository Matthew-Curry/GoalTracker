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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
##############################################OLD STUFF###################################################################################################
#from django.views.generic.base import TemplateView #the generic template view for use as the homepage########was for the home page
#the imports below are for the REST implementation

#where i think this goes:

#there are url paths that lead to a login and signup templates

#there is a catch all template that sends all requests to a basic view that is stored in the core utils.
#this view uses a template onto which a single page application is mounted, which is where Vue changes to all the other functionality and makes
#api requests to get what it needs to run




###########################################################################################################################################################
from django_registration.backends.one_step.views import RegistrationView
#the custom user forms
from accounts.forms import (CustomUserCreationForm,
                            CustomUserChangeForm,
                            CustomRegistrationForm)

from core.views import IndexTemplateView, null_view



urlpatterns = [
    #catch redirects after views
    path(r'^rest-auth/registration/account-email-verification-sent/', null_view, name='account_email_verification_sent'),
    path(r'^rest-auth/registration/account-confirm-email/', null_view, name='account_confirm_email'),
    path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', null_view, name='password_reset_confirm'),

    #path to admin site
    path('admin/', admin.site.urls),

    #path to registration in the browser
    path("accounts/register/",
        RegistrationView.as_view(
            form_class=CustomRegistrationForm,
            success_url="/",
        ), name ='django_registration_register'),

    #needed for one step registration
    path('accounts/', include("django_registration.backends.one_step.urls")),

    #path to the login with the browser
    path('accounts/', include("django.contrib.auth.urls")),

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

    #a catch all url to send all url requests outside the previous set to the SPA
    re_path("^.*$", IndexTemplateView.as_view(), name = 'entry-point'),
]

#for static files, styling for the login and logout templates served by django
urlpatterns +=staticfiles_urlpatterns()