'''The Serializer for the Goal Model'''

#import the goal model
from goals.models import Goal
#import serializers
from rest_framework import serializers

#the serializer for the goal model
class GoalSerializer(serializers.ModelSerializer):
    #user is the related field
    user = serializers.StringRelatedField(read_only = True)
    #the meta class, tie to the appropriate model
    class Meta:
        model = Goal
        fields = '__all__'
    #method to restrict the category to an appropriate value
    def validate_category(self, value):
        #the list of appropriate categories in lowercase
        cat = ['fitness', 'social', 'education', 'career', 'hobby']
        #raise error if value is not one of these
        if value.lower() not in cat:
            raise serializers.ValidationError('Pick one of the allowed categories')
        return value