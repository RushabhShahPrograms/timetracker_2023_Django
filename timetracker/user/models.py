#User Models
from django.db import models
from django.contrib.auth.models import AbstractUser


# Don't consider this class

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


    class Meta:
        db_table='user'
        #ordering = ('email',)

    def __str__(self):
        return self.username