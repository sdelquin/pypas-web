# Generated by Django 5.0.6 on 2024-07-25 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chunks', '0003_alter_chunk_puttable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='puttable',
            field=models.BooleanField(default=True),
        ),
    ]
