# Generated by Django 3.2.18 on 2023-04-08 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_developer_submit'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer_submit',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project_task'),
        ),
    ]
