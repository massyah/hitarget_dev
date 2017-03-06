# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 20:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hitarget', '0006_auto_20170220_2325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='contact',
        ),
        migrations.AddField(
            model_name='lead',
            name='contact_company',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='contact_company_entity',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='hitarget.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='contact_email',
            field=models.EmailField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='contact_name',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='contact_phone_number',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='location_entity',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='hitarget.Location'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lead',
            name='location',
            field=models.CharField(max_length=160),
        ),
    ]
