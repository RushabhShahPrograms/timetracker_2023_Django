# Generated by Django 3.2.18 on 2023-05-22 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0027_alter_developer_submit_submit_developer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer_submit',
            name='module',
        ),
        migrations.RemoveField(
            model_name='developer_submit',
            name='project',
        ),
        migrations.RemoveField(
            model_name='developer_submit',
            name='task',
        ),
    ]
