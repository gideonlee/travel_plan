from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),	
	url(r'^logout$', views.logout, name='logout'),
	url(r'^travels$', views.dashboard, name='dashboard'),
	url(r'^travels/add$', views.add, name='add'),
	url(r'^travels/add/process$', views.process_add, name='process_add'),
	url(r'^travels/destination/(?P<id>\d+)$', views.show, name='show'),
	url(r'^travels/join/(?P<travel_id>\d+)$', views.process_join, name='process_join'),
]