# Generated by Django 5.0.6 on 2024-05-31 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_alter_user_token'),
        ('assignments', '0003_assignment_created_at_assignment_updated_at'),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together={('user', 'exercise')},
        ),
    ]
