from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static


sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    # Examples:
    # url(r'^$', 'djexample.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^account/', include('account.urls')),
    url(r'^images/', include('images.urls', namespace='images')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
