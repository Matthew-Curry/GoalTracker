#create individual scores for a given goal

#view total scores for a given goal

#import generic api views
from rest_framework import generics
#the approriate serialziers
from scores.api.serializers import IndividualScoreSerializer, TotalScoreSerializer
#the permission
from rest_framework.permissions import IsAuthenticated
#the goals model
from goals.models import Goal
#individual scores model
from scores.models import IndividualScore, TotalScore
#for the custom exception
from rest_framework.exceptions import APIException
#for getting individual score objects created today, need current date
from datetime import datetime

#the view for updating individual scores for a user's goals for that day
class IndividualScoreUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = IndividualScoreSerializer
    permission_classes = [IsAuthenticated]

    #the query set are only score that are tied to goals of the user, and are scores created today
    def get_queryset(self):
        #the user
        user = self.request.user
        #the user's goals
        goals = list(Goal.objects.filter(user = user))
        #today's date
        today = datetime.today()
        #list of goals created today
        total_score_today = TotalScore.objects.filter(date = today)
        print(total_score_today)
        #only select scores made by this user today
        return IndividualScore.objects.filter(goal__in=goals, total_score__in= total_score_today)
    
#the view for retriving all user goals to populate the calender in the main app
class IndividualScoreListView(generics.ListAPIView):
    serializer_class = IndividualScoreSerializer
    permission_classes = [IsAuthenticated]
    #the query set is all scores corosponding to goals set by the uset
    def get_queryset(self):
        #the user
        user = self.request.user
        #the users goals
        goals = list(Goal.objects.filter(user = user))
        #only select scores for this user's goals
        return IndividualScore.objects.filter(goal__in = goals)

