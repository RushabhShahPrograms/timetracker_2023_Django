import io
import os
from pydoc import doc
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView,View
from django.views.generic.edit import FormView,CreateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.decorators import *
import plotly.express as px
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from datetime import date, timedelta
from django.conf import settings
import plotly.graph_objs as go

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

@method_decorator([login_required(login_url="/user/login")],name='dispatch')
class AddProjectModulesView(CreateView):
    form_class = ProjectModulesForm
    model = Project_Module
    template_name = 'project/add_projects_modules.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form)
    
@method_decorator([login_required(login_url="/user/login")],name='dispatch')
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

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ModulesListView(ListView):
    paginate_by=5
    model = Project_Module
    template_name = 'project/modules_list.html'
    context_object_name = 'modules_list'
    
    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search = self.request.GET.get('search', None)
        queryset = super().get_queryset()
        
        if search:
            queryset = queryset.filter(Q(module_name__icontains=search) | Q(user__icontains=search))
        
        if sort_by == 'name':
            queryset = queryset.order_by('module_name')
        elif sort_by == 'start_date':
            queryset = queryset.order_by('module_start_date')
        elif sort_by == 'completion_date':
            queryset = queryset.order_by('module_completion_date')
        
        return queryset

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ModulesUpdateView(UpdateView):
    model = Project_Module
    form_class = ProjectModulesForm
    template_name = 'project/add_projects_modules.html'
    success_url = '/project/moduleslist/'

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ModulesDetailView(DetailView):
    model = Project_Module
    template_name = 'project/module_detail.html'
    context_object_name = 'modulesdetail'
    
    def get(self, request, *args, **kwargs):
        team = Project_Team.objects.filter(project_id=self.kwargs['pk'])
        return render(request, self.template_name, {'modulesdetail': self.get_object(),'team':team})
    
      
@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ModulesDeleteView(DeleteView):
    model = Project_Module
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/moduleslist/'

def send_reminder_mail():
    pending_modules = Project_Module.objects.filter(status__in=['Pending', 'In Progress'])
    for module in pending_modules:
        days_left = (module.module_completion_date - date.today()).days
        if days_left <= 3:
            subject = f'Reminder: Only 3 days left to complete {module.module_name}'
            message = f'Hi {module.user.username},\n\nJust a friendly reminder that you have only 3 days left to complete the module {module.module_name} assigned to you.\n\nThanks,\nThe Project Manager'
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[module.user.email],
                fail_silently=False,
            )

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class TaskListView(ListView):
    paginate_by=5
    model = Project_Task
    template_name = 'project/task_list.html'
    context_object_name = 'task_list'
    
    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search = self.request.GET.get('search', None)
        queryset = super().get_queryset()
        
        if search:
            queryset = queryset.filter(Q(task_title__icontains=search) | Q(priority__icontains=search))
        
        if sort_by == 'name':
            queryset = queryset.order_by('task_title')
        elif sort_by == 'priority':
            queryset = queryset.order_by('priority')
        elif sort_by == 'status':
            queryset = queryset.order_by('status')
        
        return queryset

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class TaskUpdateView(UpdateView):
    model = Project_Task
    form_class = ProjectTaskForm
    template_name = 'project/add_projects_task.html'
    success_url = '/project/taskslist/'

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class TaskDetailView(DetailView):
    model = Project_Task
    template_name = 'project/task_detail.html'
    context_object_name = 'tasksdetail'
    
    def get(self, request, *args, **kwargs):
        team = Project_Team.objects.filter(project_id=self.kwargs['pk'])
        return render(request, self.template_name, {'tasksdetail': self.get_object(),'team':team})
    
      
@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class TaskDeleteView(DeleteView):
    model = Project_Task
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/taskslist/'  


@method_decorator([login_required(login_url="/user/login"),developer_required],name='dispatch')
class UserProjectTeamListView(ListView):
    paginate_by=5
    model = Project_Team
    template_name = 'project/user_project_team_list.html'
    context_object_name = 'projectteam'
    
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
    
@method_decorator([login_required(login_url="/user/login"),developer_required],name='dispatch')
class UserTaskListView(ListView):

    def get(self,request,*args,**kwargs):
        usermodules = Project_Module.objects.filter(user__username=self.request.user.username)
        user_tasks = Project_Task.objects.filter(user__username=self.request.user.username)

        return render(request, 'project/user_task_list.html',
                      {
                        'usermodules':usermodules,
                        'user_tasks':user_tasks,
                      })


@method_decorator([login_required(login_url="/user/login"),developer_required],name='dispatch')
class DeveloperSubmitView(CreateView):
    form_class = DeveloperSubmitForm
    template_name = 'project/developer_submit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST, request.FILES)
        if form.is_valid():
            submit = form.save(commit=False)
            submit.submit_developer_name = request.user.username
            submit.save()
            form.send_email_to_manager()
            return redirect('developerpage')
        else:
            return render(request, self.template_name, {'form': form})

class ProjectModuleGanttView(DetailView):
    model = Project
    template_name = 'project/modules_chart_detail.html'

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
    

class TaskStartView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Project_Task, id=task_id, user=request.user)
        task.status = 'In Progress'
        task.start_time = timezone.now()
        task.save()
        return redirect('developerpage')

class TaskCompleteView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Project_Task, id=task_id, user=request.user)
        task.status = 'Completed'
        task.end_time = timezone.now()
        task.timer_duration = task.end_time - task.start_time
        task.save()
        return redirect('developerpage')

def start_module(request, pk):
    module = get_object_or_404(Project_Module, pk=pk, user=request.user)
    module.status = "In Progress"
    module.module_start_date = timezone.now()
    module.save()
    return redirect('developerpage')

def complete_module(request, pk):
    module = get_object_or_404(Project_Module, pk=pk, user=request.user)
    module.status = "Completed"
    module.module_completion_date = timezone.now()
    module.timer_duration = module.module_completion_date - module.module_start_date
    module.save()
    return redirect('developerpage')


from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf(request):
    template = get_template('project/pdf.html')
    projects = Project.objects.all()
    modules = Project_Module.objects.all()
    tasks = Project_Task.objects.all()
    context = {'projects': projects,
               'modules':modules,
               'tasks':tasks,}
    html = template.render(context)

    pdf_file = HttpResponse(content_type='application/pdf')
    pdf_file['Content-Disposition'] = 'attachment; filename="overall_report.pdf"'

    pisa.CreatePDF(html, dest=pdf_file)

    return pdf_file


import datetime

def generate_monthly_pdf(request):
    # Get the current month and year
    now = datetime.datetime.now()
    month = now.month
    year = now.year

    # Filter the data by the current month
    projects = Project.objects.filter(project_start_date__month=month, project_start_date__year=year)
    modules = Project_Module.objects.filter(module_start_date__month=month, module_start_date__year=year)
    tasks = Project_Task.objects.filter(start_time__month=month, start_time__year=year)

    # Render the PDF template with the filtered data
    template = get_template('project/monthlypdf.html')
    context = {'projects': projects,
               'modules': modules,
               'tasks': tasks}
    html = template.render(context)

    # Generate the PDF file and return it as an attachment
    pdf_file = HttpResponse(content_type='application/pdf')
    pdf_file['Content-Disposition'] = 'attachment; filename="monthly_report.pdf"'
    pisa.CreatePDF(html, dest=pdf_file)

    return pdf_file