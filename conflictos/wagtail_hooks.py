from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from . models import *
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.forms.widgets import OSMWidget
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from django_select2.forms import Select2MultipleWidget, ModelSelect2MultipleWidget
from wagtail.core import hooks

"""
@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'snippets']
"""


class ConflictoAdmin(ModelAdmin):
    model = Conflicto
    menu_label = 'Conflictos'
    search_fields = ('id', 'resumen')
    list_display = ('id', 'resumen')
    formfield_overrides = {
            models.ManyToManyField: {'widget': ModelSelect2MultipleWidget},
            }

    class Media:
        js = ("ext/js/jquery.min.js",)


class ConflictoTipoAdmin(ThumbnailMixin, ModelAdmin):
    model = ConflictoTipo
    menu_icon = 'cogs'
    menu_label = 'Tipos de conflicto'
    search_fields = ('conflictotipo_nombre', 'conflictotipo_descripcion')
    list_display = ('admin_thumb', 'conflictotipo_nombre', 'conflictotipo_descripcion')
    thumb_image_field_name = 'conflictotipo_imagen'
    thumb_col_header_text = 'Ícono'


class OrganizacionAdmin(ThumbnailMixin, ModelAdmin):
    model = Organizacion
    menu_icon = 'folder'
    menu_label = 'Organizaciones'
    search_fields = ('organizacion_nombre', 'organizacion_descripcion')
    list_display = ('admin_thumb', 'organizacion_nombre', 'organizacion_descripcion')
    thumb_image_field_name = 'organizacion_imagen'
    thumb_col_header_text = 'Logo'


class EmpresaAdmin(ThumbnailMixin, ModelAdmin):
    model = Empresa
    menu_icon = 'link'
    menu_label = 'Empresas'
    search_fields = ('empresa_nombre', 'empresa_descripcion')
    list_display = ('admin_thumb', 'empresa_nombre', 'empresa_descripcion')
    thumb_image_field_name = 'empresa_imagen'
    thumb_col_header_text = 'Logo'


class SecretariaAdmin(ThumbnailMixin, ModelAdmin):
    model = Secretaria
    menu_icon = 'form'
    menu_label = 'Secretarías'
    search_fields = ('secretaria_nombre', 'secretaria_descripcion')
    list_display = ('admin_thumb', 'secretaria_nombre', 'secretaria_descripcion')
    thumb_image_field_name = 'secretaria_imagen'
    thumb_col_header_text = 'Logo'


class PuebloAdmin(ModelAdmin):
    model = Pueblo
    menu_icon = 'group'
    menu_label = 'Pueblos originarios'
    search_fields = ('pueblo_nombre', 'pueblo_descripcion')
    list_display = ('pueblo_nombre', 'pueblo_descripcion')


class PublicacionAdmin(ModelAdmin):
    model = Publicacion
    menu_icon = 'doc-full'
    menu_label = 'Publicaciones'
    search_fields = ('id', 'titulo_articulo', 'titulo_publicacion')
    list_display = ('id', 'titulo_articulo', 'titulo_publicacion')


class CamposConflictosModelAdminGroup(ModelAdminGroup):
    menu_label = 'Campos conflictos'
    menu_icon = 'folder-open-inverse' 
    items = (ConflictoTipoAdmin, OrganizacionAdmin, EmpresaAdmin, SecretariaAdmin, PuebloAdmin, PublicacionAdmin)


modeladmin_register(CamposConflictosModelAdminGroup)
modeladmin_register(ConflictoAdmin)
