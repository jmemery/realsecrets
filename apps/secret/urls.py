from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^secrets$', views.secrets),
    url(r'^secretsubmit$', views.secretsubmit),
    url(r'^likesecret(?P<secretid>\d+)$', views.likesecret),
    url(r'^deletesecret(?P<secretid>\d+)$', views.deletesecret),
    url(r'^popularsecrets$', views.popularsecrets),
    url(r'^mysecrets$', views.mysecrets),
    url(r'^otherssecrets$', views.otherssecrets),
    url(r'^logout$', views.logout),
]
