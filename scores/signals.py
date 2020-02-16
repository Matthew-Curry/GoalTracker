'''The signals for the scores app, update the total score when individual scores are updated'''

#import the post_save signal
from django.db.models.signals import post_save
#import involved models
from scores.models import IndividualScore, TotalScore

#the function to be called when the individual score is updated
def updateTotalScore(sender, **kwargs):
    #the updated instance
    this_individual_score = kwargs['instance']
    #the total score obj tied to the instance
    this_total_score = this_individual_score.total_score
    #get all associated individual scores objects
    in_list = list(this_total_score.individual_scores.all())
    #iterate over pairs and add to the score
    updated_score = 0
    for obj in in_list:
        #get the score
        s = int(obj.individual_score)
        #get the goal value
        g = int(obj.goal.measure)
        #the int fraction is the normalized score
        s = int(100*(s/g))
        #get the weight
        w = int(obj.goal.weight)
        w = float(w/100)
        #the product
        prod = s * w
        prod = int(prod)
        #the updated score
        updated_score = updated_score + prod
    #set the updated score to the score of the total score object
    this_total_score.total_score = updated_score
    this_total_score.save()

#call on update of an individual score object
post_save.connect(updateTotalScore, sender = IndividualScore)



