# Generated by Django 5.2 on 2025-06-09 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultation_app', '0011_remove_videocall_consultation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VideoCall',
        ),
    ]
