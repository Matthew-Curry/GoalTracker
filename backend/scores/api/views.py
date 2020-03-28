'''The relevant views for the Individual Score and Total Score'''

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
        #only select scores made by this user today
        return IndividualScore.objects.filter(goal__in=goals, total_score__in= total_score_today)

#a view for retrieving all scores for the user on the current day for the purpose of display
class IndividualScoreTodayListView(generics.ListAPIView):
    serializer_class = IndividualScoreSerializer
    permission_classes = [IsAuthenticated]
    #the query set are only score that are tied to goals of the user, and are scores created today
    def get_queryset(self):
        #the user
        user = self.request.user
        #the user's goals
        goals = list(Goal.objects.filter(user = user))
        #today's date
        today = datetime.now()
        #list of goals created today
        total_score_today = TotalScore.objects.filter(date = today)
        #only select scores made by this user today
        return IndividualScore.objects.filter(goal__in=goals, total_score__in= total_score_today)

    
#the view for retriving all user goals. Accepts an optional paramter to allow for viewing goals for a particular total score defined by the passed in primary key of the total score object
class IndividualScoreListView(generics.ListAPIView):
    serializer_class = IndividualScoreSerializer
    permission_classes = [IsAuthenticated]
    #the query set is all scores corosponding to goals set by the user
    def get_queryset(self):
        #filter for total score id if passed in
        total_score_id = self.request.query_params.get('id', None)
        if total_score_id is not None:
            score_list = IndividualScore.objects.filter(total_score = total_score_id)
        else:
            #filter by just user
            user = self.request.user
            goals = list(Goal.objects.filter(user = user))
            score_list = IndividualScore.objects.filter(goal__in = goals)
        #only select scores for this user's goals
        return score_list

#A list view of the scores to see all scores accumulated by a user. Accepts a query paramter for the month filter. In the form of a string "Month YYYY"
class TotalScoreListView(generics.ListAPIView):
    serializer_class = TotalScoreSerializer
    permission_classes = [IsAuthenticated]
    #the query set is all scores corosponding to goals set by the user
    def get_queryset(self):
        #the user
        user = self.request.user
        #the users goals
        goals = list(Goal.objects.filter(user = user))
        #a list of all individual scores
        scores_ = IndividualScore.objects.filter(goal__in = goals)
        #use individual scores to get total scores
        total_scores = TotalScore.objects.filter(id__in=scores_.values('total_score_id'))
        #clean the month param and filter if there
        month_arg = self.request.query_params.get('month', None)
        if month_arg is not None:
            month_filters = self.clean_month(month_arg)
            month = month_filters[0]
            year = month_filters[1]
            #filter by user and month
            total_scores = TotalScore.objects.filter(id__in=scores_.values('total_score_id'), date__year = year, date__month = month)
        else:
            #filter by just user
            total_scores = TotalScore.objects.filter(id__in=scores_.values('total_score_id'))
        
        return total_scores
    
    #a method that takes the month in the form "Month YYYY and returns a list, month then year"
    def clean_month(self, month):
        month_filters = month.split(' ')
        month_filters[1] = int(month_filters[1])
        month_str = month_filters[0]
        if month_str == 'January':
            month_filters[0] = 1
        elif month_str == 'February':
            month_filters[0] = 2
        elif month_str == 'March':
            month_filters[0] = 3
        elif month_str == 'April':
            month_filters[0] = 4
        elif month_str == 'May':
            month_filters[0] = 5
        elif month_str == 'June':
            month_filters[0] = 6
        elif month_str == 'July':
            month_filters[0] = 7
        elif month_str == 'August':
            month_filters[0] = 8
        elif month_str == 'September':
            month_filters[0] = 9
        elif month_str == 'October':
            month_filters[0] = 10
        elif month_str == 'November':
            month_filters[0] = 11
        elif month_str == 'December':
            month_filters[0] = 12
        

        return month_filters
    




