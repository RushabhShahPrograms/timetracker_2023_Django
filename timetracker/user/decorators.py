from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,login_url='login'):
    actual_decorator = user_passes_test(lambda user:user.is_active and user.is_manager,login_url=login_url,redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator

def developer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,login_url='login'):
    actual_decorator = user_passes_test(lambda user:user.is_active and user.is_developer,login_url=login_url,redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_manager(user):
    return user.is_authenticated and user.is_manager

def is_developer(user):
    return user.is_authenticated and user.is_developer

manager_or_developer_required = user_passes_test(lambda u: is_manager(u) or is_developer(u))