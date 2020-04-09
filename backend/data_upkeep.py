'''A script that automates the creation of a new Total Score object and Individual Score objects for each User at the start of each day'''

#need to include django enviroment to use models
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goal_project.settings")
import django
django.setup()

#other imports
import schedule
import time
import datetime
from pytz import timezone
#import Goal models
from goals.models import Goal
#both scores models
from scores.models import TotalScore, IndividualScore
#import the user model
from accounts.models import CustomUser

#a function that creates the appropriate individual score and total score objects for the current day for a given user
def makeScores(user_):
    #the current day as an integer
    day = datetime.datetime.now(tz = timezone('US/Eastern')).weekday()
    #current date
    today = datetime.datetime.now(tz = timezone('US/Eastern'))
    print('today is of type')
    #the queryset holding all goals for the day
    query_set = None
    #variable that will hold the total score today
    total_score_today = None
    #get all goals that have to be done today
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
    #if the user does not have goal scheduled break else make total goal
    if len(query_set)!=0:
        #instantiate a total score, date is current date and score is initially 0
        total_score_today = TotalScore.objects.create(total_score = 0, date = today)
    else:
        return
    #for every goal in the query set, instantiate an individual score and ti/e to the total score
    for goal_ in list(query_set):
        score = IndividualScore.objects.create(goal = goal_, total_score = total_score_today, individual_score = 0)


#a method that makes scores for all users in the data base
def updateDataBase():
    #query all users
    users = CustomUser.objects.all()
    #iterate over and add new scores for each
    for user in users:
        makeScores(user)



###########################################################################
#FOR EVENTUAL USE ON SERVER

#update the database every day at 12 AM
#schedule.every().day.at('00:00').do(updateDataBase, 'Start of the day')

#An infinite loop to keep the updates consistent
#while True:
#    schedule.run_pending()
#    time.sleep(60)

#to update score objects during testing
updateDataBase()


