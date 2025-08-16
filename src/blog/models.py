# -*- coding: utf-8 -*-
#         name: mx.namespace.blog.models
#       author: Javier Sanchez Toledano
#        email: javier@namespace.mx
#          url: http://namespace.mx
#  description: Modelos básicos para el blog namespace.mx
#      version: 0.1.0

# Configuración ConxB
from namespace.settings import base
from core.models import TimeStampedModel

# Desde django
from django.db import models
from django.contrib.auth.models import User

# Desde Python
from taggit.managers import TaggableManager
from bs4 import BeautifulSoup
import datetime
import markdown
import os


MD_EXT = ['codehilite', 'meta', 'abbr', 'attr_list', 'def_list', 'fenced_code', 'footnotes', 'smart_strong', 'tables',
          'headerid', 'sane_lists', 'extra', 'smartypants', 'toc', 'admonition']


class Categoria(TimeStampedModel):
    title = models.CharField('Título', max_length=250, help_text="Máximo 250 caracteres")
    slug = models.SlugField(unique=True, max_length=60, help_text="Se sugiere el texto generado por el título. Debe ser único.")
    description = models.TextField('Descripción')

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categorías"
        verbose_name = 'Categoría'

    def __unicode__(self):
        return self.title

    def permalink(self):
        return '/categoria/%s/' % self.slug

    def get_absolute_url(self):
        return 'https://namespace.mx/categoria/%s/' % self.slug


class Entry(TimeStampedModel):
    LIVE_STATUS     = 1
    DRAFT_STATUS    = 2
    HIDDEN_STATUS   = 3
    STATUS_CHOICES = (
        (LIVE_STATUS,     'Live'),
        (DRAFT_STATUS,   'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    # Campos principales
    title           = models.CharField('Título', max_length=250)
    excerpt         = models.TextField('Resumen', blank=True)
    body            = models.TextField('Contenido')
    extend          = models.TextField('Extendido', blank=True)
    pub_date        = models.DateTimeField(default=datetime.datetime.now)

    # Campos para generar el html generado con textitle
    excerpt_html    = models.TextField(editable=False, blank=True)
    body_html       = models.TextField(editable=False, blank=True)
    extend_html     = models.TextField(editable=False, blank=True)

    # Metadatos
    enable_comments = models.BooleanField(default=True)
    featured        = models.BooleanField(default=False)
    slug            = models.SlugField(unique_for_date='pub_date')
    status          = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)

    # Taxonomía
    category        = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tags            = TaggableManager()

    # Seguimiento
    autor           = models.ForeignKey(User, related_name='entradas', editable=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Entradas'
        verbose_name        = 'Entrada'
        ordering            = ['-id', '-pub_date']
        unique_together     = ('slug', 'pub_date')

    def __unicode__ (self):
        return self.title

    def save(self, force_insert=False, force_update=False):  # pylint: disable=W0221, E1002
        self.body_html = markdown.markdown(self.body, output_format='html5', lazy_ol=True, extensions=MD_EXT)
        if self.excerpt:
            self.excerpt_html = markdown.markdown(self.excerpt, output_format='html5', lazy_ol=True, extensions=MD_EXT)
        if self.extend:
            self.extend_html  = markdown.markdown(self.extend, output_format='html5', lazy_ol=True, extensions=MD_EXT)
        super(Entry, self).save(force_insert, force_update)

    def resumen(self):
        if self.excerpt:
            return unicode(self.excerpt)
        else:
            return unicode(self.body_html)

    def permalink(self):
        return "/%s/%s/" % (self.category.slug, self.slug)

    def get_absolute_url (self):
        return "https://namespace.mx/%s/%s/" % (self.category.slug, self.slug)
        