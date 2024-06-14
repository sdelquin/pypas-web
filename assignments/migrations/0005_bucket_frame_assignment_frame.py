# Generated by Django 5.0.6 on 2024-06-13 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_alter_user_token'),
        ('assignments', '0004_alter_assignment_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('num_exercises', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='assignments.bucket')),
                ('context', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='access.context')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='frame',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assignments', to='assignments.frame'),
        ),
    ]