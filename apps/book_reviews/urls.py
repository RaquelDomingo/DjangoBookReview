from django.conf.urls import url
from views import index, new, create, show, show_user
from . import views

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new/$', new, name='new'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<id>\d+)/$', show, name='show'),
    url(r'^users/(?P<id>\d+)/$', show_user, name='show_user'),
    
]