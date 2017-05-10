from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings

# Create your models here.
# class Userprofile(models.Model):
#     user=models.OneToOneField(User,unique=True)
#     phone = models.CharField(max_length=11,null=True, blank=True)
#     gender = models.CharField(max_length=2)
#     nick_name = models.CharField(max_length=50,  default="")
#     birthday = models.DateField(null=True, blank=True)
#     address = models.CharField(max_length=100, default="")
#     image = models.ImageField(upload_to="image/%Y/%m", default=u"/static/img/img.jpg", max_length=100)
#
#
#     def __unicode__(self):
#         return self.name
class Profile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to='static/image/%Y/%m',
                              default='static/image/default.jpg',
                              max_length=200,
                              blank=True,
                              null=True,
                              verbose_name='user_icon')
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Bulletin(models.Model):
    creator = models.ForeignKey(User,related_name='created_bulletin')
    follower = models.ManyToManyField(User,related_name='followed_bulletin')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True,null=True)


    def __unicode__(self):
        return self.name


class Message(models.Model):
    bulletin = models.ForeignKey(Bulletin)
    publisher = models.ForeignKey(User)
    release_time = models.DateTimeField(auto_now_add = True)
    message_content = models.TextField(null = True)
    title = models.CharField(max_length = 100)
    category = models.CharField(max_length = 50, blank = True)
   
   
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-release_time']

class Comment(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE)
    critics = models.ForeignKey(User)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField(blank=True, null=True)
    

    def __unicode__(self):
        return self.comment_content[:20]

    class Meta:
        ordering = ['-comment_time'] 

