# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-04 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_mustbuy_nav_shop_wheel'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=60)),
                ('trackid', models.CharField(max_length=40)),
                ('categoryid', models.CharField(max_length=255)),
                ('brandname', models.CharField(max_length=55)),
                ('img1', models.CharField(max_length=255)),
                ('childcid1', models.CharField(max_length=255)),
                ('productid1', models.CharField(max_length=255)),
                ('longname1', models.CharField(max_length=255)),
                ('price1', models.CharField(max_length=255)),
                ('marketprice1', models.CharField(max_length=20)),
                ('img2', models.CharField(max_length=255)),
                ('childcid2', models.CharField(max_length=255)),
                ('productid2', models.CharField(max_length=255)),
                ('longname2', models.CharField(max_length=255)),
                ('price2', models.CharField(max_length=255)),
                ('marketprice2', models.CharField(max_length=20)),
                ('img3', models.CharField(max_length=255)),
                ('childcid3', models.CharField(max_length=255)),
                ('productid3', models.CharField(max_length=255)),
                ('longname3', models.CharField(max_length=255)),
                ('price3', models.CharField(max_length=255)),
                ('marketprice3', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'axf_mainshow',
            },
        ),
    ]
