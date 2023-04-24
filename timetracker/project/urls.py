from django.urls import path,include
from .views import *
from . import views

urlpatterns = [
 path('addprojects/',AddProjectsView.as_view(),name="addprojects"),
 path('addprojectsmodules/',AddProjectModulesView.as_view(),name="addprojectsmodules"),
 path('addprojectstask/',AddProjectTaskView.as_view(),name="addprojectstask"),
 path('addprojectsteam/',AddProjectTeamView.as_view(),name="addprojectsteam"),
 path('addusertask/',UserTaskView.as_view(),name="addusertask"),
 path('teamlist/', UserProjectTeamListView.as_view(), name='teamlist'),
 path('usertasklist/',UserTaskListView.as_view(),name='usertasklist'),
 path('projectlist/',ProjectListView.as_view(),name="projectlist"),
 path('projectdelete/<int:pk>',ProjectDeleteView.as_view(),name='projectdelete'),
 path('projectupdate/<int:pk>',ProjectUpdateView.as_view(),name='projectupdate'),
 path('projectdetail/<int:pk>',ProjectDetailView.as_view(),name='projectdetail'),
 path('modules/<int:pk>',ProjectModuleGanttView.as_view(), name='modules'),
 path('moduleslist/',ModulesListView.as_view(),name="moduleslist"),
 path('modulesdelete/<int:pk>',ModulesDeleteView.as_view(),name='modulesdelete'),
 path('modulesupdate/<int:pk>',ModulesUpdateView.as_view(),name='modulesupdate'),
 path('modulesdetail/<int:pk>',ModulesDetailView.as_view(),name='modulesdetail'),
 path('taskslist/',TaskListView.as_view(),name="taskslist"),
 path('tasksdelete/<int:pk>',TaskDeleteView.as_view(),name='tasksdelete'),
 path('tasksupdate/<int:pk>',TaskUpdateView.as_view(),name='tasksupdate'),
 path('tasksdetail/<int:pk>',TaskDetailView.as_view(),name='tasksdetail'),

 path('developersubmit/',DeveloperSubmitView.as_view(),name='developersubmit'),
 path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
 path('generate-monthly-pdf/', views.generate_monthly_pdf, name='generate-monthly-pdf'),
]