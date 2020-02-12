###########The Urls.py for the score api#############
#the path function
from django.urls import path
#import the views tied to scores
from scores.api.views import IndividualScoreUpdateView, IndividualScoreListView, TotalScoreListView

#the url patterns
urlpatterns = [
    path('score/<int:pk>/update/', IndividualScoreUpdateView.as_view(), name = 'update-score-api'),
    path('score/list/', IndividualScoreListView.as_view(), name = 'score-list-api'),
    path('totalScore/list/', TotalScoreListView.as_view(), name = 'totalScore-list-api')
]