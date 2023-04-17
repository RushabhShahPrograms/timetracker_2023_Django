# Generated by Django 3.2.18 on 2023-04-17 16:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20230414_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer_submit',
            name='code_snippets',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='developer_submit',
            name='comments',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='developer_submit',
            name='submit_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_decription',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project_module',
            name='module_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project_task',
            name='task_description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
