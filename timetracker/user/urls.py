from . import views
from django.urls import path,include
from .views import *
#from django.contrib.auth.views import LogoutView


urlpatterns = [
 
 path('adminregister/',AdminRegisterView.as_view(),name='adminregister'),
 path('managerregister/',ManagerRegisterView.as_view(),name='managerregister'),
 path('developerregister/',DeveloperRegisterView.as_view(),name='developerregister'),
 path('login/',UserLoginView.as_view(),name='login'),
 path('logout/',views.logoutUser,name='logout'),
 path('sendmail/',views.sendMail,name='sendmail'),
 path('managerpage/',ManagerPage.as_view(),name="managerpage"),
 path('developerpage/',DeveloperPage.as_view(),name="developerpage"),
 path('adminpage/',AdminPage.as_view(),name="adminpage"),
 path('userprofile/',UserProfileView.as_view(),name="userprofile"),
 path('userprofileupdate/<int:pk>',UserProfileUpdateView.as_view(),name="userprofileupdate"),
 
]