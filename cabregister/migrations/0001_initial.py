# Generated by Django 5.1.7 on 2025-03-24 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_number', models.CharField(max_length=150)),
                ('adhar', models.ImageField(upload_to='adhar car owner')),
                ('driving_license', models.ImageField(upload_to='driving license')),
                ('vehicle_rc', models.ImageField(upload_to='Vehicle')),
                ('vehicle_type', models.CharField(max_length=150)),
                ('price_per_km', models.PositiveIntegerField()),
                ('approved', models.BooleanField(default=False)),
                ('on_dutty', models.BooleanField(default=False)),
                ('busy', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cab_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CabImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cab_images', to='cabregister.cab')),
            ],
        ),
        migrations.CreateModel(
            name='CabLocationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabregister.cab')),
            ],
        ),
    ]
