# -*- coding: utf-8 -*-
#         name: com.namespace.blog.views
#       author: Javier Sanchez Toledano
#        email: javier@namespace.mx
#          url: http://namespace.mx
#  description: Vistas para el blog namespace.mx
#      version: 0.1.0

## MÓDULOS
# Entradas, modelo y formulario
from .models import Entry, Category

# Desde Django, utilerías y atajos
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # pylint: disable=W0611
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.syndication.views import Feed
from django.contrib.sitemaps import Sitemap

# Módulos genéricos
# from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView, DateDetailView
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page


## CLASES
# Clases genéricas
class BlogArchivo(ListView):
    queryset = Entry.objects.select_related('category').order_by('-pub_date', 'id')
    paginate_by = 6
    template_name = 'koding/index.html'


class EntradaIndividual(DetailView):
    model = Entry
    context_object_name = 'article'
    slug_field = 'slug'
    template_name = 'koding/article.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaIndividual, self).get_context_data(**kwargs)
        context['cats'] = context['article'].category.slug
        context['mnTemas'] = True
        return context


class CategoryList(ListView):
    paginate_by = 5
    template_name = "koding/category.html"
    make_object_list = True
    context_object_name = 'categoria_list'

    def get_queryset(self):
        self.cat = get_object_or_404(Categoria, slug=self.args[0])
        return Entry.objects.filter(category=self.cat).select_related().order_by('-pub_date', 'id')

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['cat'] = self.cat
        context['cats'] = self.cat.slug
        context['mnTemas'] = True
        return context

### Etiquetas
class TagListView(ListView):
    paginate_by = 5
    template_name = "koding/tag.html"
    make_object_list = True
    context_object_name = 'tag_list'

    def get_queryset(self):
        self.entries = get_list_or_404(Entry.objects.order_by('-pub_date', 'id'), tags__slug__in=[self.kwargs['tag_slug']])
        return self.entries

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        try:
            context['tag'] = self.entries[0].tags.all().filter(slug=self.kwargs['tag_slug'])[0]
            return context
        except IndexError:
            return context

def tags_list(request):
    return render(request, 'koding/tag_list.html', {'title': 'Lista de Etiquetas'})


class BlogFeed(Feed):
    '''Feed for latest 15 blog entries'''
    #These could also be pulled from your settings.py file to avoid repetitive hardcoding
    title = 'namespace.mx'
    link = 'https://namespace.mx' #URI of site
    description = 'Artículos recientes en namespace.mx - Hablamos de Desarrollo Web'
    site = 'https://namespace'

    item_author_name = 'Javier Sanchez Toledano'
    item_author_email = 'javier@toledano.dev'
    item_author_link = 'http://yo.toledano.org' #URI of author

    def items(self):
        #What items to use in the feed
        return Entry.objects.filter(status=1).order_by('-pub_date')[:15]

    def item_pubdate(self, item):
        #For each item, what is the pubdate?
        return item.pub_date

    def item_description(self, entry):
        return entry.excerpt

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Entry.objects.filter(status=1)

    def lastmod(self, obj): # pylint: disable=R0201
        return obj.pub_date

    def location(self, entry):
        return entry.permalink()


def robots (request): # pylint: disable=W0613
    """
    Devuelve el archivo robots.txt directamente a los navegadores.
    @param request:
    @return: robots.txt
    """
    return render_to_response ('robots.txt')
