#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.flatpages.models import FlatPage
from django.views.decorators.cache import cache_page

from blog.models import Entry
from blog.models import Categoria


# Vistas
def home(request):
    return render(request, 'post.html', {'title':'Namespace'})

def robots (request): # pylint: disable=W0613
    """
    Devuelve el archivo robots.txt directamente a los navegadores.
    @param request:
    @return: robots.txt
    """
    return render(request, 'robots.txt')


@cache_page(60 * 60 * 6)
def mapa(request):
    flats = FlatPage.objects.all()
    cats = Category.objects.all()
    meses = Entry.objects.datetimes('pub_date', 'month', order='DESC')
    entries = Entry.objects.all().order_by('-pub_date','id')[:100]
    return render(request, 'koding/mapa.html', {'flats': flats, 'cats':cats, 'meses':meses, 'entries':entries})

def error404(request):
    return render(request, '404.html', {'title': 'Error 404'})