#User Models
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
genderChoice=(
   ("Male","male"),
   ("Female","female")
)
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    birthDate = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    landmark = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    salary = models.IntegerField(null=True,blank=True)
    gender = models.CharField(choices=genderChoice,max_length=50)
    email = models.EmailField(unique=True,null = False)
    username = models.CharField(max_length=100,unique=True,null=False)
    profile_pic = models.ImageField(upload_to='images/',null=True,blank=True)
    jobRole = models.CharField(max_length=50,null=True,blank=True)
    skills = models.CharField(max_length=500,blank=True,null=True)
    contact_number = PhoneNumberField(null=True, blank=True, unique=True)
    alternate_contact_number = PhoneNumberField(null=True, blank=True, unique=True)
    alternate_email = models.EmailField(blank=True,null=True)
    bio = RichTextField(null=True,blank=True)
    website_url = models.URLField(max_length=200,null=True,blank=True)
    linkedin_url = models.URLField(max_length=200,null=True,blank=True)
    twitter_url = models.URLField(max_length=200,null=True,blank=True)
    instagram_url = models.URLField(max_length=200,null=True,blank=True)
    facebook_url = models.URLField(max_length=200,null=True,blank=True)
    youtube_url = models.URLField(max_length=200,null=True,blank=True)
    github_url = models.URLField(max_length=200,null=True,blank=True)
    other_url = models.URLField(max_length=200,null=True,blank=True)

    def get_my_field_as_list(self):
        return [x.strip() for x in self.skills.split(',')]
    
    class Meta:
        db_table='user'
        #ordering = ('email',)

    def __str__(self):
        return self.username
    

class Schedule(models.Model):
    schedule_title = models.CharField(max_length=200)
    schedule_description = RichTextField(null=True,blank=True)
    schedule_documents = models.FileField(upload_to='schedule_documents/',null=True,blank=True)
    users = models.ManyToManyField(User, related_name='schedules')
    schedule_meeting_url = models.URLField()
    schedule_meeting_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    schedule_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='schedule'
    
    def __str__(self):
        return self.schedule_title