from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView,View
from django.views.generic.edit import FormView,CreateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.decorators import *
from plotly.offline import plot
import plotly.graph_objs as go
from django.shortcuts import render, get_object_or_404
import plotly.express as px
from django.core.paginator import Paginator
from django.db.models import Q

class IndexView(TemplateView):
    template_name = "project/index.html"


@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectsView(CreateView):
    form_class = AddProjectsForm
    model = Project
    template_name = 'project/add_projects.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form)

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectModulesView(CreateView):
    form_class = ProjectModulesForm
    model = Project_Module
    template_name = 'project/add_projects_modules.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form)
    
@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectTaskView(CreateView):
    form_class = ProjectTaskForm
    model = Project_Task
    template_name = 'project/add_projects_task.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form) 

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectTeamView(CreateView):
    form_class = ProjectTeamForm
    model = Project_Team
    template_name = 'project/add_projects_team.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form)

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class UserTaskView(CreateView):
    form_class = UserTaskForm
    model = User_Task
    template_name = 'project/add_user_task.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form) 


@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectListView(ListView):
    paginate_by=5
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'project_list'
    
    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search = self.request.GET.get('search', None)
        queryset = super().get_queryset()
        
        if search:
            queryset = queryset.filter(Q(project_title__icontains=search) | Q(project_technology__icontains=search))
        
        if sort_by == 'name':
            queryset = queryset.order_by('project_title')
        elif sort_by == 'start_date':
            queryset = queryset.order_by('project_start_date')
        elif sort_by == 'completion_date':
            queryset = queryset.order_by('project_completion_date')
        
        return queryset

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = AddProjectsForm
    template_name = 'project/add_projects.html'
    success_url = '/project/projectlist/'

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'projectdetail'
    
    def get(self, request, *args, **kwargs):
        team = Project_Team.objects.filter(project_id=self.kwargs['pk'])
        return render(request, self.template_name, {'projectdetail': self.get_object(),'team':team})
    
      
@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/projectlist/'    


@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class TaskListView(ListView):
    paginate_by=5
    model = Project_Team
    template_name = 'project/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search = self.request.GET.get('search', None)
        queryset = super().get_queryset().filter(user__username=self.request.user.username)
        
        if search:
            queryset = queryset.filter(Q(project__icontains=search) | Q(team_name__icontains=search) | Q(badge__icontains=search))
        
        if sort_by == 'team_name':
            queryset = queryset.order_by('team_name')
        elif sort_by == 'project':
            queryset = queryset.order_by('project')
        
        return queryset

class ProjectModuleGanttView(DetailView):
    model = Project
    template_name = 'project/modules_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        modules = project.project_module_set.all()

        if modules:
            df = []
            for module in modules:
                df.append({
                    'Task': module.module_name,
                    'Start': module.module_start_date,
                    'Finish': module.module_completion_date,
                    'Developer': module.user.username if module.user else '',
                })
            fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Developer")
            chart_div = fig.to_html(full_html=False)
            context['chart_div'] = chart_div
            context['modules'] = modules
        else:
            context['chart_div'] = ''
            context['modules'] = []

        return context