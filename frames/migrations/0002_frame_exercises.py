# Generated by Django 5.0.6 on 2024-07-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_alter_topic_options_topic_order'),
        ('frames', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='frame',
            name='exercises',
            field=models.ManyToManyField(related_name='frames', to='exercises.exercise'),
        ),
    ]
