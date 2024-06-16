# Generated by Django 5.0.6 on 2024-06-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0003_alter_exercise_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='topic',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
