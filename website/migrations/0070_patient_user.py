# Generated by Django 5.0.2 on 2024-02-09 05:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0069_alter_bloodrequest_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
