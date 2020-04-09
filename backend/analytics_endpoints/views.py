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
from datetime import datetime, timedelta

class TimeChartView(APIView):
    """View for the time series chart. Returns days and weighted scores by category for each day"""
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        day_one = TotalScore.objects.first().date
        last_day = TotalScore.objects.last().date
        #list of days
        date_list = [day_one + timedelta(days=x) for x in range((last_day-day_one).days + 1)]
        #list of categories
        cat_list = list(Goal.objects.values_list('category', flat=True).distinct())
        #the response with empty list as values
        response = {k:[] for k in cat_list}
        response['days'] = date_list
        #iterate over days and get weighted score for each day and category combo and append
        for day in date_list:
            for cat in cat_list:
                total_scores = TotalScore.objects.filter(date = day)
                goals = Goal.objects.filter(user = request.user, category = cat)
                scores = IndividualScore.objects.filter(total_score__in = total_scores, goal__in = goals)
                s = 0
                g = 0
                if scores:
                    for score_ in scores:
                        s = s + score_.individual_score
                        g = g + score_.goal.measure

                    weight = list(scores)[0].goal.weight
                    weight = float(weight/100)
                    s_norm = int(100*(s/g))
                    prod = s_norm * weight
                    prod = int(prod)
                    response[cat].append(prod)
                else:
                    response[cat].append(0)
        
        return Response(response)

class PieChartView(APIView):
    """View for returning data for the pie chart."""

    def get_per_weight(self, cat_list, user, time):
        """A function that returns the weight as dictated by performance for each category in a dictionary. Takes the 
        list of categories to cover, the request user, and the number of days back to cover, can accept string "start" to define since inception"""

        date_list = []
        if time == "start":
            day_one = TotalScore.objects.first().date
            last_day = TotalScore.objects.last().date
            #list of days
            date_list = [day_one + timedelta(days=x) for x in range((last_day-day_one).days + 1)]
        else:
            day_one = datetime.now() - timedelta(days=time)
            day_one = day_one.date()
            last_day = TotalScore.objects.last().date
            #list of days
            date_list = [day_one + timedelta(days=x) for x in range((last_day-day_one).days + 1)]
        
        # the response
        response = {k:0 for k in cat_list}

        # iterate over days, add all scores given, all goals set, divide to get weight. Perform for each cat
        for cat in cat_list:
            sum_norm = 0
            for day in date_list:
                total_scores = TotalScore.objects.filter(date = day)
                goals = Goal.objects.filter(user = user, category = cat)
                scores = IndividualScore.objects.filter(total_score__in = total_scores, goal__in = goals)
                for score in scores:
                    s = score.individual_score
                    g = score.goal.measure
                    sum_norm = sum_norm + int(100*s/g)
            
            response[cat] = sum_norm
            
        # iterate over and divide by overall sum
        new_overall = sum(list(response.values()))
        for cat in cat_list:
            response[cat] = float(response[cat]/new_overall)

        return response

    def get(self, request):
        #list of categories
        cat_list = list(Goal.objects.values_list('category', flat=True).distinct())
        #parallel boolean list to mark if weight was grabbed
        cat_check = [False] * len(cat_list)
        #the current user
        user = request.user
        #build first mapping of categories to weights. Iterate over goals and pick out categories
        response = {'current': {}}
        user_goals = Goal.objects.filter(user = user)
        for goal in user_goals:
            cat = goal.category
            index = cat_list.index(cat)
            if cat_check[index] ==  False:
                weight = goal.weight
                response['current'][cat] = weight
                cat_check[index] = True
        
        response['past_week'] = self.get_per_weight(cat_list, user, 7)
        response['past_30'] = self.get_per_weight(cat_list, user, 30)
        response['past_60'] = self.get_per_weight(cat_list, user, 60)
        response['past_90'] = self.get_per_weight(cat_list, user, 90)
        response['since_start'] = self.get_per_weight(cat_list, user, "start")

        return Response(response)
        
class ProbView(APIView):
    """A view for returning the probilities associted with the liklihood of a user completing a goal on the most and least likely
        days and categories
        
        Probabilities are proxied as (number of points scored on day/number of points possible to score"""

    def get(self, request):
        # the results of min and max prob by day
        day_response = self.day_results(request.user)

        # the result of min and max prob by category
        cat_response = self.cat_results(request.user)

        # merge the two for the response
        day_response.update(cat_response)
        
        return Response(day_response)

    # a method for buidling the response object by day
    def day_results(self, user):
        # list probabilities by day, initially set value to index for filter, will be overwritten before response returned
        date_filters = {'Sunday': 0, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7}
        day_response = {'most': [0], 'least': [float('inf')]}
        days = list(date_filters.keys())
        # get probability proxies by day 
        for day in days:
            day_num = date_filters[day]
            # get all scores from that day and add 
            total_scores = TotalScore.objects.filter(date__week_day = day_num)
            user_goals = Goal.objects.filter(user = user)
            scores = list(IndividualScore.objects.filter(total_score__in = total_scores, goal__in = user_goals).values_list('individual_score', flat = True))
            score_obj = IndividualScore.objects.filter(total_score__in = total_scores)
            poss = []
            for score in score_obj:
                goal = score.goal.measure
                poss.append(goal)

            day_points_scored = sum(scores)
            poss_points = sum(poss)

            if poss_points !=0:
                prob = day_points_scored/poss_points
                prob = int(round(prob *100))
                #determine if prob is min or max, add if so
                day_response = self.det_add(prob, day, day_response)
            else:
                prob = 0
                day_response = self.det_add(prob, day, day_response)
        
        day_response['dayMost'] = day_response.pop('most')
        day_response['dayLeast'] = day_response.pop('least')

        return day_response

    # a method for seeing if a prob should be added for day obj
    def det_add(self, prob, item, response):
        if response['most'][0]< prob:
            response['most'] = [prob, item]
        elif response['most'][0] == prob:
            response['most'].append(item)
        
        if response['least'][0] > prob:
            response['least'] = [prob, item]
        elif response['least'][0] == prob:
            response['least'].append(item)
        
        return response
    
    # a method for returning the response by category
    def cat_results(self, user):
        # list probabilities by day, initially set value to index for filter, will be overwritten before response returned
        cat_response = {'most': [0], 'least': [float('inf')]}
        cats = list(Goal.objects.values_list('category', flat=True).distinct())

        # get probability proxies by cat
        for cat in cats:
            # get all scores from that cat and add 
            user_goals = Goal.objects.filter(user = user, category = cat)
            scores = list(IndividualScore.objects.filter(goal__in = user_goals).values_list('individual_score', flat = True))
            score_obj = IndividualScore.objects.filter(goal__in = user_goals)
            poss = []
            for score in score_obj:
                goal = score.goal.measure
                poss.append(goal)

            day_points_scored = sum(scores)
            poss_points = sum(poss)

            if poss_points !=0:
                prob = day_points_scored/poss_points
                prob = int(round(prob *100))
                #determine if prob is min or max, add if so
                cat_response = self.det_add(prob, cat, cat_response)
            else:
                prob = 0
                cat_response = self.det_add(prob, cat, cat_response)

        cat_response['catMost'] = cat_response.pop('most')
        cat_response['catLeast'] = cat_response.pop('least')
        
        return cat_response



