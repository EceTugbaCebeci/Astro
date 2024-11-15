# Generated by Django 5.0.7 on 2024-07-12 12:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natalcharts', '0002_planetaryposition_personalizedprobability'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalizedprobability',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='relative',
            name='role',
            field=models.CharField(blank=True, choices=[('Parent', 'Parent'), ('Sibling', 'Sibling'), ('Spouse', 'Spouse'), ('Friend', 'Friend'), ('Other', 'Other')], max_length=20),
        ),
    ]
