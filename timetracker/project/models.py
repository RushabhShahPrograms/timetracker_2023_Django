#Project Models
from datetime import datetime, timezone
from django.conf import settings
from django.db import models
from django.urls import reverse
from user.models import User
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

# Status Class Don't consider this class as it is not used anywhere
status_choice = (("Completed","Completed"),
                 ("Pending","Pending"),
                 ("Cancelled","Cancelled"))
class Status(models.Model):
    status_name = models.CharField(choices=status_choice,max_length=100)

    class Meta:
        db_table='status'
   
    def __str__(self):
        return self.status_name


# Project Class
status_choice = (("Completed","Completed"),
                 ("Pending","Pending"),
                 ("In Progress","In Progress"),
                 ("Cancelled","Cancelled"))
class Project(models.Model):
    project_title = models.CharField(max_length=100)
    project_decription = RichTextField(null=True,blank=True)
    project_technology = models.CharField(max_length=100)
    project_estimated_hours = models.IntegerField()
    project_start_date = models.DateField()
    project_completion_date = models.DateField()
    project_file = models.FileField(upload_to='project_files/',null=True,blank=True)
    status = models.CharField(choices=status_choice,max_length=100, default='Pending')

    class Meta:
        db_table='project'
   
    def __str__ (self):
        return self.project_title


# Project Module Class
status_choice = (("Completed","Completed"),
                 ("Pending","Pending"),
                 ("In Progress","In Progress"),
                 ("Cancelled","Cancelled"))
class Project_Module(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100)
    module_description = RichTextField(null=True,blank=True)
    module_estimated_hours = models.IntegerField()
    timer_duration = models.DurationField(blank=True, null=True, default=0)
    module_start_date = models.DateTimeField()
    module_completion_date = models.DateTimeField()
    user= models.ForeignKey(User,on_delete=models.CASCADE,default=True)
    status = models.CharField(choices=status_choice,max_length=100,default='Pending')

    class Meta:
        db_table='project_module'

    def __str__(self):
        return self.module_name
   

# Project Task Class
status_choice = (("Completed","Completed"),
                 ("Pending","Pending"),
                 ("In Progress","In Progress"),
                 ("Cancelled","Cancelled"))
priorityChoice=(
   ('High','High Priority'),
   ('Less','Less Priority')
)
class Project_Task(models.Model):
   module = models.ForeignKey(Project_Module,on_delete=models.CASCADE)
   project = models.ForeignKey(Project,on_delete=models.CASCADE)
   task_title = models.CharField(max_length=100)
   task_description = RichTextField(null=True,blank=True)
   priority = models.CharField(choices=priorityChoice,max_length=30)
   user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
   task_estimated_hours = models.IntegerField()
   timer_duration = models.DurationField(blank=True, null=True,default=0)
   status = models.CharField(choices=status_choice,max_length=100, default='Pending')
   start_time = models.DateTimeField(null=True, blank=True)
   end_time = models.DateTimeField(null=True, blank=True)
   
   def save(self, *args, **kwargs):
        if self.status == 'Pending':
            delta = self.end_time - timezone.now()
            if delta.days == 3:
                subject = 'Reminder: Task pending for module completion'
                message = f'Hello {self.user.username},\n\nYou have a pending task "{self.task_title}" for the module "{self.module.module_name}". The task is scheduled to end in 3 days ({self.module.module_completion_date}). Please complete the task before the module ends.\n\nPriority: {self.priority}\n\nThank you.'
                send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[self.user.email], fail_silently=False)
        elif self.status == 'In Progress':
            delta = self.end_time - timezone.now()
            if delta.days == 3:
                subject = 'Reminder: Task in progress for module completion'
                message = f'Hello {self.user.username},\n\nYou have a task "{self.task_title}" in progress for the module "{self.module.module_name}". The module is scheduled to end in 3 days ({self.module.module_completion_date}). Please complete the task before the module ends.\n\nPriority: {self.priority}\n\nThank you.'
                send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[self.user.email], fail_silently=False)
        super().save(*args, **kwargs)

   class Meta:
       db_table='project_task'

   def __str__(self):
       return self.task_title
   

# Badge Class

badgeChoice=(
   ('InProgress','InProgress'),
   ('QuickFinisher','QuickFinisher'),
   ('LazyLoader','LazyLoader'),
   ('SilentUser','SilentUser')
)
class Badge(models.Model):
   badge = models.CharField(choices=badgeChoice,max_length=25)
   class Meta:
       db_table='badge'

   def __str__(self):
       return self.badge
   

# Project Team Class
status_choice = (("Completed","Completed"),
                 ("Pending","Pending"),
                 ("Cancelled","Cancelled"))
badgeChoice=(
   ('IN','InProgress'),
   ('QF','QuickFinisher'),
   ('LL','LazyLoader'),
   ('SU','SilentUser')
)
class Project_Team(models.Model):
    team_name = models.CharField(max_length=100)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    user= models.ManyToManyField(User)
    status = models.CharField(choices=status_choice,max_length=100)
    badge = models.CharField(choices=badgeChoice,max_length=25)

    class Meta:
        db_table = 'project_team'

    def __str__(self):
        return self.team_name
   

# User Task Class
status_choice = (("Completed","Completed"),
                 ("Pending","Pending"),
                 ("Cancelled","Cancelled"))
class User_Task(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   task = models.ForeignKey(Project_Task,on_delete=models.CASCADE)
   status = models.CharField(choices=status_choice,max_length=100)
   user_totalutil_minutes = models.IntegerField()

   class Meta:
       db_table='user_task'

   def __str__(self):
       return self.user_id


# Task Badge Class
   
class Task_Badge(models.Model):
    badge = models.ForeignKey(Badge,on_delete=models.CASCADE)
    task = models.ForeignKey(Project_Task,on_delete=models.CASCADE)
    
    class Meta:
       db_table='task_badge'
    
    def __str__(self):
       return self.badge
    
# Developer Submission Class
status_choice = (("Completed","Completed"),
                 ("In Progress","In Progress"),
                 ("Pending","Pending"),
                 ("Cancelled","Cancelled"))
class Developer_Submit(models.Model):
    task = models.ForeignKey(Project_Task, on_delete=models.CASCADE,null=True,blank=True)
    module = models.ForeignKey(Project_Module, on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    submit_title = models.CharField(max_length=200)
    submit_description = RichTextField(null=True,blank=True)
    code_snippets = RichTextField(null=True,blank=True)
    submit_screenshots = models.ImageField(upload_to='developer_task_screenshots/', blank=True, null=True)
    submit_file = models.FileField(upload_to='developer_task_files/',blank=True,null=True)
    status = models.CharField(choices=status_choice,max_length=50, default='In Progress')
    submit_time_spent = models.DurationField(blank=True, null=True)
    submit_submit_date = models.DateTimeField(auto_now_add=True)
    submit_developer_name = models.CharField(max_length=100)
    submit_manager_name = models.CharField(max_length=100)
    comments = RichTextField(null=True,blank=True)
    submit_url = models.URLField(blank=True, null=True)

    class Meta:
       db_table='developer_submit'

    def __str__(self):
        return self.submit_title
    
class TaskTimer(models.Model):
    task = models.ForeignKey(Project_Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_paused = models.BooleanField(default=False)
    pause_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'TaskTimer'
    
    def __str__(self):
        return self.start_time
    
class TaskTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Project_Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()

    class Meta:
        db_table = 'TaskTime'

    def save(self, *args, **kwargs):
        if self.start_time is not None and self.end_time is not None:
            self.duration = self.end_time - self.start_time
        super(TaskTime, self).save(*args, **kwargs)