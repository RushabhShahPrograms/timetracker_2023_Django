# Generated by Django 3.2.18 on 2023-04-24 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_tasktime'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_module',
            name='timer_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='project_module',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='project_task',
            name='timer_duration',
            field=models.DurationField(blank=True, default=0, null=True),
        ),
    ]