import random
import json

from django.shortcuts import render, redirect

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from .models import  Feedback
from mainApp.forms import CreateFeedbackForm, UpdateUserForm, CreateUserForm

from rest_framework import viewsets, filters
from .serializers import FeedbackSerializer
from django.views.decorators.csrf import csrf_exempt

def get_feedback(request=None):
    id = request.GET.get('id', None)
    obj = Feedback.objects.get(pk=id)
    fb = obj.feedback
    data={
        'feedbacks' : fb
    }
    return JsonResponse(data)

@csrf_exempt
def get_feedbacks(request=None):
    objs = Feedback.objects.all().order_by('-created_at')
    serializer = FeedbackSerializer(objs, many=True)
    return JsonResponse(serializer.data, safe=False)


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
def manager(request, fb=None):
    
    context = {
        'feedbacks': Feedback.objects.filter(manager=request.user)
    } 
    return render(request, 'manager.html', context)


@login_required(login_url='homepage')
def adminPage(request):

    if request.method == "POST":
        pk = request.POST.get('id') # Get a user ID from the post
        user = User.objects.get(id=pk) # Find user with that ID
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save() # Update user 
    else:
        form = UpdateUserForm(instance=request.user)

    context = {
        'managers': User.objects.all(),
        'form': form
    } 
    return render(request, 'admin.html', context)

@login_required(login_url='homepage')
def feedback_delete(request, id=None):
    obj = Feedback.objects.get(pk=id)
    obj.delete()
    return redirect('/manager')


@login_required(login_url='homepage')
def mark_read(request, id=None):
    obj = Feedback.objects.get(pk=id)
    obj.isRead = True
    obj.save()
    return redirect('/manager')



@login_required(login_url='homepage')
def add_manager(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminPage') #Not sure 

    else:
        form = CreateUserForm()

    context = {
        'form': form
    }

    return render(request, 'add_manager.html', context)



def logout_request(request):
    messages.info(request, f"{request.user.username} has been logged out")
    logout(request)
    return redirect(home)

