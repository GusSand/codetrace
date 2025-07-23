"""Accounts views"""
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from quizzes.models import Player


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):  # type: ignore
        model = Player
        fields = UserCreationForm.Meta.fields  # type: ignore


class __typ0(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def show_privacy_policy(__tmp0: <FILL>) :
    return render(__tmp0, 'privacy_policy.html')
