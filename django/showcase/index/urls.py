from django.urls import path
from index import views
from django.conf.urls import url
urlpatterns = [
    path('', views.index, name='index'),
    url(r'^index$', views.index),
]
