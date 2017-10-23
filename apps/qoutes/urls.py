from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),    
    url(r'^addQoute$', views.addQoute),
    url(r'^followQoute/(?P<qoute_id>[0-9]+)$', views.followQoute),
    url(r'^removeQoute/(?P<qoute_id>[0-9]+)$', views.removeQoute),
    url(r'^users/(?P<user_id>[0-9]+)$', views.users),
    # url(r'^', views.)
]