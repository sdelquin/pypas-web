# Generated by Django 5.0.6 on 2024-07-24 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_alter_topic_options_topic_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='available',
        ),
    ]