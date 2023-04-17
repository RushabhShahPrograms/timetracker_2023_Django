from django.contrib import admin
from .models import *
from django.utils.html import format_html

class ScheduleAdmin(admin.ModelAdmin):
    search_fields=['schedule_title','schedule_meeting_date']
    list_display=('schedule_title','created_by','schedule_meeting_url','schedule_meeting_date')
    list_display_links=('schedule_title','created_by','schedule_meeting_date')
    list_filter=('schedule_created_at','schedule_meeting_date')
    save_on_top = True

class UserAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields=['username','contact_number','email','alternate_contact_number','alternate_email']
    list_display=('username','gender','contact_number','is_manager','is_developer')
    list_filter=('date_joined','is_manager','is_developer')

    @admin.display(boolean=True, description='Is Manager?')
    def is_manager(self, obj):
        return obj.is_manager
    
    @admin.display(boolean=True, description='Is Developer?')
    def is_developer(self, obj):
        return obj.is_developer
    

admin.site.register(User,UserAdmin)
admin.site.register(Schedule,ScheduleAdmin)