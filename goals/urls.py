#url paths for the goal app
from django.urls import path

from .views import GoalSurvey #the views to connect

urlpatterns = [
    path('survey/', GoalSurvey.as_view(), name = 'survey'),
]