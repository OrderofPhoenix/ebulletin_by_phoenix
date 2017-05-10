from django.test import TestCase
from .models import Bulletin,Message,Comment
from django.contrib.auth.models import User 

# Create your tests here.
def message_list(login_user_id, bulletin_id):
    
    login_user=User.objects.get(pk=login_user_id)
    created_bulletins=Bulletin.objects.filter(creator=login_user)
    followed_bulletins=Bulletin.objects.filter(follower=login_user)
    
    bulletin=Bulletin.objects.get(pk=bulletin_id)
    messages=Message.objects.filter(bulletin=bulletin)
    message_comments=[]
    for message in messages:
        comments=Comment.objects.filter(message=message)
        message_comments.append((message.id,comments))
    message_comments_dict=dict(message_comments)
    return message_comments,message_comments_dict