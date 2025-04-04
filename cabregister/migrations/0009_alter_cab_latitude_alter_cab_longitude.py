# Generated by Django 5.1.7 on 2025-03-25 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabregister', '0008_rename_lattitude_cab_latitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cab',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='cab',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True),
        ),
    ]
