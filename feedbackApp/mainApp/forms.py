from django.forms import ModelForm
from mainApp.models import Feedback
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.encoding import smart_text



class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())

class CreateFeedbackForm(ModelForm):
    manager = UserFullnameChoiceField(queryset=User.objects.exclude(first_name__exact='', last_name__exact=''))
    class Meta:
        model = Feedback
        fields = ['manager', 'feedback', 'type_choice', 'salesforceOp', 'submitted_by']
        widgets = {
            'manager': forms.Select(
				attrs={
					'class': 'btn btn-lg btn-primary dropdown-toggle'
					}
				),
            'feedback': forms.Textarea(
				attrs={
					'class': 'form-control green-border-focus  form-control-sm'
					}
				),
                'type_choice': forms.Select(
				attrs={
					'class': ''
					}
				),
			}

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser')
        
        
class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name',  'email', 'is_superuser')    
        exclude = ('password','groups')