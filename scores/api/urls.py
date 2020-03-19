'''The Urls.py for the score API'''

#the path function
from django.urls import path
#import the views tied to scores
from scores.api.views import (IndividualScoreUpdateView, 
                            IndividualScoreListView, 
                            TotalScoreListView,
                            IndividualScoreTodayListView)

#the url patterns
urlpatterns = [
    path('score/<int:pk>/update/', IndividualScoreUpdateView.as_view(), name = 'update-score-api'),
    path('score/list/', IndividualScoreListView.as_view(), name = 'score-list-api'),
    path('score/list/today/', IndividualScoreTodayListView.as_view(), name = 'score-today-list-api'),
    #no params
    path('totalScore/list/', TotalScoreListView.as_view(), name = 'totalScore-list-api'),
    #params
    path('totalScore/list/?<str:month>', TotalScoreListView.as_view(), name = 'totalScore-list-api')
]