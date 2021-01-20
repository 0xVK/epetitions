from django.conf.urls import url, include
from core.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [

    url(r'^fb_login/$', fb_login),
    url(r'^login/$', login_page, name='login_page'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^ticket/$', bug_ticket, name='bug_ticket'),
    url(r'^profile/my-petitions/$', my_petitions, name='my-petitions'),
    url(r'^profile/my-signed-petitions/$', my_signed_petitions, name='my-signed-petitions'),
    url(r'^profile/petitions-to-review/$', petitions_to_review, name='petitions-to-review'),
]
