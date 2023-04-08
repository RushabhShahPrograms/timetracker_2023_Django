import django.forms as form
from .models import *

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

class DeveloperSubmitForm(form.ModelForm):
    class Meta:
        model = Developer_Submit
        fields = '__all__'
    
    def __init__(self, task_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if task_id:
            self.fields['task'].queryset = Project_Task.objects.filter(id=task_id)

    task = form.ModelChoiceField(queryset=Project_Task.objects.none(), widget=form.HiddenInput())