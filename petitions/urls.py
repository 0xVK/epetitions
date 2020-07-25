from django.conf.urls import url, include
from petitions.views import *

urlpatterns = [

    url(r'^$', index, name='index'),
    url(r'^p/(?P<pid>\d+)/$', petition, name='petition'),
    url(r'^p/(?P<pid>\d+)/sign/$', sign_petition, name='sign_petition'),
    url(r'^p/(?P<pid>\d+)/review/$', review_petition, name='review_petition'),
    url(r'^create/$', create_petition, name='create_petition'),
]
