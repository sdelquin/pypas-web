# Generated by Django 5.0.6 on 2024-06-16 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0011_rename_stock_batch'),
        ('exercises', '0002_topic_exercise_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='batches', to='exercises.exercise'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='batches', to='assignments.frame'),
        ),
    ]