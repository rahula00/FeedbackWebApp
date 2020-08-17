import random, string
import json
import urllib
from django.conf import settings


from django.shortcuts import render, redirect

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages

from .models import  Feedback
from mainApp.forms import CreateFeedbackForm, UpdateUserForm, CreateUserForm, UpdateCurrentUserForm, ForgotPassForm

from rest_framework import viewsets, filters
from .serializers import FeedbackSerializer
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail


@login_required(login_url='homepage')
def get_feedback(request=None):
    id = request.GET.get('id', None)
    obj = Feedback.objects.get(pk=id)
    fb = obj.feedback
    data={
        'feedbacks' : fb
    }
    return JsonResponse(data)

@csrf_exempt
@login_required(login_url='homepage')
def get_feedbacks(request=None):
    testreq = request.GET.get('test', None)
    objs = Feedback.objects.filter(manager=request.user).order_by('-created_at')
    serializer = FeedbackSerializer(objs, many=True)
    print(testreq)
    return JsonResponse(serializer.data, safe=False)

@login_required(login_url='homepage')
def delete_feedback(request):
    id = request.GET.get('id', None)
    obj = Feedback.objects.get(pk=id)
    obj.delete()
    return render(request, 'manager.html', {})


@login_required(login_url='homepage')
def mark_read(request, id=None):
    id = request.GET.get('id', None)
    obj = Feedback.objects.get(pk=id)
    obj.isRead = True
    obj.save()
    return render(request, 'manager.html', {})


def resetPass(request):
    if request.method == 'POST':
        changePassForm = ForgotPassForm(request.POST)
        if changePassForm.is_valid():
                email = changePassForm.cleaned_data['email']
                for user in User.objects.all():
                    if user.email == email:
                        newPass = generatePassword()
                        u = User.objects.get(email=email)
                        u.set_password(newPass)
                        u.save()
                        send_mail(
                        'You requested a one time password',
                        'Your new password is: ' + newPass + ', please change your password immediately',
                        'feedback@04lpsalesweb01.crowdstrike.sys',
                        [email],
                        fail_silently=False,
                        )
                        return redirect('homepage')
                
                messages.error(request, "Email does not exist")
                return redirect('homepage')
        
    changePassForm = ForgotPassForm()
    context = {"changePassForm":changePassForm}
    return render(request, 'resetPass.html', context)

def home(request):
    
    if request.method == 'POST':
        if 'login' in request.POST:
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    if user.is_superuser:
                        return redirect('manager/administrate/')
                    return redirect('manager/') #Not sure 
            else:
                messages.error(request, "Invalid username or password")
        elif 'pass' in request.POST:
            if request.method == 'POST':
                changePassForm = ForgotPassForm(request.POST)
                if changePassForm.is_valid():
                        email = changePassForm.cleaned_data['email']
                        for user in User.objects.all():
                            if user.email == email:
                                newPass = generatePassword()
                                u = User.objects.get(email=email)
                                u.set_password(newPass)
                                u.save()
                                send_mail(
                                'You requested a one time password',
                                'Your new password is: ' + newPass + ', please change your password immediately',
                                'feedback@04lpsalesweb01.crowdstrike.sys',
                                [email],
                                fail_silently=False,
                                )
                                return redirect('homepage')
                        
                        messages.error(request, "Email does not exist. OTP not sent")
                        return redirect('homepage')
    changePassForm = ForgotPassForm()
    form = AuthenticationForm()
    return render(request = request,
                  template_name = "index.html",
                  context={
                  "changePassForm":changePassForm,
                  "form":form
                  }
                 )


def index(request):
    if request.method == 'POST':
        F = CreateFeedbackForm(request.POST)
        if F.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                new_feedback = F.save()
                # Send email
                if new_feedback.manager.email != None:
                    send_mail(
                        'You have new feedback waiting for you',
                        'You recieved a new feedback item, log in to https://04lpsalesweb01.crowdstrike.sys/ to view',
                        'feedback@04lpsalesweb01.crowdstrike.sys',
                        [new_feedback.manager.email],
                        fail_silently=False,
                    )
                messages.info(request, f"Thank you for the feedback!")
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            
    form = CreateFeedbackForm()
    context = {
        'managers': User.objects.all(),
        'type_choice': Feedback.TYPE_CHOICES,
        'form': form
    }
    return render(request, 'list.html', context)


@login_required(login_url='homepage')
def manager(request, fb=None):
    context = {} 
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
def manager_delete(request, id=None):
    if request.method == "POST":
        try:
            user = User.objects.get(pk=id)
            user.delete()
        except:
            messages.info(request, f"Cannot Delete User")
        return redirect('adminPage')
    else:
        context = {}
        return render(request, 'admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='homepage')
def manager_update(request, id=None):
    user = User.objects.get(pk=id)
    user.save()
    if request.method == "POST":
        passForm = SetPasswordForm(user=user, data=request.POST)
        if passForm.is_valid():
            passForm.save()
            messages.info(request, f"Password Changed")
            return redirect('adminPage')
        form = UpdateUserForm(request.POST, instance=user)
        form.save()
        return redirect('adminPage')
    else:
        passForm = SetPasswordForm(user=user)
        form = UpdateUserForm(instance=user)
        context = {'form': form, 'passForm': passForm}
        return render(request, 'update_manager.html', context)

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

@login_required(login_url='homepage')
def current_manager_update(request):
    if request.method == "POST":
        form = UpdateCurrentUserForm(request.POST, instance=request.user)
        form.save()
        return redirect('manager')
    else:
        form = UpdateCurrentUserForm(instance=request.user)
        context = {'form': form}
        return render(request, 'update_current.html', context)


@login_required(login_url='homepage')
def changePass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('manager')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changePass.html', {
        'form': form
    })

def generatePassword():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(random.randint(8,15))))
    return result_str
