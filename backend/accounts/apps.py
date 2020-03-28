from django.apps import AppConfig
from django.conf import settings
from django.contrib import auth


class AccountsConfig(AppConfig):
    name = 'accounts'
    #method to set the proper redirect for the auth
    def ready(self):
        auth.REDIRECT_FIELD_NAME = settings.REDIRECT_FIELD_NAME