#the API View
from rest_framework.views import APIView
#the models
from scores.models import IndividualScore, TotalScore
from goals.models import Goal
#the approriate serialziers
from scores.api.serializers import IndividualScoreSerializer, TotalScoreSerializer
from goals.api.serializers import GoalSerializer
#the permission
from rest_framework.permissions import IsAuthenticated
#the ressponse
from rest_framework.response import Response
#for getting score information for the current day
from datetime import datetime


class GoalToScoreOfTotalView(APIView):
    """An API view that returns goals mapped to scores achieved for a particular total score id"""
    
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        #filter for total score id
        total_score_id = request.query_params.get('id', None)
        #get all individual scores coropsponding to this total score
        ind_scores = list(IndividualScore.objects.filter(total_score= total_score_id))
        #iterate over scores and append to json object
        the_response = {}
        for id_ in ind_scores:
            #get individual score data, use to get goal data
            ind_score_data = IndividualScoreSerializer(id_).data
            goal_id = ind_score_data['goal']
            goal = list(Goal.objects.filter(id= goal_id))[0]
            goal_data = GoalSerializer(goal).data
            
            #get pieces you need from data
            goal_score = ind_score_data['individual_score']
            goal_name = goal_data['goal']
            goal_unit = goal_data['unit']

            the_response[goal_name] = [goal_score, goal_unit]
        
        return Response(the_response)

class ScoreTodayView(APIView):
    """An API view that returns the information needed for the ScoreToday Component in the Front End. Needs goal information
    for presentation and individual score id for submission of the scores."""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        today = datetime.today()
        total_score_today = TotalScore.objects.filter(date = today)
        user_goals = Goal.objects.filter(user = request.user)
        #individual scores associated with this score and user
        ind_scores = list(IndividualScore.objects.filter(total_score__in= total_score_today, goal__in = user_goals))
        #iterate over scores and append corosponding goal (there is a one to one relationship) to the response
        the_response = {}
        for id_ in ind_scores:
            #get individual score data, use to get goal data
            ind_score_data = IndividualScoreSerializer(id_).data
            goal_id = ind_score_data['goal']
            goal = list(Goal.objects.filter(id= goal_id))[0]
            goal_data = GoalSerializer(goal).data

            #get pieces you need from data
            goal_score = ind_score_data['individual_score']
            ind_score_id = ind_score_data['id']
            goal_name = goal_data['goal']
            goal_unit = goal_data['unit']
            goal_measure = goal_data['measure']
            goal_cat = goal_data['category']
            entry = [goal_name, goal_score, goal_unit, goal_measure, ind_score_id]
            #determine how to add to object
            if goal_cat in list(the_response.keys()):
                the_response[goal_cat].append(entry)
            else:
                the_response[goal_cat] = [entry]
        
        return Response(the_response)



