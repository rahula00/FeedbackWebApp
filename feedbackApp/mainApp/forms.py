from django.forms import ModelForm
from mainApp.models import Feedback
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class CreateFeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'manager', 'type_choice', 'submitted_by']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        
class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name',  'email', 'is_superuser')    
        exclude = ('password','groups')