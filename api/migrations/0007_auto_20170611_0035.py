# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 00:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20170609_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
