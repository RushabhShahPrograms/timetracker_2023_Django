import django.forms as form
from django import forms
from .models import *
from user.models import User
from django.forms import DateTimeInput,DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AddProjectsForm(form.ModelForm):

    project_start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    project_completion_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Project
        fields = '__all__'
        
class ProjectModulesForm(form.ModelForm):

    module_start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    module_completion_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    user = form.ModelChoiceField(queryset=User.objects.filter(is_developer=True))
    class Meta:
        model = Project_Module
        fields = '__all__'

class ProjectTaskForm(form.ModelForm):

    start_time = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    end_time = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    user = form.ModelChoiceField(queryset=User.objects.filter(is_developer=True))
    class Meta:
        model = Project_Task
        fields = '__all__'

class ProjectTeamForm(form.ModelForm):
    user = form.ModelChoiceField(queryset=User.objects.filter(is_developer=True))
    class Meta:
        model = Project_Team
        fields ='__all__'

class UserTaskForm(form.ModelForm):
    class Meta:
        model = User_Task
        fields = '__all__' 


class DeveloperSubmitForm(forms.ModelForm):

    submit_submit_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Developer_Submit
        fields = '__all__'
        widgets = {
            'submit_manager_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
        }

    def __init__(self, user, *args, **kwargs):
        super(DeveloperSubmitForm, self).__init__(*args, **kwargs)
        self.fields['submit_developer_name'].initial = user.username
        self.fields['task'].queryset = Project_Task.objects.filter(user=user)
        self.fields['module'].queryset = Project_Module.objects.filter(user=user)
        self.fields['project'].queryset = Project_Team.objects.filter(user=user)
        manager = User.objects.filter(is_manager=True).first()
        self.fields['submit_manager_name'].initial = manager.username