from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
import requests
from .models import User,Schedule,WorkTime
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView,ListView,DetailView
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from project.views import *
from user.decorators import *
from django.utils.decorators import method_decorator
import plotly.graph_objs as go
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.db.models.functions import Coalesce
from plotly.offline import plot
from django.db.models import Q
from django.views import View
from django.core.mail import EmailMessage
import calendar
from calendar import HTMLCalendar
from datetime import date, datetime
from django.db.models import Sum

class AdminRegisterView(CreateView):
    model = User
    form_class = AdminRegisterForm
    template_name = 'user/admin_register.html'
    #success_url = "/product/adminpage/"
    
    def form_valid(self,form):
        email = form.cleaned_data.get('email')
        user=form.save()
        recipient_list = [email]
        subject = "welcome to django"
        message = "Say hello to Django!! You are Admin now"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        #print(email)
        login(self.request,user)
        return redirect('/user/adminpage/')


class ManagerRegisterView(CreateView):
    model = User
    form_class = ManagerRegisterForm
    template_name = 'user/manager_register.html'
    #success_url = "/product/managerpage/"
    
    def form_valid(self,form):
        email = form.cleaned_data.get('email')
        user=form.save()
        recipient_list = [email]
        subject = "welcome to django"
        message = "Say hello to Django!! You are Manager now"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        #print(email)
        login(self.request,user)
        return redirect('/user/managerpage/')

        

class DeveloperRegisterView(CreateView):
    model = User
    form_class = DeveloperRegistrationForm
    template_name = 'user/developer_register.html'
    #success_url = "/product/developerpage/"    

        
    def form_valid(self,form):
        email = form.cleaned_data.get('email')
        user=form.save()
        recipient_list = [email]
        subject = "welcome to django"
        message = "Say hello to Django!! You are Developer now"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        #print(email)
        login(self.request,user)
        return redirect('/user/developerpage') 

    

class UserLoginView(LoginView):
     template_name = 'user/login.html'
    
     def get_redirect_url(self):
         if self.request.user.is_authenticated:
             if self.request.user.is_manager:
                 return '/user/managerpage/'
             else:
                 return '/user/developerpage/'
            
def sendMail(request):
    subject = "welcome to django"
    message = "hello django"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [User.objects.values_list('email', flat=True)]
    send_mail = (subject,message,email_from,recipient_list)

    return HttpResponse("mail sent")



def logoutUser(request):
    logout(request)
    return redirect('index')


@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class AdminPage(TemplateView):
    template_name="user/admin_page.html"

