"""feedbackApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url 
from django.urls import path
from mainApp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager/administrate/', adminPage, name="adminPage"),
    path('', home, name="homepage"),
    path('default/', index, name="default"),
    
    path('manager/', manager, name="manager"),
    path('manager/logout/', logout_request, name="logout"),
    path('add_manager', add_manager, name="add_manager"),
    path('m_delete/<int:id>/',manager_delete,name='manager_delete'),
    path('m_update/<int:id>/', manager_update,name='manager_update'),

    path('mr/<int:id>',mark_read_old,name="mark_fb_read"),
    url(r'^ajax/mark_read/$', mark_read, name='mark_read'),
    url(r'^ajax/get_feedback/$', get_feedback, name='get_feedback'),
    url(r'^ajax/get_feedbacks/$', get_feedbacks, name='get_feedbacks'),
    url(r'^ajax/delete_feedback/$', delete_feedback, name='delete_feedback'),
]