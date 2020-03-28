'''The serializers for the Individual Score and Total Score models'''

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
