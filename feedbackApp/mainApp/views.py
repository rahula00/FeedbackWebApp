import random
import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Managers, Feedback
from mainApp.forms import CreateFeedbackForm


def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('manager/') #Not sure 
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                  template_name = "index.html",
                  context={"form":form})


def index(request):
    if request.method == 'POST':
        form = CreateFeedbackForm(request=request, data=request.POST)
        if form.is_valid():
            new_feedback = form.save()
            


    form = CreateFeedbackForm()
    context = {
        'managers': Managers.objects.all(),
        'type_choice': Feedback.TYPE_CHOICES,
        'form': form
    }
    return render(request, 'list.html', context)


@login_required(login_url='homepage')
def manager(request):
    
    context = {
        'feedbacks': Feedback.objects.filter(manager__first_name__contains="Steve") #Change this to the name / id of the logged in user/manager
    } 
    return render(request, 'manager.html', context)

def logout_request(request):
    messages.info(request, f"{request.user.username} has been logged out")
    logout(request)
    return redirect(home)

