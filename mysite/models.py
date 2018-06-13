from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Users(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=15)
    message = models.CharField(max_length=20,default='这个人很懒什么也没说')
    pub_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message



class All_Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    article = models.TextField()
    time = models.DateTimeField(auto_now=True)
    replay_time = models.DateField()
    def __str__(self):
        return self.title

class Collection(models.Model):                               #收藏
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ManyToManyField(All_Article)

    def __str__(self):
        return self.article

class Replay(models.Model):
    all_article = models.ForeignKey(All_Article, on_delete=models.CASCADE)
    text = models.TextField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text




# Create your models here.


