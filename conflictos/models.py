import django
import datetime
import itertools
import re
from django.contrib.gis.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from . blocks import ConflictosStreamBlock

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from django import forms
from wagtail.snippets.models import register_snippet
from django.utils.encoding import is_protected_type
from django_select2.forms import Select2MultipleWidget, ModelSelect2MultipleWidget

from graphos.renderers.c3js import PieChart as C3PieChart
#from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import SimpleDataSource
from graphos.sources.model import ModelDataSource



# Create your models here.

class ConflictosStandardPage(Page):
    cuerpo = StreamField(ConflictosStreamBlock(), verbose_name='Cuerpo de la página', blank=True)

    content_panels = Page.content_panels + [
            StreamFieldPanel('cuerpo'),
            ]


class ConflictosMapaPagina(Page):
    es_publica = models.BooleanField(default=False)
    mostrar_aviso = models.BooleanField(default=False)
    aviso = StreamField(ConflictosStreamBlock(), verbose_name='Cuerpo del aviso de bienvenida', blank=True)
    en_construccion = StreamField(ConflictosStreamBlock(), verbose_name='Cuerpo del mensaje de página en construcción', blank=True)

    def get_conflictos_tipos(self):
        return ConflictoTipo.objects.all()

        

    content_panels = Page.content_panels + [
            FieldPanel('es_publica'),
            FieldPanel('mostrar_aviso'),
            StreamFieldPanel('aviso'),
            StreamFieldPanel('en_construccion'),
            ]


class ConflictosDatos(Page):
    cuerpo = StreamField(ConflictosStreamBlock(), verbose_name='Cuerpo de la página', blank=True)

    def get_conflictos_tipos_datos(self):
        return [(ConflictoTipo.objects.get(id=i).conflictotipo_nombre, Conflicto.objects.filter(tipo=i).count()) for i in Conflicto.objects.all().values_list('tipo', flat=True).distinct().order_by('tipo')]

    def get_conflictos_tipos_grafica(self):
        data_source = SimpleDataSource(data=self.get_conflictos_tipos())
        chart_conflictos_tipos = C3PieChart(data_source)
        return chart_conflictos_tipos

    content_panels = Page.content_panels + [
            StreamFieldPanel('cuerpo'),
            ]

class MyC3PieChart(C3PieChart):
    def get_options_json_js(self):
        return re.sub(r'\"(.+?)\":', r'\1:', self.get_options_json())[1:-1]

