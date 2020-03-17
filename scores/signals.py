'''The signals for the scores app, update the total score when individual scores are updated'''

#import the post_save signal
from django.db.models.signals import post_save
#import involved models
from scores.models import IndividualScore, TotalScore

#the function to be called when the individual score is updated
def update_total_score(sender, **kwargs):
    #the updated instance
    this_individual_score = kwargs['instance']
    #the total score obj tied to the instance
    this_total_score = this_individual_score.total_score
    #get all associated individual scores objects
    in_list = list(this_total_score.individual_scores.all())
    #group individual scores that have the same category
    in_list = group_list(in_list)
    #iterate over pairs and add to the score. If encounter a list (same category) will need to add scores before applying wieghting
    updated_score = 0
    for obj in in_list:
        #check if obj is list, if so account for multiple goals of same category
        if isinstance(obj, list):
            #sum the scores and the goal measures
            s = 0
            g = 0
            for score_ in obj:
                #add to score
                s = s + int(score_.individual_score)
                #add to goal value
                g = g + int(score_.goal.measure)
            #all weights are the same, so just get from the first one
            w = int(obj[0].goal.weight)
            w = float(w/100)
        #otherwise, handle individual item
        else:
            #get the score
            s = int(obj.individual_score)
            #get the goal value
            g = int(obj.goal.measure)
            #get the weight
            w = int(obj.goal.weight)
            w = float(w/100)
        #Now use score, goal, and wieght values to calculate
        #normalized score
        s = int(100*(s/g))
        #the product
        prod = s * w
        prod = int(prod)
        #the updated score
        updated_score = updated_score + prod
    #set the updated score to the score of the total score object
    this_total_score.total_score = updated_score
    this_total_score.save()

#a function that takes a list of individual scores and returns a list where all scores of goals in the same
#category are put into lists of length 2
def group_list(in_list):
    #make a list of all the categories of the scores
    cat_list = []
    for score in in_list:
        #get the category
        cat = score.goal.category
        #append to cat list
        cat_list.append(cat)
    #the list of score values to return
    grouped = []
    #identified indices to prevent dups
    visited = []
    #iterate over cat list, make duplicate sets
    for i in range(0, len(cat_list)):
        #if visited, continue
        if(i in visited):
            continue
        else:
            visited.append(i)
            #the set right now is just this score
            the_set = [in_list[i]]
            #the value at that index
            the_cat = cat_list[i]
            #iterate over from one spot ahead
            for j in range(i+1, len(cat_list)):
                if the_cat == cat_list[j]:
                    #visited
                    visited.append(j)
                    #append to list defining the set of this category
                    the_set.append(in_list[j])
            #check if length 1, if so just use the value. otherwwise, append the set
            if len(the_set) == 1:
                grouped.append(in_list[i])
            else:
                grouped.append(the_set)
            
    #after iteration, return the list
    return grouped
        
#call on update of an individual score object
post_save.connect(update_total_score, sender = IndividualScore)



