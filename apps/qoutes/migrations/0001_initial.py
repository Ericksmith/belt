# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-23 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Qoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qoute_by', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=75)),
                ('password', models.CharField(max_length=255)),
                ('birthday', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='qoute',
            name='followed_by',
            field=models.ManyToManyField(related_name='followed_qoutes', to='qoutes.User'),
        ),
        migrations.AddField(
            model_name='qoute',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_qoutes', to='qoutes.User'),
        ),
    ]
