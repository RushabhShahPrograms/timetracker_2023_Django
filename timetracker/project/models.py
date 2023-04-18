#Project Models
from datetime import timezone
from django.db import models
from django.urls import reverse
from user.models import User
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

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
    status = models.CharField(choices=status_choice,max_length=100)

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
    module_start_date = models.DateField()
    module_completion_date = models.DateField()
    user= models.ManyToManyField(User)
    status = models.CharField(choices=status_choice,max_length=100)

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
   task_util_minutes = models.IntegerField()
   status = models.CharField(choices=status_choice,max_length=100, default='Pending')
   start_time = models.DateField(null=True, blank=True)
   end_time = models.DateField(null=True, blank=True)

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
        return f"{self.submit_title} ({self.submit_developer_name}, {self.submit_submit_date.strftime('%Y-%m-%d %H:%M:%S')})"