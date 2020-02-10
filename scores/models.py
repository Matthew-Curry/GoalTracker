from django.db import models
#a score object holds goals
from goals.models import Goal

#a model for holding scores
class TotalScore(models.Model):
    #holds an aggregate score, 1 to 100
    total_score = models.IntegerField()
    #total score is by date
    date = models.DateField()

#a model for individual scores, tied to one total score
class IndividualScore(models.Model):
    #an individual score is tied to one goal
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    #the individual score
    individual_score = models.IntegerField()
    #tied to a total score
    total_score = models.ForeignKey(TotalScore, related_name = 'individual_scores', on_delete = models.CASCADE)


