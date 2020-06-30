from django.db import models

# Create your models here.
class Managers(models.Model):
	first_name = models.CharField(blank=False, max_length=40)
	last_name = models.CharField(blank=False, max_length=40)
	email = models.CharField(blank=False, max_length=90)
	password = models.CharField(max_length=100, default="crowdstrike")
	created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
	feedback = models.CharField(blank=False, max_length=2000)
	manager = models.ForeignKey(Managers, blank=True, null=True, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

