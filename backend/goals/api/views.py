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
#the API View
from rest_framework.views import APIView
#for the response
from rest_framework.response import Response
from rest_framework import status

class GoalCreateAPIView(APIView):
    """Create a new goal. Can accept multiple goals for use with the intitial survey at app start"""
    permission_classes = [IsAuthenticated]
    #tie the current user to the new goal
    def post(self, request, format=None):
        data = request.data
        request_user = request.user
        serializer = GoalSerializer(data=data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save(user = request_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#List API view of all goals, used as a read only endpoint for the calender
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
