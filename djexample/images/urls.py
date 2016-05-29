from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^create/$', views.image_create, name='create'),
	url(r'^detail/(?P<id>\d+)/(?P<slug>[-\W]+)/$', views.image_detail, name='default'),
	url(r'^like/$', views.image_like, name='like'),
	url(r'^$', views.image_list, name='list'),
]
