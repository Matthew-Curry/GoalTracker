'''Custom utils, functions that can be imported by the rest of the project'''

from accounts.models import CustomUser
from goals.models import Goal
from scores.models import TotalScore, IndividualScore 
from datetime import datetime
from django.test import Client
import json

#creates a user, used for repetitive pieces of test code
def create_user(email_, first, last):
    #make a user
    user =  CustomUser.objects.create_user(email = email_,
                                                        first_name = first,
                                                        last_name = last)
    user.set_password(r'a-very-strong-password')
    user.save()
    return user

#a method that creates a single goal, returns the goal
def single_goal(user_):
    Goal1 = Goal.objects.create(goal = 'test4',
                    category = 'fitness',
                    measure =  10, 
                    unit =  'minutes', 
                    weight = 100, 
                    mon = True,
                    tues = False,
                    wen = False,
                    thurs = False,
                    fri = False,
                    sat =  False,
                    sun =  False,
                    user = user_
                    )
    return Goal1


#a method that creates three goals
def create_three_goals(user_):
    Goal1 = Goal.objects.create(goal = 'test1',
                    category = 'fitness',
                    measure =  10, 
                    unit =  'minutes', 
                    weight = 100, 
                    mon = True,
                    tues = False,
                    wen = False,
                    thurs = False,
                    fri = False,
                    sat =  False,
                    sun =  False,
                    user = user_
                    )
    Goal2 = Goal.objects.create(goal = 'test2',
                    category = 'career',
                    measure =  10, 
                    unit =  'hours', 
                    weight = 100, 
                    mon = False,
                    tues = False,
                    wen = True,
                    thurs = False,
                    fri = False,
                    sat =  False,
                    sun =  False,
                    user = user_
                    )
    Goal3 = Goal.objects.create(goal = 'test3',
                    category = 'social',
                    measure =  10, 
                    unit =  'reps', 
                    weight = 100, 
                    mon = False,
                    tues = True,
                    wen = False,
                    thurs = False,
                    fri = False,
                    sat =  False,
                    sun =  False,
                    user = user_
                    )
    return [Goal1, Goal2, Goal3]

#a method that creates 3 total scores given a list of three goals
def create_three_scores():
    score1 = TotalScore.objects.create(total_score = 0, date = datetime.now())
    score2 = TotalScore.objects.create(total_score = 0, date = datetime.now())
    score3 = TotalScore.objects.create(total_score = 0, date = datetime.now())
    return [score1, score2, score3]

#a method that creates 3 individual score objects given first a list of goals and then a list of Total Scores
def create_three_ind_scores(goal_list, total_scores):
    IndividualScore.objects.create(goal = goal_list[0], individual_score = 10, total_score = total_scores[0])
    IndividualScore.objects.create(goal = goal_list[1], individual_score = 20, total_score = total_scores[1])
    IndividualScore.objects.create(goal = goal_list[2], individual_score = 30, total_score = total_scores[2])

#a method that creates three individual scores tied to one total score
def create_three_ind_scores_same(goal_list, total_score):
    IndividualScore.objects.create(goal = goal_list[0], individual_score = 10, total_score = total_score)
    IndividualScore.objects.create(goal = goal_list[1], individual_score = 20, total_score = total_score)
    IndividualScore.objects.create(goal = goal_list[2], individual_score = 30, total_score = total_score)

#method that makes an int and returns the corosponding month
def clean_month(num):
    month_str = ''
    if num == 1:
            month_str = 'January'
    elif num == 2:
            month_str = 'February'
    elif num == 3:
            month_str = 'March'
    elif num == 4:
            month_str = 'April'
    elif num == 5:
            month_str = 'May'
    elif num == 6:
            month_str = 'June'
    elif num == 7:
            month_str = 'July'
    elif num == 8:
            month_str = 'August'
    elif num == 9:
            month_str = 'September'
    elif num == 10:
            month_str = 'October'
    elif num == 11:
            month_str = 'November'
    elif num == 12:
            month_str = 'December'
    
    return month_str




    





