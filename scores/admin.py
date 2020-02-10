from django.contrib import admin
#import the two models that hold scores
from scores.models import TotalScore, IndividualScore

#register the models
admin.site.register(TotalScore)
admin.site.register(IndividualScore)
