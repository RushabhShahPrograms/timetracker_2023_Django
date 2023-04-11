from . import views
from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views
# from schedule.views import CreateEventView, CalendarView, EditEventView, DeleteEventView

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

#schedularURLS
# path('calendar/', CalendarView.as_view(), name='calendar_home'),
# path('event/create/', CreateEventView.as_view(), name='calendar_create_event'),
# path('event/update/<int:pk>/', EditEventView.as_view(), name='edit_event'),
# path('event/delete/<int:pk>/', DeleteEventView.as_view(), name='delete_event'),

path('calendar/', CalendarView.as_view(), name='calendar_home'),
path('event/create/', EventCreateView.as_view(), name='calendar_create_event'),
]