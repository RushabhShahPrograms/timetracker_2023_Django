from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from requests import request

from .models import Developer_Submit


@receiver(post_save, sender=Developer_Submit)
def notify_manager(sender, instance, created, **kwargs):
    if created:
        submit_developer_name = instance.submit_developer_name
        submit_manager_name = instance.submit_manager_name
        message = f"A new submission has been made by {submit_developer_name}."
        messages.info(submit_manager_name, message)