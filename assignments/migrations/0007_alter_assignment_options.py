# Generated by Django 5.0.6 on 2024-06-15 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0006_alter_frame_options_alter_assignment_passed_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['created_at']},
        ),
    ]
