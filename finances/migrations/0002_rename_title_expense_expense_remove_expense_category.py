# Generated by Django 4.0.5 on 2022-06-26 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='title',
            new_name='expense',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='category',
        ),
    ]
