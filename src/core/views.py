#-*- coding: utf-8 -*-
from annoying.decorators import render_to

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.flatpages.models import FlatPage
from django.views.decorators.cache import cache_page

from blog.models import Entry
from blog.models import Categoria


# Vistas
@render_to('post.html')
def home(request):
    return {'title':'Namespace'}

def robots (request): # pylint: disable=W0613
    """
    Devuelve el archivo robots.txt directamente a los navegadores.
    @param request:
    @return: robots.txt
    """
    return render_to_response ('robots.txt')


@cache_page(60 * 60 * 6)
@render_to('koding/mapa.html')
def mapa(request):
    flats = FlatPage.objects.all()
    cats = Categoria.objects.all()
    meses = Entry.objects.datetimes('pub_date', 'month', order='DESC')
    entries = Entry.objects.all().order_by('-pub_date','id')[:100]
    return {'flats': flats, 'cats':cats, 'meses':meses, 'entries':entries}

@render_to('404.html')
def error404(request):
    return {'title': 'Error 404'}