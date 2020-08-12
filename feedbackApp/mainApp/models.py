from django.db import models
from django.contrib.auth.models import User



# Create your models here.




class Feedback(models.Model):
	
	
	feedback = models.CharField(blank=False, max_length=500)
	salesforceOp = models.CharField(blank=True, max_length=100, null=True, default='N/A')
	#manager = models.ForeignKey(Managers, blank=True, null=True, on_delete=models.CASCADE)
	manager = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
	isRead = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	TYPE_CHOICES = [
        ('Sales', 'Sales'),
        ('Technical', 'Technical'),
        ('Coaching', 'Coaching'),
        ('Other', 'Other'),
    ]
	
	type_choice = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Other')
	submitted_by = models.CharField(max_length=60, default="Anonymous")