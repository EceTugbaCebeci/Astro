# Generated by Django 5.0.7 on 2024-07-15 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('natalcharts', '0006_rename_probabilitiescomments_probabilitiescomment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProbabilitiesComment',
            new_name='ProbabilitiesComments',
        ),
    ]
