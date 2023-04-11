from django import forms
import django.forms as form
from django.contrib.auth.forms import *
from django.db import transaction
from .models import User


class AdminRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','gender','birthDate','salary')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        return user    

class ManagerRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','gender','birthDate','salary')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        return user    


class DeveloperRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','gender','birthDate','salary')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.save()
        return user
    

class EditUserProfileForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user
    

from schedule.models import Event
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start', 'end', 'description']