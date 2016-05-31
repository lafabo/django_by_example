from django.conf.urls import url, include
from . import views


urlpatterns = [
	# post views
	# old login view
	# url(r'^login/$', views.user_login, name='login'),

	# login logout urls
	url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
	url(r'logout/$', 'django.contrib.auth.views.logout', name='logout'),
	url(r'logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
	url(r'^$', views.dashboard, name='dashboard'),
	# change password urls
	url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
	# reset password urls
	url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
	url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
	url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
	url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
	# user registration
	url(r'^registration/$', views.registration, name='registration'),
	# user edit profile
	url(r'^edit/$', views.edit, name='edit'),
	url(r'social-auth/', include('social.apps.django_app.urls', namespace='social')),
	# following
	url(r'^users/follow/$', views.user_follow, name='user_follow'),
	# user list
	url(r'^users/$', views.user_list, name='user_list'),
	# user details page
	url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),
]
