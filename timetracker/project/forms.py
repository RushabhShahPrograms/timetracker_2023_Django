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