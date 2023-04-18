from django.contrib import admin
from .models import *
from django.utils.html import format_html

class ProjectAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('project_title','project_technology','project_completion_date','status')
    list_display_links=('project_title','project_technology')
    search_fields=['project_title','project_technology','project_completion_date','status']
    list_filter=('status','project_start_date','project_completion_date','project_technology')

    def status_color(self, obj):
        if obj.status == 'Pending':
            return format_html('<span style="color: orange;">{}</span>', obj.status)
        elif obj.status == 'Completed':
            return format_html('<span style="color: green;">{}</span>', obj.status)
        elif obj.status == 'Cancelled':
            return format_html('<span style="color: red;">{}</span>', obj.status)
        elif obj.status == 'In Progress':
            return format_html('<span style="color: blue;">{}</span>', obj.status)
        else:
            return obj.status

    status_color.short_description = 'Status'

class Project_TeamAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('team_name','project','status')
    list_display_links=('team_name','project')
    search_fields=['team_name','status']
    list_filter=('status','project')

class Project_ModuleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('module_name','project','module_completion_date','status')
    list_display_links=('module_name','project')
    search_fields=['module_name','module_estimated_hours','status','module_start_date','module_completion_date']
    list_filter=('status','module_estimated_hours','module_completion_date','module_start_date')

class Project_TaskAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('task_title','module','project','user','priority','status','start_time','end_time')
    list_display_links=('task_title','module','project')
    search_fields=['task_title','task_description','priority','status','start_time','end_time']
    list_filter=('priority','status','module','project','start_time','end_time')

class User_TaskAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('task','user','status')
    list_filter=('user_totalutil_minutes',)

class Developer_SubmitAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display=('submit_title','task','module','project','submit_developer_name','submit_submit_date','status')
    list_display_links=('submit_title','task','module','project','submit_developer_name')
    search_fields=['submit_title','submit_developer_name','project','module','task','status','submit_file','submit_screenshots','submit_submit_date']
    list_filter=('submit_submit_date','status')

admin.site.register(Project,ProjectAdmin)
admin.site.register(Project_Team,Project_TeamAdmin)
admin.site.register(Project_Module,Project_ModuleAdmin)
admin.site.register(Project_Task,Project_TaskAdmin)
admin.site.register(User_Task,User_TaskAdmin)
admin.site.register(Developer_Submit,Developer_SubmitAdmin)
admin.site.register(TaskTimer)