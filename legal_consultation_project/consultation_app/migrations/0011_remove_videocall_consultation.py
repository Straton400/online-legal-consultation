# Generated by Django 5.2 on 2025-06-09 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultation_app', '0010_videocall_consultation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videocall',
            name='consultation',
        ),
    ]
