# Generated by Django 5.1.7 on 2025-03-26 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='place_id',
        ),
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.FloatField(max_length=100),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.FloatField(max_length=100),
        ),
    ]
