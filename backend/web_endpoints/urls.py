#the path function
from django.urls import path
#views
from web_endpoints.views import GoalToScoreOfTotalView, ScoreTodayView

urlpatterns = [
#no params
path('endpoints/goal-to-scores/', GoalToScoreOfTotalView.as_view(), name = 'goal-to-scores-api'),
#params
path('endpoints/goal-to-scores/?<int:id>', GoalToScoreOfTotalView.as_view(), name = 'goal-to-scores-api'),
#endpoint for ScoeToday page
path('endpoints/ScoreToday/', ScoreTodayView.as_view(), name = 'ScoreToday')
]