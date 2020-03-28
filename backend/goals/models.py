'''Defines the Goal model'''

from django.db import models
#the user model
from accounts.models import CustomUser
#the validators
from django.core.validators import MaxValueValidator, MinValueValidator

#a model for holding user goals
class Goal(models.Model):
    #the user models is the foriegn key
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name= 'goals')
    #Can picks from 5 categories, restricted options in serializer 
    category = models.CharField(max_length = 255)
    #user writes goal
    goal = models.CharField(max_length = 255)
    #User defines integer measure
    measure = models.IntegerField()
    #user defines any unit
    unit = models.CharField(max_length = 255)
    #user defines the amount of wieght of this goal
    weight = models.IntegerField(
        default = 0,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    #picks multiple days for the goal
    mon = models.BooleanField()
    tues = models.BooleanField()
    wen = models.BooleanField()
    thurs = models.BooleanField()
    fri = models.BooleanField()
    sat = models.BooleanField()
    sun = models.BooleanField()

    
