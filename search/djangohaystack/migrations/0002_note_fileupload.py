# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-27 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('djangohaystack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='fileUpload',
            field=models.FileField(default=django.utils.timezone.now, upload_to='fileup'),
            preserve_default=False,
        ),
    ]
