#-*- coding: utf-8 -*-
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static # For static files in debug mode

from blog.views import BlogArchivo, EntradaIndividual, CategoriaList, TagListView, tags_list
from blog.views import BlogFeed
from blog.views import BlogSitemap

from core.views import mapa, robots

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
# admin.autodiscover() is no longer needed in modern Django

sitemaps = { "blog": BlogSitemap }

urlpatterns = [
    path('', BlogArchivo.as_view(), name='home'), # Original commented out
    # path('', cache_page(30)(BlogArchivo.as_view()), name='home'),
    path('mapa/', mapa, name='mapa'),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('rss/', BlogFeed()),
    path('<slug:cat>/<slug:slug>/', EntradaIndividual.as_view(), name='post'),    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}), # Pass sitemap function directly
    path('robots.txt', robots),
    path('tag/', tags_list, name='tags'),
    path('tag/<slug:tag_slug>', TagListView.as_view(), name='tag'),
    path('cats/', CategoriaList.as_view(), name="categoria"),
]

# error404 = "core.views.error404" # This is not how 404 handlers are defined anymore

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # The old way of serving static files in debug mode is deprecated.
    # We also need to define MEDIA_URL in settings.