class MyHTMLCalendar(HTMLCalendar):
    def __init__(self, year=None):
        self.year = year
        super().__init__()

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year = theyear
        v = []
        a = v.append
        a('<table class="calendar">\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a(self.formatweekheader())
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
        a('</table>\n')
        return ''.join(v)

    def formatday(self, day, weekday):
        """
        Return a formatted day cell with given content.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="day">%d</td>' % day

# @method_decorator(login_required(login_url='/user/login'), name='dispatch')
@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ManagerPage(ListView):
    template_name="user/manager_page.html"

    def get(self,request,*args,**kwargs):
        project = Project.objects.all().values()
        InProgressProject = Project.objects.filter(status="In Progress")
        team = Project_Team.objects.all().values()
        module = Project_Module.objects.all().values()
        pendingmodule = Project_Module.objects.filter(status="Pending")
        InProgressmodule = Project_Module.objects.filter(status="In Progress")
        task = Project_Task.objects.all().values()
        pendingtask = Project_Task.objects.filter(status="Pending")
        InProgresstask = Project_Task.objects.filter(status="In Progress")
        schedules = Schedule.objects.all()
        developersubmit = Developer_Submit.objects.all().order_by(F('submit_submit_date').desc(nulls_last=True))[:5]

        # Bar Chart
        completedproject = Project.objects.filter(status="Completed")
        pendingproject = Project.objects.filter(status="Pending")
        chs = Project.objects.annotate(month=ExtractMonth('project_start_date')) \
                                  .values('month') \
                                  .annotate(total_projects=Count('id')) \
                                  .order_by('month')
        

        # Pie Chart
        completed_projects = Project.objects.filter(status="Completed")
        pending_projects = Project.objects.filter(status="Pending")
        cancelled_projects = Project.objects.filter(status="Cancelled")
        total_projects = Project.objects.aggregate(
            completed=Coalesce(Count('id', filter=Q(status="Completed")), 0),
            pending=Coalesce(Count('id', filter=Q(status="Pending")), 0),
            cancelled=Coalesce(Count('id', filter=Q(status="Cancelled")), 0)
        )

        
        labels = ['Completed', 'Pending', 'Cancelled']
        values = [total_projects['completed'], total_projects['pending'], total_projects['cancelled']]
        colors = ['#B2A4FF', '#57C5B6', '#D864A9']

        trace = go.Pie(labels=labels, values=values,
                       hoverinfo='label+percent', textinfo='value',
                       textfont=dict(size=20),
                       marker=dict(colors=colors, line=dict(color='#000000', width=1)))

        data = [trace]
        layout = go.Layout(title='Total Projects',
                           margin=dict(l=50, r=50, b=100, t=100, pad=4),
                           autosize=True,)

        chart = plot(go.Figure(data=data, layout=layout), output_type='div')

        #Calendar
        # Get the year and month from the request parameters
        year = int(self.request.GET.get('year', datetime.now().year))
        month = self.request.GET.get('month', datetime.now().strftime('%B'))

        # Add the calendar data to the context
        month_number = list(calendar.month_name).index(month.capitalize())
        cal = MyHTMLCalendar(year=year).formatmonth(year, month_number)
        
        # Highlight the meeting date in the calendar
        schedules = Schedule.objects.filter(schedule_meeting_date__year=year, schedule_meeting_date__month=month_number).order_by(F('schedule_meeting_date').desc(nulls_last=True))
        for schedule in schedules:
            day = schedule.schedule_meeting_date.day
            html = f'<a class="calendar-meeting-link" data-toggle="modal" data-target="#meeting-details-modal" data-meeting-id="{schedule.pk}">{day}</a>'
            cal = cal.replace(f'>{day}<', f' style="background-color: skyblue">{html}<')

        today = datetime.now()
        if today.year == year and today.month == month_number:
            day = today.day
            cal = cal.replace(f'>{day}<', f' style="background-color: yellow">{day}<')

        # Add Indian holidays with green color
        holidays = []
        response = requests.get(f'https://calendarific.com/api/v2/holidays?api_key=<your_api_key>&country=IN&year={year}')
        if response.status_code == 200:
            data = response.json()
            for holiday in data['response']['holidays']:
                holiday_date = datetime.strptime(holiday['date']['iso'], '%Y-%m-%d').date()
                holiday_name = holiday['name']
                holidays.append({'date': holiday_date, 'name': holiday_name})

        for holiday in holidays:
            day = holiday['date'].day
            html = f'<span class="calendar-holiday">{holiday["name"]}</span>'
            cal = cal.replace(f'>{day}<', f' style="background-color: green">{html}<')

        return render(request, 'user/manager_page.html',
                      {'projects':project,
                       'teams':team,
                       'completedprojects':completedproject,
                       'pendingprojects':pendingproject,
                       'pendingmodule':pendingmodule,
                       'pendingtask':pendingtask,
                       'modules':module,
                       'tasks':task,
                       'chs':chs,
                       'completed_projects': completed_projects,
                       'pending_projects': pending_projects,
                       'cancelled_projects': cancelled_projects,
                       'chart': chart,
                       'schedules':schedules,
                       'developersubmit':developersubmit,
                       'year': year,
                        'month': month,
                        'month_number': month_number,
                        'cal': cal,
                        'current_year': datetime.now().year,
                        'time': datetime.now().strftime('%I:%M:%S %p'),
                        'schedules':schedules,
                        'InProgressproject':InProgressProject,
                        'InProgressmodule':InProgressmodule,
                        'InProgresstask':InProgresstask,
                       })


def notifications(request):
    developersubmit = Developer_Submit.objects.order_by('-submit_date')[:6]
    if developersubmit:
        request.session['new_notifications'] = True
    else:
        request.session['new_notifications'] = False
    return render(request, 'notifications.html', {'developersubmit': developersubmit, 'new_notifications': request.session.get('new_notifications', False)})



from django.db.models import F
@method_decorator([login_required(login_url="/user/login"),developer_required],name='dispatch')
class DeveloperPage(ListView):

    def get(self,request,*args,**kwargs):
        modules = Project_Module.objects.filter(user__username=self.request.user.username)
        notifymodules = Project_Module.objects.filter(user__username=self.request.user.username).order_by(F('module_start_date'))[:1]
        projects = Project_Team.objects.filter(user__username=self.request.user.username)
        notifyprojects = Project_Team.objects.filter(user__username=self.request.user.username)[:1]
        tasks = Project_Task.objects.filter(user__username=self.request.user.username)
        notifytasks = Project_Task.objects.filter(user__username=self.request.user.username).order_by(F('end_time'))[:1]
        meetings = Schedule.objects.filter(users__in=[self.request.user]).order_by(F('schedule_meeting_date').desc(nulls_last=True))[:6]
        notifymeetings = Schedule.objects.filter(users__in=[self.request.user]).order_by(F('schedule_meeting_date').desc(nulls_last=True))[:1]
        # user_timers = Timer.objects.filter(user=request.user)

        #Calendar
        # Get the year and month from the request parameters
        year = int(self.request.GET.get('year', datetime.now().year))
        month = self.request.GET.get('month', datetime.now().strftime('%B'))

        # Add the calendar data to the context
        month_number = list(calendar.month_name).index(month.capitalize())
        cal = MyHTMLCalendar(year=year).formatmonth(year, month_number)
        
        # Highlight the meeting date and current date in the calendar
        schedules = Schedule.objects.filter(users__username=self.request.user.username,schedule_meeting_date__year=year, schedule_meeting_date__month=month_number).order_by(F('schedule_meeting_date').desc(nulls_last=True))
        for schedule in schedules:
            day = schedule.schedule_meeting_date.day
            cal = cal.replace(f'>{day}<', f' style="background-color: skyblue">{day}<')

        today = datetime.now()
        if today.year == year and today.month == month_number:
            day = today.day
            cal = cal.replace(f'>{day}<', f' style="background-color: yellow">{day}<')

        # Add Indian holidays with green color
        holidays = []
        response = requests.get(f'https://calendarific.com/api/v2/holidays?api_key=<your_api_key>&country=IN&year={year}')
        if response.status_code == 200:
            data = response.json()
            for holiday in data['response']['holidays']:
                holiday_date = datetime.strptime(holiday['date']['iso'], '%Y-%m-%d').date()
                holiday_name = holiday['name']
                holidays.append({'date': holiday_date, 'name': holiday_name})

        for holiday in holidays:
            day = holiday['date'].day
            html = f'<span class="calendar-holiday">{holiday["name"]}</span>'
            cal = cal.replace(f'>{day}<', f' style="background-color: green">{html}<')

        #Task Line Chart
        # Query the data
        tasks = Project_Task.objects.filter(user=request.user, status='Completed')
        task_titles = [task.task_title for task in tasks]
        timer_durations = [task.timer_duration.total_seconds() / 60 for task in tasks] # convert to minutes

        # Create the Scatter trace
        trace = go.Scatter(
            x=task_titles,
            y=timer_durations,
            mode='lines+markers'
        )

        # Create the Layout object
        layout = go.Layout(
            title='Time Taken to Complete Tasks',
            xaxis=dict(title='Task Title'),
            yaxis=dict(title='Timer Duration (minutes)')
        )

        # Create the Figure object
        fig = go.Figure(data=[trace], layout=layout)

        # Generate the HTML code to display the chart
        chart_div = plot(fig, output_type='div', include_plotlyjs=False)

        #Module Line Chart
        # Query the data
        modules = Project_Module.objects.filter(user=request.user, status='Completed')
        module_titles = [module.module_name for module in modules]
        timer_durations = [module.timer_duration.total_seconds() / 60 for module in modules] # convert to minutes

        # Create the Scatter trace
        trace = go.Scatter(
            x=module_titles,
            y=timer_durations,
            mode='lines+markers'
        )

        # Create the Layout object
        layout = go.Layout(
            title='Time Taken to Complete Modules',
            xaxis=dict(title='Module Title'),
            yaxis=dict(title='Timer Duration (minutes)')
        )

        # Create the Figure object
        fig = go.Figure(data=[trace], layout=layout)

        # Generate the HTML code to display the chart
        module_chart_div = plot(fig, output_type='div', include_plotlyjs=False)

        # Total Hours
        user = request.user
        # calculate total hours for tasks
        task_hours = Project_Task.objects.filter(user=user, status='Completed').aggregate(Sum('timer_duration'))['timer_duration__sum'] or 0
        # calculate total hours for modules
        module_hours = Project_Module.objects.filter(user=user, status='Completed').aggregate(Sum('timer_duration'))['timer_duration__sum'] or 0
        # calculate total hours for all tasks and modules
        total_hours = (task_hours or 0) + (module_hours or 0)
        total_hours_formatted = '{:.2f}'.format(total_hours.total_seconds() / 3600)
        
        return render(request, 'user/developer_page.html',
                      {'modules':modules,
                       'projects':projects,
                       'tasks':tasks,
                       'meetings':meetings,
                       'notifymeetings':notifymeetings,
                       'notifytasks':notifytasks,
                       'notifymodules':notifymodules,
                       'notifyprojects':notifyprojects,
                       'year': year,
                        'month': month,
                        'month_number': month_number,
                        'cal': cal,
                        'current_year': datetime.now().year,
                        'time': datetime.now().strftime('%I:%M:%S %p'),
                        'schedules':schedules,
                        'chart_div':chart_div,
                        'module_chart_div':module_chart_div,
                        'total_hours_formatted':total_hours_formatted,
                       })

    template_name="user/developer_page.html"

# class TaskStartView(View):
#     def post(self, request, task_id):
#         task = get_object_or_404(Project_Task, id=task_id, user=request.user)
#         task.status = 'In Progress'
#         task.save()
#         TaskTime.objects.create(user=request.user, task=task, start_time=timezone.now())
#         return redirect('developerpage')

# class TaskCompleteView(View):
#     def post(self, request, task_id):
#         task = get_object_or_404(Project_Task, id=task_id, user=request.user)
#         task.status = 'Completed'
#         task.save()
#         task_time = TaskTime.objects.get(user=request.user, task=task, end_time=None)
#         task_time.end_time = timezone.now()
#         return redirect('developerpage')
    
# def dashboard(request):
#     task_times = TaskTime.objects.filter(user=request.user, end_time__isnull=False)
#     task_durations = [tt.duration for tt in task_times]

#     module_times = TaskTime.objects.filter(user=request.user, task__module__isnull=False, end_time__isnull=False)
#     module_durations = [tt.duration for tt in module_times]

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=[i+1 for i in range(len(task_durations))], y=[td.total_seconds()/3600 for td in task_durations], name='Task'))
#     fig.add_trace(go.Scatter(x=[i+1 for i in range(len(module_durations))], y=[md.total_seconds()/3600 for md in module_durations], name='Module'))
#     fig.update_layout(title='Task and Module Durations', xaxis_title='Task/Module', yaxis_title='Duration (hours)')

#     graph_div = fig.to_html(full_html=False)

#     return render(request, 'user/developerpage.html', {'graph_div': graph_div})

# def start_module(request, pk):
#     module = get_object_or_404(Project_Module, pk=pk, user=request.user)
#     module.status = "In Progress"
#     module.save()
#     return redirect('developerpage')

# def complete_module(request, pk):
#     module = get_object_or_404(Project_Module, pk=pk, user=request.user)
#     module.status = "Completed"
#     module.save()
#     return redirect('developerpage')

    
class ShowProfilePageView(DetailView):
    model = User
    template_name = 'user/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = User.objects.all()
        user = self.request.user
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User,id=self.kwargs['pk'])
        if user.is_developer:
            context['navbar_template'] = 'developer_navbar.html'
        else:
            context['navbar_template'] = 'manager_navbar.html'
        context["page_user"] = page_user
        context['skills'] = page_user.skills
        return context

class EditProfilePageView(UpdateView):
    model = User
    form_class = EditUserProfileForm
    template_name = "user/edit_user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_developer:
            context['navbar_template'] = 'developer_navbar.html'
        else:
            context['navbar_template'] = 'manager_navbar.html'
        return context
    
    def get_success_url(self):
        return reverse_lazy('userprofile', kwargs={'pk': self.kwargs['pk']})


from django.contrib.auth.mixins import LoginRequiredMixin
class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'user/schedule_form.html'
    success_url = '/user/schedulelist/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # Send email notifications to invited users
        for user in form.cleaned_data['users']:
            if user != self.request.user:
                user.schedules.add(form.instance)

                # Construct email message
                subject = f'New Meeting: {form.instance.schedule_title}'
                body = f'You have been invited to a new meeting: {form.instance.schedule_title}\n\nDescription: {form.instance.schedule_description}\n\nMeeting URL: {form.instance.schedule_meeting_url}\n\nMeeting Date and Time: {form.instance.schedule_meeting_date}'

                # Attach the document if it was uploaded
                if form.cleaned_data['schedule_documents']:
                    attachment = form.cleaned_data['schedule_documents']
                    email = EmailMessage(
                        subject=subject,
                        body=body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    email.attach(attachment.name, attachment.read(), attachment.content_type)
                    email.send(fail_silently=False)
                else:
                    # Send email without attachment
                    send_mail(
                        subject=subject,
                        message=body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )

        return response




class ScheduleListView(ListView):
    model = Schedule
    template_name = 'user/schedule_list.html'
    context_object_name = 'schedules'
    ordering = ['-schedule_meeting_date']

    def get_queryset(self):
        return super().get_queryset()


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'user/schedule_form.html'
    success_url = '/user/schedulelist/'

class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'user/schedule_detail.html'
    context_object_name = 'scheduledetail'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'scheduledetail': self.get_object()})

class ScheduleDeleteView(DeleteView):
    model = Schedule
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/user/schedulelist/'


def get_meeting_details(request, meeting_id):
    schedule = get_object_or_404(Schedule, pk=meeting_id)
    context = {'schedule': schedule}
    return render(request, 'user/meeting_details.html', context)