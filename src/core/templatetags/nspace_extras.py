#! -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from django.db.models import Count
from taggit.models import TaggedItem, Tag

register = template.Library()

T_MIN = 1.0
T_MAX = 6.0
T_FREQ = 2

def get_weight_fun(t_min, t_max, f_min, f_max):
    def weight_fun(f_i, t_min=t_min, t_max=t_max, f_min=f_min, f_max=f_max):
        # Prevent a division by zero here, found to occur under some
        # pathological but nevertheless actually occurring circumstances.
        if f_max == f_min:
            mult_fac = 1.0
        else:
            mult_fac = float(t_max-t_min)/float(f_max-f_min)      
        return t_max - (f_max-f_i)*mult_fac
    return weight_fun

@register.inclusion_tag('comunes/blog_recientes.html')
def recientes ():
    from blog.models import Entry
    entries = Entry.objects.order_by('-id', '-pub_date')[:5]
    return {'entries':entries}

@register.inclusion_tag('comunes/tagcloud.html')
def nube_de_etiquetas():
    queryset = Tag.objects.all()
    tags = queryset.annotate(freq=Count('taggit_taggeditem_items')).filter(freq__gte=T_FREQ)
    freq = tags.values_list('freq', flat=True)
    weight_fun = get_weight_fun(T_MIN, T_MAX, min(freq), max(freq))
    tags = tags.order_by('name')
    for tag in tags:
        tag.clase = int(weight_fun(tag.freq))
    return {'tags':tags}


@register.filter(name='jsdate')
def jsdate(d):
    """formats a python date into a js Date() constructor.
    """
    try:
        return "new Date({0},{1},{2})".format(d.year, d.month - 1, d.day)
    except AttributeError:
        return 'undefined'

@register.filter(name='moneda')
def moneda(pesos):
    pesos = round(float(pesos), 2)
    return "$%s%s" % (intcomma(int(pesos)), ("%0.2f" % pesos)[-3:])
    
@register.simple_tag
def active(request, pattern):
    import re
    try: 
        if re.search(pattern, request.path):
            return 'active'
    except: return ''  
      
@register.filter(name='clave')
def clave(dicc, key):
    try: return dicc[key]
    except KeyError: return 0
  
@register.filter(name='porciento')
def porciento(num):
    if float(num) > 100: return 100
    else: return "%.2f" % float(num)
  
@register.filter(name='ceros')
def cero(num):
    if num=='': num = 0
    return num
 

@register.filter(name='horas')
def horas(sec):
    if sec == '': return 0
    else: return (sec)/60/60

DIA = 86400

@register.filter(name='txthoras')
def txthoras(sec):
    horas = ""
    if sec == '': return 0
    else:
        sec= int(sec)
        tiempo = sec / 60
        d = (tiempo) / 1440
        h = (tiempo - (d * 1440)) / 60
        m = tiempo % 60
        if d > 0: horas = str(d) + 'd' 
        if h > 0: horas = horas  + str(h) + "h"
        if m > 0: horas = horas  + str(m) + 'm'
        return horas
    
@register.filter(name='upp')
def upp(txt):
    altas = txt
    return altas.upper()