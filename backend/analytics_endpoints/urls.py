#the path function
from django.urls import path
#views
from analytics_endpoints.views import TimeChartView, PieChartView, ProbView

urlpatterns = [
#url for the time chart
path('analytics/timeChart/', TimeChartView.as_view(), name = 'time-chart'),
#url for the pie chart
path('analytics/pieChart/', PieChartView.as_view(), name = 'pie-chart'),
#url for the probabilities
path('analytics/probs/', ProbView.as_view(), name = 'pie-chart')
]