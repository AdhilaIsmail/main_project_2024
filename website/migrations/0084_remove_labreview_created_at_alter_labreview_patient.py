# Generated by Django 5.0.2 on 2024-03-26 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0083_labreview_delete_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labreview',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='labreview',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.patient'),
        ),
    ]