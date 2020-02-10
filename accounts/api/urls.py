#The path function
from django.urls import path
#the appropriate view
from accounts.api.views import CurrentUserAPIView

#the url patterns
urlpatterns = [
    path('accounts/', CurrentUserAPIView.as_view(), name = 'current-user')
]