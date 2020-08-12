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

    class Meta:
        model = Feedback
        fields = ['manager', 'feedback', 'type_choice', 'salesforceOp', 'submitted_by']
        widgets = {
            'manager': forms.Select(
				attrs={
					'class': 'btn btn-outline-danger dropdown-toggle'
					}
				),
            'feedback': forms.Textarea(
				attrs={
					'class': 'form-control border-danger rounded',
                    'placeholder': 'Leave your feedback here',
                    'rows': '5',
					}
				),
                'type_choice': forms.Select(
				attrs={
					'class': 'btn btn-outline-danger dropdown-toggle'
					}
				),
                'salesforceOp': forms.Textarea(
				attrs={
					'class': 'form-control-sm border-danger rounded'
					}
				),
                'submitted_by': forms.Textarea(
				attrs={
					'class': 'form-control-sm border-danger rounded'
					}
				),
			}
    manager = UserFullnameChoiceField(queryset=User.objects.exclude(first_name__exact='', last_name__exact='').order_by('last_name'))
    manager.widget.attrs.update({'class': 'btn btn-outline-danger dropdown-toggle'})

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'password1', )
        
        
class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name',  'email', 'is_superuser')    
        exclude = ('password','groups')

class UpdateCurrentUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name',  'email')    
        exclude = ('password','groups')

