#-*- coding: utf-8 -*-
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static # For static files in debug mode

from blog.views import BlogArchivo, EntradaIndividual, CategoriaList, TagListView
from blog.views import BlogFeed
from blog.views import BlogSitemap

from django.contrib import admin
# admin.autodiscover() is no longer needed in modern Django

sitemaps = { "blog": BlogSitemap }

urlpatterns = [
    # path('', BlogArchivo.as_view(), name='home'), # Original commented out
    re_path(r'^', cache_page(30)(BlogArchivo.as_view()), name='home'),
    path('mapa/', 'core.views.mapa', name='mapa'), # This will need to be fixed, direct string import is deprecated
    path('admin/', admin.site.urls),
    path('rss/', BlogFeed()),

    # ### Entrada Individual ### #
    # re_path(r'^(?P<cat>[-\w]+)/(?P<slug>[-\w]+)/
, EntradaIndividual.as_view(), name='post'), # Original commented out
    re_path(r'^(?P<cat>[-\w]+)/(?P<slug>[-\w]+)/
, cache_page(30) (EntradaIndividual.as_view()), name='post'),
    re_path(r'^t/(?P<slug>[-\w]+)/\d+
, EntradaIndividual.as_view()),
    
    path('sitemap.xml', include('django.contrib.sitemaps.views.sitemap')), # include() for sitemap
    path('robots.txt', 'core.views.robots'),

    ### Etiquetas
    path('tag/', 'blog.views.tags_list', name='tags'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)
, TagListView.as_view(), name='tag'),

    re_path(r'^([-\w]+)/
, CategoriaList.as_view(), name="categoria"),
]

# error404 = "core.views.error404" # This is not how 404 handlers are defined anymore

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # The old way of serving static files in debug mode is deprecated.
    # We also need to define MEDIA_URL in settings.
