# Generated by Django 3.2.18 on 2023-04-07 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_alter_badge_badge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_task',
            name='end_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project_task',
            name='start_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
