from django.shortcuts import render
#import django's create view to make an entry in the goals database
from django.views.generic.edit import CreateView
#import the goal database
from .models import Goal

#the survey view
class GoalSurvey(CreateView):
    model = Goal
    fields = '__all__'
    template_name = 'survey.html'

    #a method to automatically set the author of an article to the current user
    #def form_valid(self, form):
     #   form.instance.author = self.request.user  #########not sure if this will work
      #  return super().form_valid(form)
