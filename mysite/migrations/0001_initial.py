# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='All_Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=20)),
                ('article', models.TextField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('replay_time', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('article', models.ManyToManyField(to='mysite.All_Article')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('text', models.TextField(max_length=150)),
                ('user', models.IntegerField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('all_article', models.ForeignKey(to='mysite.All_Article')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nickname', models.CharField(max_length=15)),
                ('message', models.CharField(max_length=20, default='这个人很懒什么也没说')),
                ('pub_time', models.DateTimeField(auto_now=True)),
                ('username', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
