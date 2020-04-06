"""The View for the Sign Up Page"""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

#the view for the signup page
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('survey')
    template_name = 'signup.html'
