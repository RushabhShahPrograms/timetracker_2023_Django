# Generated by Django 3.2.18 on 2023-04-11 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20230411_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer_submit',
            name='submit_time_spent',
            field=models.DurationField(blank=True, null=True),
        ),
    ]