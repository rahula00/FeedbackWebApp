import random
import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import  Feedback
from mainApp.forms import CreateFeedbackForm, UpdateUserForm
from django.contrib.auth.models import User


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
        F = CreateFeedbackForm(request.POST)
        if F.is_valid():
            new_feedback = F.save()
            
    form = CreateFeedbackForm()
    context = {
        'managers': User.objects.all(),
        'type_choice': Feedback.TYPE_CHOICES,
        'form': form
    }
    return render(request, 'list.html', context)


@login_required(login_url='homepage')
def manager(request):
    
    context = {
        'feedbacks': Feedback.objects.filter(manager=request.user)
    } 
    return render(request, 'manager.html', context)


@login_required(login_url='homepage')
def adminPage(request):

    
    
    if request.method == "POST":
        # Get a user ID from the post
        # Find user with that ID
        # Update user 
        F = UpdateUserForm(request.POST, instance=request.user)
        if F.is_valid():
            F.save()


    form = UpdateUserForm()
    context = {
        'managers': User.objects.all(),
        'form': form
    } 
    return render(request, 'admin.html', context)


def logout_request(request):
    messages.info(request, f"{request.user.username} has been logged out")
    logout(request)
    return redirect(home)

