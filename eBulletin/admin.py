from django.contrib import admin
from eBulletin.models import Bulletin,Profile,Message,Comment
# Register your models here.
admin.site.register(Profile)
admin.site.register(Bulletin)
admin.site.register(Message)
admin.site.register(Comment)
