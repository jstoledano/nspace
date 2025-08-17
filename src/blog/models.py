# -*- coding: utf-8 -*-
#         name: mx.namespace.blog.models
#       author: Javier Sanchez Toledano
#        email: javier@toledano.dev
#          url: http://toledano.dev
#  description: Modelos básicos para el blog toledano.dev
#      version: 0.1.0

# Configuración ConxB
from core.models import TimeStampedModel

# Desde django
from django.db import models
from django.contrib.auth.models import User

# Desde Python
from taggit.managers import TaggableManager
import datetime
from django.utils import timezone
import markdown


MD_EXT = ['codehilite', 'meta', 'abbr', 'attr_list', 'def_list', 'fenced_code', 'footnotes', 'smart_strong', 'tables',
          'headerid', 'sane_lists', 'extra', 'smartypants', 'toc', 'admonition']


class Category(TimeStampedModel):
    title = models.CharField('Título', max_length=250, help_text="Máximo 250 caracteres")
    slug = models.SlugField(unique=True, max_length=60, help_text="Se sugiere el texto generado por el título. Debe ser único.")
    description = models.TextField('Descripción')
    icon = models.CharField('Icono', max_length=50, blank=True, help_text="Nombre del icono de FontAwesome o similar (ej. coffee, music)")

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"
        verbose_name = 'Category'

    def __str__(self):
        return self.title

    def permalink(self):
        return '/category/%s/' % self.slug

    def get_absolute_url(self):
        return 'https://toledano.dev/category/%s/' % self.slug


class Entry(TimeStampedModel):
    class EntryStatus(models.TextChoices):
        LIVE = 'LIVE', 'Live'
        DRAFT = 'DRAFT', 'Draft'
        HIDDEN = 'HIDDEN', 'Hidden'

    status = models.CharField(
        max_length=10,
        choices=EntryStatus.choices,
        default=EntryStatus.LIVE,
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
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags            = TaggableManager()

    # Seguimiento
    autor           = models.ForeignKey(User, related_name='entradas', editable=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Entries'
        verbose_name        = 'Entry'
        ordering            = ['-id', '-pub_date']
        unique_together     = ('slug', 'pub_date')

    def __str__ (self):
        return self.title

    def save(self, force_insert=False, force_update=False):  # pylint: disable=W0221, E1002
        self.body_html = markdown.markdown(self.body, extensions=MD_EXT)
        if self.excerpt:
            self.excerpt_html = markdown.markdown(self.excerpt, extensions=MD_EXT)
        if self.extend:
            self.extend_html  = markdown.markdown(self.extend, extensions=MD_EXT)
        super(Entry, self).save(force_insert, force_update)

    def resumen(self):
        if self.excerpt:
            return str(self.excerpt)
        else:
            return str(self.body_html)

    def permalink(self):
        return "/category/%s/%s/" % (self.category.slug, self.slug)

    def get_absolute_url (self):
        return "https://toledano.dev/category/%s/%s/" % (self.category.slug, self.slug)
        