'''Views for the Goals API'''

#base classes to construct the views
from rest_framework import generics
from rest_framework.generics import get_object_or_404
#user needs to be authenticated to access goals
from rest_framework.permissions import IsAuthenticated
#the serializer and model
from goals.api.serializers import GoalSerializer
from goals.models import Goal
#for getting goals that are active today
from datetime import datetime


#create a new goal, will be used with initial survey
class GoalCreateAPIView(generics.CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    #tie the current user to the new goal
    def perform_create(self, serializer):
        request_user = self.request.user
        serializer.save(user = request_user)

#List API view of all goals, used as a read only endpoint for the calender
class GoalListAPIView(generics.ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    #get all goals that are for this user
    def get_queryset(self):
        user = self.request.user
        return Goal.objects.filter(user = user)

#a API view of all goals for that day. Used to populate the today page
class GoalListTodayAPIView(generics.ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    #get all goals that are for this user for this day
    def get_queryset(self):
        #the weekday as an integer
        day = datetime.now().weekday()
        #the user 
        user = self.request.user
        #use the day and the user to get the query set this method should return
        return self.return_query_set(day, user)
    
    #a method to set the day to what it should be
    def return_query_set(self, day, user_):
        if day == 0:
            query_set = Goal.objects.filter(mon=True, user = user_)
        elif day == 1:
            query_set = Goal.objects.filter(tues =True, user = user_)
        elif day ==2:
            query_set = Goal.objects.filter(wen=True, user = user_)
        elif day ==3:
            query_set = Goal.objects.filter(thurs=True, user = user_)
        elif day==4:
            query_set = Goal.objects.filter(fri=True, user = user_)
        elif day==5:
            query_set = Goal.objects.filter(sat=True, user = user_)
        else:
            query_set = Goal.objects.filter(sun=True, user = user_)
        #return the proper query set
        return query_set

#delete, update goals when the period ends. Per each goal
class GoalRUDAPView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
