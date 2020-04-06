'''The Urls.py for the score API'''

#the path function
from django.urls import path
#import the views tied to scores
from scores.api.views import (IndividualScoreUpdateView,  
                            TotalScoreListView,
                            IndividualScoreListView)

#the url patterns
urlpatterns = [
    path('score/update/', IndividualScoreUpdateView.as_view(), name = 'update-score-api'),
    #no params
    path('totalScore/list/', TotalScoreListView.as_view(), name = 'totalScore-list-api'),
    #params
    path('totalScore/list/?<str:month>', TotalScoreListView.as_view(), name = 'totalScore-list-api'),
    #get list of individual scores, used for testing purposes
    path('score/list/', IndividualScoreListView.as_view(), name = 'score-list-api'),
]