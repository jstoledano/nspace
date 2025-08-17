# -*- encoding: utf-8 -*-
#         name: com.conxb.blog.admin
#       author: Javier Sanchez Toledano
#        email: javier@toledano.dev
#          url: http://toledano.dev
#  description: Módulo de administración para el blog toledano.dev
#      version: 0.1.0

# Modulo de administracion
from django.contrib import admin

# Módulos de la aplicacion
from blog.models import Entry, Category

class EntryAdmin(admin.ModelAdmin): # pylint: disable=R0904
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
    date_hierarchy = 'pub_date'
    list_display = ('title', 'category', 'featured', 'status', 'pub_date')
    list_filter = ('category', 'featured', 'status')
    list_select_related = ('category',)
    

    def save_model(self, request, obj, form, change): 
        obj.autor = request.user
        obj.save()
        
class CategoryAdmin (admin.ModelAdmin): # pylint: disable=R0904
    prepopulated_fields = {'slug': ['title']} 

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)