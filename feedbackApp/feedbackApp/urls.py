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
    path('delete/<int:id>/',feedback_delete,name='fb_delete'),
    path('mr/<int:id>',mark_read,name="mark_fb_read")
]