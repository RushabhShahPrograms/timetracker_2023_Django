from django import forms
import django.forms as form
from django.contrib.auth.forms import *
from django.db import transaction
from .models import User,Schedule
from django import forms
from django.forms import DateTimeInput,DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AdminRegisterForm(UserCreationForm):

    birthDate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    
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

    birthDate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

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

    birthDate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

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

    birthDate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))


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

    schedule_meeting_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))


    class Meta:
        model = Schedule
        fields = '__all__'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        return user