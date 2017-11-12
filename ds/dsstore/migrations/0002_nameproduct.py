# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-12 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_url', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
