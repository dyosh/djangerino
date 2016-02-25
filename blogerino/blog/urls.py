from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<post_id>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<post_id>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<post_id>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/(?P<post_id>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),

    url(r'^comment/(?P<comment_id>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^comment/(?P<comment_id>\d+)/approve/$', views.comment_approve, name='comment_approve'),
]