# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20171217_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='nickname',
            field=models.CharField(default=None, max_length=15),
        ),
    ]
