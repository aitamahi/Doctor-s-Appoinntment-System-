# Generated by Django 3.2.9 on 2022-07-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_timeslot_timeslot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.ManyToManyField(to='app.Timeslot'),
        ),
    ]
