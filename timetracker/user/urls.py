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
]