from . import views
from django.urls import path,include
from .views import *

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
]