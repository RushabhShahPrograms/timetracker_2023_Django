# Generated by Django 3.2.18 on 2023-04-09 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20230409_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
