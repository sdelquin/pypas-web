# Generated by Django 5.0.6 on 2024-07-24 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frames', '0002_frame_exercises'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frame',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='frame',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
