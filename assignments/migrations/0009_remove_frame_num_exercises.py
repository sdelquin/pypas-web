# Generated by Django 5.0.6 on 2024-06-16 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0008_frame_exercises'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frame',
            name='num_exercises',
        ),
    ]
