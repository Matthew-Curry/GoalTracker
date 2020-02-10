#url paths for the accounts app, connect to signup page
from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
]