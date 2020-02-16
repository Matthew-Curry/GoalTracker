'''Views for the Goals API'''

#base classes to construct the views
from rest_framework import generics
from rest_framework.generics import get_object_or_404
#user needs to be authenticated to access goals
from rest_framework.permissions import IsAuthenticated
#the serializer and model
from goals.api.serializers import GoalSerializer
from goals.models import Goal


#create a new goal, will be used with initial survey
class GoalCreateAPIView(generics.CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    #tie the current user to the new goal
    def perform_create(self, serializer):
        request_user = self.request.user
        serializer.save(user = request_user)

#List API view of all goals, used as a read only endpoint for the main app
class GoalListAPIView(generics.ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    #get all goals that are for this user
    def get_queryset(self):
        user = self.request.user
        return Goal.objects.filter(user = user)

#delete, update goals when the period ends. Per each goal
class GoalRUDAPView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