class ConflictosTablero(Page):
    cuerpo = StreamField(ConflictosStreamBlock(), verbose_name='Cuerpo de la página', blank=True)

    def get_conflictos_tipos_datos(self):
        return [(ConflictoTipo.objects.get(id=i).conflictotipo_nombre, Conflicto.objects.filter(tipo=i).count()) for i in Conflicto.objects.all().values_list('tipo', flat=True).distinct().order_by('tipo') if Conflicto.objects.filter(tipo=i).count() > 0]

    def get_conflictos_tipos_grafica(self):
        datos_grafica = self.get_conflictos_tipos_datos()
        #datos_grafica = ["Tipo de conflicto", "Cantidad"].append(datos_grafica)
        data_source = SimpleDataSource(data=datos_grafica)
        #chart_conflictos_tipos = C3PieChart(data_source, width=245)
        chart_conflictos_tipos = MyC3PieChart(SimpleDataSource(data=datos_grafica), options={'legend': {'show': False}})
        return chart_conflictos_tipos

    def get_conflictos_estados(self):
        estados = EntidadFederativa.objects.filter(pk__in=list(itertools.chain.from_iterable([list(EntidadFederativa.objects.filter(geom__intersects=conflicto_id).values_list('pk', flat=True)) for conflicto_id in Conflicto.objects.all().values_list('geom', flat=True).order_by('pk')]))).order_by('entidadfederativa_nombre').values_list('id', flat=True)
        conflictos_estados = [Conflicto.objects.filter(geom__intersects=EntidadFederativa.objects.get(id=estado_id).geom).count() for estado_id in EntidadFederativa.objects.filter(pk__in=list(itertools.chain.from_iterable([list(EntidadFederativa.objects.filter(geom__intersects=conflicto_id).values_list('pk', flat=True)) for conflicto_id in Conflicto.objects.all().values_list('geom', flat=True).order_by('pk')]))).order_by('entidadfederativa_nombre').values_list('id', flat=True)]
        datos = list(zip(EntidadFederativa.objects.filter(id__in=estados).values_list('entidadfederativa_nombre', flat=True), conflictos_estados))
        #grafica = C3PieChart(SimpleDataSource(data=["Entidad Federativa", "Cantidad"].append(datos)), width=225, height=400)
        grafica = C3PieChart(SimpleDataSource(data=datos), width=245, height=400)
        grafica = MyC3PieChart(SimpleDataSource(data=datos), options={'legend': {'show': False}})
        return {'datos': datos, 'grafica': grafica}

    def get_conflictos_municipios(self):
        municipios = Municipio.objects.filter(pk__in=list(itertools.chain.from_iterable([list(Municipio.objects.filter(geom__intersects=conflicto_id).values_list('pk', flat=True)) for conflicto_id in Conflicto.objects.all().values_list('geom', flat=True).order_by('pk')]))).order_by('municipio_nombre').values_list('id', flat=True)
        conflictos_municipios = [Conflicto.objects.filter(geom__intersects=Municipio.objects.get(id=municipio_id).geom).count() for municipio_id in Municipio.objects.filter(pk__in=list(itertools.chain.from_iterable([list(Municipio.objects.filter(geom__intersects=conflicto_id).values_list('pk', flat=True)) for conflicto_id in Conflicto.objects.all().values_list('geom', flat=True).order_by('pk')]))).order_by('municipio_nombre').values_list('id', flat=True)]
        datos = list(zip(Municipio.objects.filter(id__in=municipios).values_list('municipio_nombre', flat=True), conflictos_municipios))
        grafica = MyC3PieChart(SimpleDataSource(data=datos), options={'legend': {'show': False}})
        return {'datos': datos, 'grafica': grafica}

    def get_organizaciones(self):
        datos = [(Organizacion.objects.get(id=i).organizacion_nombre, Conflicto.objects.filter(organizaciones=i).distinct().count()) for i in Conflicto.objects.filter(organizaciones__isnull=False).values_list('organizaciones', flat=True).distinct().order_by('organizaciones')]
        grafica = C3PieChart(SimpleDataSource(data=datos), width=245, height=1400)
        grafica = MyC3PieChart(SimpleDataSource(data=datos), options={'legend': {'show': False}})
        return {'datos': datos, 'grafica': grafica}

    def get_empresas(self):
        datos = [(Empresa.objects.get(id=i).empresa_nombre, Conflicto.objects.filter(empresas=i).distinct().count()) for i in Conflicto.objects.filter(empresas__isnull=False).values_list('empresas', flat=True).distinct().order_by('empresas')]
        grafica = C3PieChart(SimpleDataSource(data=datos), width=245, height=1400)
        grafica = MyC3PieChart(SimpleDataSource(data=datos), options={'legend': {'show': False}})
        return {'datos': datos, 'grafica': grafica}

    def get_secretarias(self):
        datos = [(Secretaria.objects.get(id=i).secretaria_nombre, Conflicto.objects.filter(secretarias=i).distinct().count()) for i in Conflicto.objects.filter(secretarias__isnull=False).values_list('secretarias', flat=True).distinct().order_by('secretarias')]
        grafica = C3PieChart(SimpleDataSource(data=datos), width=245, height=1400)
        grafica = MyC3PieChart(SimpleDataSource(data=datos), options={'legend': {'show': False}})
        return {'datos': datos, 'grafica': grafica}

    def get_pueblos(self):
        datos = [(Pueblo.objects.get(id=i).pueblo_nombre, Conflicto.objects.filter(pueblos_originarios=i).distinct().count()) for i in Conflicto.objects.filter(pueblos_originarios__isnull=False).values_list('pueblos_originarios', flat=True).distinct().order_by('pueblos_originarios')]
        grafica = C3PieChart(SimpleDataSource(data=datos), width=245, height=1400)
        grafica = MyC3PieChart(SimpleDataSource(data=datos), options={'legend': {'show': False}})
        return {'datos': datos, 'grafica': grafica}




    content_panels = Page.content_panels + [
            StreamFieldPanel('cuerpo'),
            ]





