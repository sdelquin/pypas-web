# Generated by Django 5.0.6 on 2024-06-16 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0009_remove_frame_num_exercises'),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frame',
            name='exercises',
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadable', models.BooleanField(default=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock', to='exercises.exercise')),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock', to='assignments.frame')),
            ],
        ),
    ]
