# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20171217_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='nickname',
            field=models.CharField(max_length=15),
        ),
    ]
