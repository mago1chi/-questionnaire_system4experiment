from django.conf.urls import patterns, url
from evaluate import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^confirm/', views.confirm, name='confirm'),
  url(r'^display/', views.display, name='display'),
  url(r'^register/', views.register, name='register'),
  url(r'^update/', views.update, name='update'),
)