@register_snippet
class EntidadFederativa(models.Model):
    entidadfederativa_nombre = models.CharField(max_length=100, unique=True)
    geom = models.MultiPolygonField()

    def __str__(self):
        return self.entidadfederativa_nombre

    def natural_key(self):
        return self.entidadfederativa_nombre

    class Meta:
        verbose_name_plural = 'Entidades federativas'




@register_snippet
class Municipio(models.Model):
    municipio_nombre = models.CharField(max_length=120)
    municipio_entidadfederativa = models.ForeignKey(EntidadFederativa, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='estado_municipios')
    geom = models.MultiPolygonField()

    def __str__(self):
        return "{} ({})".format(self.municipio_nombre, self.municipio_entidadfederativa)


    def natural_key(self):
        return self.municipio_nombre

    class Meta:
        ordering = ['municipio_nombre']






@register_snippet
class Organizacion(models.Model):
    organizacion_nombre = models.CharField(max_length=120, unique=True)
    organizacion_imagen = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        help_text='Ícono del logo de la organización.'
    )
    organizacion_descripcion = RichTextField()

    panels = [
            FieldPanel('organizacion_nombre', classname='full'),
            FieldPanel('organizacion_descripcion', classname='full'),
            ImageChooserPanel('organizacion_imagen')
            ]

    def __str__(self):
        return self.organizacion_nombre

    def natural_key(self):
        return self.organizacion_nombre

    class Meta:
        ordering = ['organizacion_nombre']





@register_snippet
class Empresa(models.Model):
    empresa_nombre = models.CharField(max_length=120, unique=True)
    empresa_imagen = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        help_text='Ícono del logo de la empresa.'
    )
    empresa_descripcion = RichTextField()

    panels = [
            FieldPanel('empresa_nombre'),
            FieldPanel('empresa_descripcion'),
            ImageChooserPanel('empresa_imagen')
            ]

    def __str__(self):
        return self.empresa_nombre

    def natural_key(self):
        return self.empresa_nombre

    class Meta:
        ordering = ['empresa_nombre']




@register_snippet
class Secretaria(models.Model):
    secretaria_nombre = models.CharField(max_length=120, unique=True)
    secretaria_imagen = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        help_text='Ícono del logo de la empresa.'
    )
    secretaria_descripcion = RichTextField()

    panels = [
            FieldPanel('secretaria_nombre'),
            FieldPanel('secretaria_descripcion'),
            ImageChooserPanel('secretaria_imagen')
            ]

    def __str__(self):
        return self.secretaria_nombre

    def natural_key(self):
        return self.secretaria_nombre

    class Meta:
        ordering = ['secretaria_nombre']



@register_snippet
class Pueblo(models.Model):
    pueblo_nombre = models.CharField(max_length=120, unique=True)
    pueblo_descripcion = RichTextField()

    panels = [
            FieldPanel('pueblo_nombre'),
            FieldPanel('pueblo_descripcion'),
            ]

    def __str__(self):
        return self.pueblo_nombre

    def natural_key(self):
        return self.pueblo_nombre
    
    class Meta:
        ordering = ['pueblo_nombre']



@register_snippet
class Publicacion(models.Model):
    autores = models.CharField(max_length=254)  # impresa, linea
    fecha = models.DateField() # impresa, linea
    titulo_articulo = models.CharField(max_length=254) # impresa, linea
    titulo_publicacion = models.CharField(max_length=254) # impresa, linea
    volumen = models.PositiveIntegerField(blank=True, null=True) # impresa, linea
    numero = models.PositiveIntegerField(blank=True, null=True) # impresa, linea 
    paginas = models.CharField(max_length=10, blank=True, null=True) # impresa, linea
    url = models.URLField(null=True, blank=True) # linea
    doi = models.URLField(null=True, blank=True) # linea
    

    def __str__(self):
        return '"{}", {} ({})'.format(self.titulo_articulo, self.titulo_publicacion, self.fecha.year) 

    def natural_key(self):
        return (self.pk, self.autores, self.fecha.year, self.titulo_articulo, self.titulo_publicacion, self.volumen, self.numero, self.paginas, self.url, self.doi)

    class Meta:
        ordering = ['titulo_articulo']


