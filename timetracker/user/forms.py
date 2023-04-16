from django import forms
import django.forms as form
from django.contrib.auth.forms import *
from django.db import transaction
from .models import User,Schedule
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


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
    
from django.forms.widgets import SelectMultiple

class ScheduleForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_developer=True),
        widget=SelectMultiple(attrs={'class': 'chosen-select'})
    )

    schedule_meeting_date = forms.DateTimeField(widget=DateTimePickerInput(format='%Y/%m/%d %H:%M:%S'))


    class Meta:
        model = Schedule
        fields = '__all__'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user