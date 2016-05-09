from django.contrib.urls import url
from . import views

urlpatterns = [
	url(r'^s', views.post_list, name='post_list')
	url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\{2})/(?P<post>[-\w+]/$',
	    views.post_detail, name='post_detail')
]