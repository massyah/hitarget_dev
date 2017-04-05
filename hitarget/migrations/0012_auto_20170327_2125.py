# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 21:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hitarget', '0011_auto_20170309_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='location_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='data_management.Location', verbose_name='Lieux liés'),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
