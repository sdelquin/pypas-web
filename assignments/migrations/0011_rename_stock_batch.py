# Generated by Django 5.0.6 on 2024-06-16 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0010_remove_frame_exercises_stock'),
        ('exercises', '0002_topic_exercise_topic'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stock',
            new_name='Batch',
        ),
    ]
