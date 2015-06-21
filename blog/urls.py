from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.post_list),  #'http://127.0.0.1:8000/' is not a part of URL
]