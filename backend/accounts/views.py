#NOT SURE IF I AM KEEPING THIS

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

#the view for the signup page
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('survey') ######try sending to survey page
    template_name = 'signup.html'
