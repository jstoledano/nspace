#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page

from blog.views import BlogArchivo, EntradaIndividual, CategoriaList, TagListView
from blog.views import BlogFeed
from blog.views import BlogSitemap

from django.contrib import admin
admin.autodiscover()

sitemaps = { "blog": BlogSitemap }

urlpatterns = patterns('',
    # url(r'^$', BlogArchivo.as_view(), name='home'),
    url(r'^$', cache_page(30)(BlogArchivo.as_view()), name='home'),
    url(r'^mapa/$', 'core.views.mapa', name='mapa'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rss/$', BlogFeed()),

    # ### Entrada Individual ### #
    # url(r'^(?P<cat>[-\w]+)/(?P<slug>[-\w]+)/$', EntradaIndividual.as_view(), name='post'),
    url(r'^(?P<cat>[-\w]+)/(?P<slug>[-\w]+)/$', cache_page(30) (EntradaIndividual.as_view()), name='post'),
    url(r'^t/(?P<slug>[-\w]+)/\d+$', EntradaIndividual.as_view()),
    
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', 'core.views.robots'),

    ### Etiquetas
    url(r'^tag/$', 'blog.views.tags_list', name='tags'),
    url(r'^tag/(?P<tag_slug>[-\w]+)$', TagListView.as_view(), name='tag'),

    url(r'^([-\w]+)/$', CategoriaList.as_view(), name="categoria"),
)

error404 = "core.views.error404"

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
