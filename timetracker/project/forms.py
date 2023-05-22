import django.forms as form
from django import forms
from .models import *
from user.models import User
from django.forms import DateTimeInput,DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import CheckboxSelectMultiple
from crispy_forms.bootstrap import PrependedText
from crispy_forms.layout import Submit, Layout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.template.defaultfilters import linebreaks

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
    user = form.ModelChoiceField(queryset=User.objects.filter(is_developer=True))
    module_start_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    module_completion_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = Project_Module
        fields = '__all__'

class ProjectTaskForm(form.ModelForm):

    start_time = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))

    user = form.ModelChoiceField(queryset=User.objects.filter(is_developer=True))
    class Meta:
        model = Project_Task
        fields = '__all__'

class ProjectTeamForm(form.ModelForm):
    # user = form.ModelChoiceField(queryset=User.objects.filter(is_developer=True))
    user = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_developer=True),
        widget=CheckboxSelectMultiple,
    )
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.layout = Layout(
        PrependedText('user', 'user'),
    )

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

    submit_developer_email = forms.EmailField(label='Developer Email', required=True)


    class Meta:
        model = Developer_Submit
        fields = '__all__'
        widgets = {
            'submit_manager_name': forms.TextInput(attrs={'class': 'form-control', 'editable': True}),
        }

    def __init__(self, user, *args, **kwargs):
        super(DeveloperSubmitForm, self).__init__(*args, **kwargs)
        self.fields['submit_developer_name'].initial = user.username
        self.fields['submit_developer_email'].initial = user.email
        manager = User.objects.filter(is_manager=True).first()
        self.fields['submit_manager_name'].initial = manager.username
        self.fields['submit_submit_date'].initial = timezone.now()

    def send_email_to_manager(self):
        subject = 'Developer Submission'
        message = render_to_string('project/developer_submission_email.html', {'form': self})
        plain_message = strip_tags(message)
        manager = User.objects.filter(is_manager=True).first()
        to_email = manager.email
        sender_email = self.cleaned_data.get('submit_developer_email')

        # Apply linebreaks filter to the message content
        message_with_linebreaks = linebreaks(plain_message)

        # Create EmailMessage object
        email = EmailMessage(subject, message_with_linebreaks, sender_email, [to_email])
        email.content_subtype = 'html'  # Set content type as HTML

        # Attach submit_file if present
        submit_file = self.cleaned_data.get('submit_file')
        if submit_file:
            file_name = submit_file.name
            file_content = submit_file.read()
            email.attach(file_name, file_content)

        # Attach submit_screenshot if present
        submit_screenshot = self.cleaned_data.get('submit_screenshots')
        if submit_screenshot:
            screenshot_name = submit_screenshot.name
            screenshot_content = submit_screenshot.read()
            email.attach(screenshot_name, screenshot_content)

        # Send the email
        email.send(fail_silently=False)