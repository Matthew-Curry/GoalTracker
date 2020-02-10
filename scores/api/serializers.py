 #process will go like this:
#every day at 12AM, a method will instantiate indivdual goal objects for the day and a total score object FOR EACH USER, THIS IS DONE IN CORE.UTILS

#the current day's individual score objects will be presented to the user in the frontend when they log in that day

#they will fill these out. Once post a post request is sent, it will update the total score object

#will only present the score objects for the given day to the user





#a serializer for individual score


#add custom permission so only an authenitcated user on the same day can edit their score



#use signals to update the total score when the individual score is changed




#a serializer for total score, calls custom method to calculate the score


#import the models
from scores.models import TotalScore, IndividualScore
#import rest framework serializers
from rest_framework import serializers

#the serializer for individual goals
class IndividualScoreSerializer(serializers.ModelSerializer):
    #the meta data
    class Meta:
        model = IndividualScore
        fields = '__all__'
        #cannot change total score, goal object
        read_only_fields = ['goal', 'total_score']

#the serializer for the total score
class TotalScoreSerializer(serializers.ModelSerializer):
    #the meta data
    class Meta:
        model = TotalScore
        fields = '__all__'
