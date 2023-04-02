#Project Models
from django.db import models
from user.models import User



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
                 ("Cancelled","Cancelled"))
class Project(models.Model):
    project_title = models.CharField(max_length=100)
    project_decription = models.TextField()
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
                 ("Cancelled","Cancelled"))
class Project_Module(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100)
    module_description = models.TextField()
    module_estimated_hours = models.IntegerField()
    module_start_date = models.DateField()
    module_completion_date = models.DateField()
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(choices=status_choice,max_length=100)

    class Meta:
        db_table='project_module'

    def __str__(self):
        return self.module_name
   

# Project Task Class
status_choice = (("Completed","Completed"),
                 ("Pending","Pending"),
                 ("Cancelled","Cancelled"))
priorityChoice=(
   ('High','High Priority'),
   ('Less','Less Priority')
)
class Project_Task(models.Model):
   module = models.ForeignKey(Project_Module,on_delete=models.CASCADE)
   project = models.ForeignKey(Project,on_delete=models.CASCADE)
   task_title = models.CharField(max_length=100)
   task_description = models.TextField()
   priority = models.CharField(choices=priorityChoice,max_length=30)
   user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
   task_estimated_hours = models.IntegerField()
   task_util_minutes = models.IntegerField()
   status = models.CharField(choices=status_choice,max_length=100)

   class Meta:
       db_table='project_task'

   def __str__(self):
       return self.task_title
   

# Badge Class

badgeChoice=(
   ('IN','InProgress'),
   ('QF','QuickFinisher'),
   ('LL','LazyLoader'),
   ('SU','SilentUser')
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
    user= models.ForeignKey(User,on_delete=models.CASCADE)
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