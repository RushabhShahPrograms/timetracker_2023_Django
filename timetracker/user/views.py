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
import plotly.graph_objs as go
import plotly.offline
from plotly.subplots import make_subplots

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



def get_status_count(items, status):
    count = items.filter(status=status).count()
    return count
    

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
        month_names = [calendar.month_name[i['month']] for i in chs]

        # Create the bar trace with custom colors
        bar_trace = go.Bar(
            x=month_names,
            y=[x['total_projects'] for x in chs],
            name='Total Projects',
            marker=dict(
                color=['#FEFF86','#B0DAFF','#B9E9FC','#DAF5FF','#B2A4FF','#FFB4B4','#FFDEB4','#FDF7C3','#7286D3','#8EA7E9','#E5E0FF','#FFF2F2'],  # Set the colors here
                line=dict(color='#000000', width=1)
            )
        )

        # Create the data list with the bar trace
        data = [bar_trace]

        # Create the layout for the plot
        layout = go.Layout(
            title='Total Projects per Month',
            xaxis=dict(title='Month'),
            yaxis=dict(title='Total Projects')
        )

        # Create the Figure object with data and layout
        fig = go.Figure(data=data, layout=layout)

        # Generate the HTML code to display the chart
        bar_chart = plot(fig, output_type='div', include_plotlyjs=False)
        

        # Pie Chart
        completed_projects = Project.objects.filter(status="Completed")
        pending_projects = Project.objects.filter(status="Pending")
        cancelled_projects = Project.objects.filter(status="In Progress")
        total_projects = Project.objects.aggregate(
            completed=Coalesce(Count('id', filter=Q(status="Completed")), 0),
            pending=Coalesce(Count('id', filter=Q(status="Pending")), 0),
            inprogress=Coalesce(Count('id', filter=Q(status="In Progress")), 0)
        )

        
        labels = ['Completed', 'Pending', 'In Progress']
        values = [total_projects['completed'], total_projects['pending'], total_projects['inprogress']]
        colors = ['#B8B5FF', '#E4FBFF', '#7868E6']

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





        # Donut Chart for modules and tasks by status 
        # Count the number of modules by status
        module_counts = {
            'Pending': Project_Module.objects.filter(status='Pending').count(),
            'In Progress': Project_Module.objects.filter(status='In Progress').count(),
            'Completed': Project_Module.objects.filter(status='Completed').count(),
        }

        # Define the colors for each status
        colors = ['#FD841F', '#77D970', '#08D9D6']

        # Create the pie chart for modules by status
        module_data = go.Pie(labels=list(module_counts.keys()),
                            values=list(module_counts.values()),
                            hole=.4,
                            name="Modules",
                            marker=dict(colors=colors))

        # Set the layout for the pie chart
        layout = go.Layout(title="Modules by Status")

        # Set the data for the plot
        data = [module_data]

        # Create the figure for the plot
        fig = go.Figure(data=data, layout=layout)

        # Convert the figure to HTML
        module_plot = plotly.offline.plot(fig, output_type='div')


        # Count the number of tasks by status
        task_counts = {
            'Pending': Project_Task.objects.filter(status='Pending').count(),
            'In Progress': Project_Task.objects.filter(status='In Progress').count(),
            'Completed': Project_Task.objects.filter(status='Completed').count(),
        }

        # Define the colors for each status
        colors = ['#FD841F', '#77D970', '#08D9D6']

        # Create the pie chart for tasks by status
        task_data = go.Pie(labels=list(task_counts.keys()),
                        values=list(task_counts.values()),
                        hole=.4,
                        name="Tasks",
                        marker=dict(colors=colors))

        # Set the layout for the pie chart
        layout = go.Layout(title="Tasks by Status")

        # Set the data for the plot
        data = [task_data]

        # Create the figure for the plot
        fig = go.Figure(data=data, layout=layout)

        # Convert the figure to HTML
        task_plot = plotly.offline.plot(fig, output_type='div')

        # Combine the plots into a single HTML div
        chart_plot = '<div class="row"><div class="col-md-6">{}</div><div class="col-md-6">{}</div></div>'.format(module_plot, task_plot)





        #Line chart of Developer Time and Completion
        # Retrieve all developers
        developers = User.objects.filter(is_developer=True)

        # Create a dictionary to store developer data
        developer_data = {}

        # Iterate over each developer
        for developer in developers:
            # Query task data for the developer
            tasks = Project_Task.objects.filter(user=developer, status='Completed')
            task_timer_durations = [task.timer_duration.total_seconds() / 3600 for task in tasks]

            # Query module data for the developer
            modules = Project_Module.objects.filter(user=developer, status='Completed')
            module_timer_durations = [module.timer_duration.total_seconds() / 3600 for module in modules]

            # Calculate total time for the developer
            total_time = sum(task_timer_durations) + sum(module_timer_durations)

            # Add developer data to dictionary
            developer_data[developer.username] = total_time

        # Create a list of tuples from the dictionary, sorted by total time
        sorted_data = sorted(developer_data.items(), key=lambda x: x[1], reverse=True)

        # Create a list of traces for the developers
        data = []
        x_values = []
        y_values = []
        for developer, total_time in sorted_data:
            # Add the developer and total time to the x and y value lists
            x_values.append(developer)
            y_values.append(total_time)

        # Create a trace for the data
        trace = go.Scatter(
            x=x_values,
            y=y_values,
            name='Total Time Taken',
            line=dict(color='#62CDFF')
        )

        # Add the trace to the data list
        data.append(trace)

        # Create the layout for the plot
        layout = go.Layout(
            title='Total Time Taken by Developers',
            xaxis=dict(title='Developer'),
            yaxis=dict(title='Total Time (hours)')
        )

        # Create the Figure object with data and layout
        fig = go.Figure(data=data, layout=layout)

        # Generate the HTML code to display the chart
        chart_div = plot(fig, output_type='div', include_plotlyjs=False)


        # Retrieve all developers
        developers = User.objects.filter(is_developer=True)

        # Create a list of traces for each developer
        data = []
        for developer in developers:
            # Query task data for the developer
            tasks = Project_Task.objects.filter(user=developer, status='Completed')
            task_titles = [task.task_title for task in tasks]
            task_timer_durations = [task.timer_duration.total_seconds() / 3600 for task in tasks]

            # Query module data for the developer
            modules = Project_Module.objects.filter(user=developer, status='Completed')
            module_titles = [module.module_name for module in modules]
            module_timer_durations = [module.timer_duration.total_seconds() / 3600 for module in modules]

            # Create traces for the developer
            task_trace = go.Scatter(
                x=task_titles,
                y=task_timer_durations,
                mode='lines+markers',
                name=developer.username + ' - Tasks'
            )
            module_trace = go.Scatter(
                x=module_titles,
                y=module_timer_durations,
                mode='lines+markers',
                name=developer.username + ' - Modules',
            )

            # Add the traces to the data list
            data.append(task_trace)
            data.append(module_trace)

        # Create the layout for the plot
        layout = go.Layout(
            title='Track Duration to Complete Tasks and Modules by Developers',
            xaxis=dict(title='Task/Module Title'),
            yaxis=dict(title='Timer Duration (hours)')
        )

        # Create the Figure object with data and layout
        fig = go.Figure(data=data, layout=layout)

        # Generate the HTML code to display the chart
        chart_detail = plot(fig, output_type='div', include_plotlyjs=False)

        chart_developer = '<div class="row"><div class="col-md-4">{}</div><div class="col-md-8">{}</div></div>'.format(chart_div, chart_detail)




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
                        'chart_developer':chart_developer,
                        'chart_plot':chart_plot,
                        'bar_chart':bar_chart,
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
        tmodules = Project_Module.objects.filter(user__username=self.request.user.username)
        notifymodules = Project_Module.objects.filter(user__username=self.request.user.username).order_by(F('module_start_date'))[:1]
        projects = Project_Team.objects.filter(user__username=self.request.user.username)
        notifyprojects = Project_Team.objects.filter(user__username=self.request.user.username)[:1]
        ttasks = Project_Task.objects.filter(user__username=self.request.user.username)
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
        task_hours = Project_Task.objects.filter(user=user, status='Completed').aggregate(Sum('timer_duration'))['timer_duration__sum'] or timedelta()
        # calculate total hours for modules
        module_hours = Project_Module.objects.filter(user=user, status='Completed').aggregate(Sum('timer_duration'))['timer_duration__sum'] or timedelta()

        # calculate total hours for all tasks and modules
        total_hours = task_hours + module_hours
        # if total_hours:
        total_hours_formatted = '{:.2f}'.format(total_hours.total_seconds() / 3600)
        # else:
            # total_hours_formatted = '0.00'

        
        return render(request, 'user/developer_page.html',
                      {'modules':tmodules,
                       'projects':projects,
                       'tasks':ttasks,
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