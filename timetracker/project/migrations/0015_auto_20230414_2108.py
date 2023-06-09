# Generated by Django 3.2.18 on 2023-04-14 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_developer_submit_submit_time_spent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer_submit',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('In Progress', 'In Progress'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='In Progress', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Cancelled', 'Cancelled')], max_length=100),
        ),
        migrations.AlterField(
            model_name='project_module',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Cancelled', 'Cancelled')], max_length=100),
        ),
    ]
