#################The signals for the scores app, update the total score when individual scores are updated#####################
#import the post_save signal
from djanog.db.models.signal import post_save
#import involved models
from scores.models import IndividualScore, TotalScore

#the function to be calle when the individual score is updated
#def updateTotalScore(sender, **kwargs):
#    if kwargs['created']:
        #the updated instance
#        this_individual_score = kwargs['instance']
        #id of the individual score
#        id_ = int(this_individual_score.id)
        #the score
#        score_ = int(this_individual_score.individual_score)
        #the goal this score corosponds to 
#        goal = this_individual_score.goal