@register_snippet
class ConflictoTipo(models.Model):
    conflictotipo_nombre = models.CharField(max_length=60, unique=True, verbose_name='Nombre del tipo de conflicto', help_text="Nombre breve del tipo de conflicto, por ejemplo: 'Agrícola', 'Carretero', 'Minero', etc (sin comillas).")
    conflictotipo_imagen = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        verbose_name='Imagen del tipo de conflicto',
        help_text='Imagen del ícono a mostrar en el mapa para este tipo de conflicto.'
    ) 
    conflictotipo_descripcion = RichTextField()
    
    panels = [
            FieldPanel('conflictotipo_nombre', classname='full'),
            FieldPanel('conflictotipo_descripcion', classname='full'),
            ImageChooserPanel('conflictotipo_imagen')
            ] 

    def __str__(self):
        return self.conflictotipo_nombre

    def natural_key(self):
        return (self.pk, self.conflictotipo_nombre, self.conflictotipo_imagen.get_rendition('fill-40x40').url)

    class Meta:
        verbose_name = 'Tipo de conflicto'
        verbose_name_plural = 'Tipos de conflicto'




class Conflicto(models.Model):
    fecha_registro = models.DateField(auto_now_add=True)
    tipo = models.ForeignKey(ConflictoTipo, on_delete=models.PROTECT)
    estados = models.ManyToManyField(EntidadFederativa, blank=True)
    municipios = models.ManyToManyField(Municipio, blank=True)
    organizaciones = models.ManyToManyField(Organizacion, blank=True)
    empresas = models.ManyToManyField(Empresa, blank=True)
    secretarias = models.ManyToManyField(Secretaria, blank=True)
    pueblos_originarios = models.ManyToManyField(Pueblo, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    total_poblacion = models.IntegerField(null=True, blank=True)
    resumen = models.TextField(blank=True, null=True)
    bibliografia = models.TextField(blank=True, null=True)
    publicaciones = models.ManyToManyField(Publicacion, blank=True)
    geom = models.MultiPointField()

    panels = [
            FieldPanel('tipo'),
            FieldPanel('resumen'),
            FieldPanel('estados', widget=ModelSelect2MultipleWidget(search_fields=('entidadfederativa_nombre__icontains',))),
            FieldPanel('municipios', widget=ModelSelect2MultipleWidget(search_fields=['municipio_nombre__icontains'])),
            FieldPanel('organizaciones', widget=ModelSelect2MultipleWidget(search_fields=('organizacion_nombre__icontains',))),
            FieldPanel('empresas', widget=ModelSelect2MultipleWidget(search_fields=('empresa_nombre__icontains',))), 
            FieldPanel('secretarias', widget=ModelSelect2MultipleWidget(search_fields=('secretaria_nombre__icontains',))), 
            FieldPanel('pueblos_originarios', widget=ModelSelect2MultipleWidget(search_fields=('pueblo_nombre__icontains',))),
            FieldPanel('total_poblacion'),
            FieldPanel('fecha_inicio'),
            FieldPanel('fecha_fin'),
            FieldPanel('bibliografia'),
            FieldPanel('publicaciones', widget=ModelSelect2MultipleWidget(search_fields=('titulo_articulo__icontains', 'titulo_publicacion__icontains'))),
            FieldPanel('geom')
            ]

    
    def __str__(self):
        returnstr = str(self.pk)
        if self.resumen:
            if len(self.resumen) > 240:
                returnstr = returnstr + ".- " + str(self.resumen[:240]) + "..."
            else:
                returnstr = returnstr + ".- " + str(self.resumen)
        return returnstr 

    class Meta:
        ordering = ['id']


