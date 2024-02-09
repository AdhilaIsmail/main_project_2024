# Generated by Django 4.2.4 on 2023-09-23 08:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_donor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='requested_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='requested_time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]
