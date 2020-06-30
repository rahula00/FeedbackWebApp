from django.contrib import admin

# Register your models here.
from .models import Managers, Feedback

admin.site.register(Managers)
admin.site.register(Feedback)