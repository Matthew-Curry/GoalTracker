'''The URLs for the goals API'''

#import path function
from django.urls import path
#import appropriate views
from goals.api.views import (GoalCreateAPIView, 
                            GoalListAPIView, 
                            GoalRUDAPView,
                            GoalListTodayAPIView)

#the url patterns
urlpatterns = [
    path('goal/create/', GoalCreateAPIView.as_view(), name = 'create-api'),
    path('goal/list/', GoalListAPIView.as_view(), name = 'list-api'),
    path('goal/<int:pk>/update/', GoalRUDAPView.as_view(), name = 'update-api'),
    path('goal/list/today/', GoalListTodayAPIView.as_view(), name = 'list-api-today')
]