from django.forms import ModelForm
from mainApp.models import Feedback


class CreateFeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'manager', 'type_choice', 'submitted_by']
    