# Generated by Django 5.0.6 on 2024-07-24 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chunks', '0001_initial'),
        ('frames', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunk',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chunks', to='frames.frame'),
        ),
        migrations.AlterUniqueTogether(
            name='chunk',
            unique_together={('frame', 'exercise')},
        ),
    ]
