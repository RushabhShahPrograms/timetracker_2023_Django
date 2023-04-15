import django.forms as form
from django import forms
from .models import *
from user.models import User

class AddProjectsForm(form.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        
class ProjectModulesForm(form.ModelForm):
    user = form.ModelChoiceField(queryset=User.objects.filter(is_developer=True))
    class Meta:
        model = Project_Module
        fields = '__all__'

class ProjectTaskForm(form.ModelForm):
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