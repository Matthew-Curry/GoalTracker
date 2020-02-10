from django.contrib import admin
#import the goals model
from goals.models import Goal

#register the models
admin.site.register(Goal)
