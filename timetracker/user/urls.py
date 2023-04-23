from . import views
from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
 #registerURLS
 path('adminregister/',AdminRegisterView.as_view(),name='adminregister'),
 path('managerregister/',ManagerRegisterView.as_view(),name='managerregister'),
 path('developerregister/',DeveloperRegisterView.as_view(),name='developerregister'),

 #loginlogoutURLS
 path('login/',UserLoginView.as_view(),name='login'),
 path('logout/',views.logoutUser,name='logout'),
 
 #sendmailURLS
 path('sendmail/',views.sendMail,name='sendmail'),
 
 #dashboardpageURLS
 path('managerpage/',ManagerPage.as_view(),name="managerpage"),
 path('developerpage/',DeveloperPage.as_view(),name="developerpage"),
 path('adminpage/',AdminPage.as_view(),name="adminpage"),
 
 #passwordresetURLS
 path('resetpassword/',
      auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"),
      name='reset_password'),
 path('resetpasswordsent/',
      auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_sent.html"),
      name='password_reset_done'),
 path('reset/<uidb64>/<token>/',
      auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_form.html"),
      name='password_reset_confirm'),
 path('resetpasswordcomplete/',
      auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_done.html"),
      name='password_reset_complete'),

# userprofileURLS
path('userprofile/<int:pk>/',ShowProfilePageView.as_view(),name="userprofile"),
path('edituserprofile/<int:pk>/',EditProfilePageView.as_view(),name="edituserprofile"),

#scheduleURLS
path('addschedule/',ScheduleCreateView.as_view(),name="addschedule"),
path('schedulelist/',ScheduleListView.as_view(),name="schedulelist"),
path('scheduledelete/<int:pk>',ScheduleDeleteView.as_view(),name='scheduledelete'),
path('scheduleupdate/<int:pk>',ScheduleUpdateView.as_view(),name='scheduleupdate'),
path('scheduledetail/<int:pk>',ScheduleDetailView.as_view(),name='scheduledetail'),

path('get-meeting-details/<int:meeting_id>/', get_meeting_details, name='get_meeting_details'),

# other URL mappings
path('<int:task_id>/start/', TaskStartView.as_view(), name='task_start'),
path('start_module/<int:pk>/', views.start_module, name='start_module'),
path('<int:task_id>/complete/', TaskStartView.as_view(), name='task_complete'),
path('complete_module/<int:pk>/', views.start_module, name='complete_module'),

]