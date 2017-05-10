from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^index/$', views.userindex,name="userindex"),
    url(r'^(?P<bulletin_id>[0-9]+)/list/$', views.message_list,name="message_list"),
    url(r'^login/$', views.userLogin, name="userlogin"),
    url(r'^(?P<message_id>[0-9]+)/detail/$', views.message_detail,name="message_detail"),
    url(r'^logout/$', views.userLogout, name="userlogout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^create_bulletin/$', views.create_bulletin, name="create_bulletin"),
    url(r'^(?P<bulletin_id>[0-9]+)/del_bulletin/$', views.del_bulletin, name="del_bulletin"),
    url(r'^search/$', views.search_bulletin, name="search_bulletin"),
    url(r'^(?P<bulletin_id>[0-9]+)/follow_bulletin/$', views.follow_bulletin, name="follow_bulletin"),
    url(r'^(?P<bulletin_id>[0-9]+)/post_message/$', views.post_message, name="post_message")
    #url(r'^(?P<id>\d+)/$', views.detail, name='detail'),
    #url(r'^test/$', views.test),
    #url(r'^(?P<id>[0-9]+)/del/$', views.del_post, name='del_post'),
    #url(r'^(?P<id>[0-9]+)/edit/$$', views.edit_post, name='edit_post')

]