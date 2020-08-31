from django.contrib import admin
from . models import *

# Register your models here.

class GeneracionConocimientoInline(admin.TabularInline):
    model = GeneracionConocimiento
    fields = ['estrategias_sistematizacion_conocimiento', 'formacion_investigadores_comunitarios',
              'inovacion_saberes_locales', 'gestion_documental_generacion_conocimiento']

class EconomiaSocialSolidariaInline(admin.TabularInline):
    model = EconomiaSocialSolidaria
    fields = ['cooperacion_colaboracion', 'intercambio_organizaciones', 'intercambio_local', 'insumos_locales',
              'autonomia_financiera', 'economia_circular']

class GestionAmbientalInline(admin.TabularInline):
    model = GestionAmbiental
    fields = ['gestion_agua', 'gestion_residuos_solidos', 'gestion_residuos_peligrosos', 'materiales_regionales',
              'materiales_amigables_ambiente', 'programa_manejo_flora', 'programa_manejo_ambiental_avalado',
              'estrategia_trafico_especies_riesgo']

class IdentidadBioculturalInline(admin.TabularInline):
    model = IdentidadBiocultural
    fields = ['fomenta_lengua_local', 'participacion_celebraciones_locales',
              'participacion_intercambio_saberes_locales', 'conservacion_patrimonio_biocultural',
              'promocion_practicas_tradicionales']

class IntegridadTerritorialInline(admin.TabularInline):
    model = IntegridadTerritorial
    fields = ['alineado_programas_ordenamiento', 'tipos_programa_ordenamiento',
              'otro_programa_ordenamiento', 'alineado_programas_ordenamiento_comunitario',
              'alineado_plan_desarrollo_local', 'participa_comite_comunitario', 'aporta_beneficios_comunidad']

class ManejoRiesgoInline(admin.TabularInline):
    model = ManejoRiesgo
    fields = ['alineado_diagnostico_riesgo', 'programa_contingencia_riesgo',
              'participa_comites_proteccion_civil', 'fondo_ahorro_contingencia',
              'programas_capacitacion_riesgo']

class BuenGobiernoExternoInline(admin.TabularInline):
    model = BuenGobiernoExterno
    fields = ['participacion_activa_reglamentos', 'participacion_equitativa_reglamentos',
              'participacion_previa_libre_informada', 'participacion_otros_actores']

class BuenGobiernoInternoInline(admin.TabularInline):
    model = BuenGobiernoInterno
    fields = ['regulacion_actores_externos', 'decisiones_internas_colectivas',
              'acuerdos_comunes_resolucion_conflictos', 'espacios_participacion', 'incorpora_cosmovision_local']

class ProduccionSocialAmbientalAmigableInline(admin.TabularInline):
    model = ProduccionSocialAmbientalAmigable
    fields = ['insumos_bajo_impacto_ambiental', 'tecnologia_respetuosa_naturaleza',
              'respeta_saberes_locales', 'privilegia_trabajo_local']

@admin.register(Evaluacion)
class SolicitudCotizacionAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [GeneracionConocimientoInline, EconomiaSocialSolidariaInline, GestionAmbientalInline,
               IdentidadBioculturalInline, IntegridadTerritorialInline, ManejoRiesgoInline, BuenGobiernoExternoInline,
               BuenGobiernoInternoInline, ProduccionSocialAmbientalAmigableInline]

admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Localidad)
admin.site.register(Representante)
admin.site.register(GrupoEtnico)
admin.site.register(ActividadEconomica)
admin.site.register(Certificacion)
admin.site.register(Reconocimiento)
admin.site.register(ActividadPreponderantePromovente)
admin.site.register(AreaConocimiento)
admin.site.register(Promovente)
admin.site.register(Proyecto)



admin.site.register(TipoProgramaOrdenamiento)
admin.site.register(GeneracionConocimiento)
admin.site.register(EconomiaSocialSolidaria)
admin.site.register(GestionAmbiental)
admin.site.register(IdentidadBiocultural)
admin.site.register(IntegridadTerritorial)
admin.site.register(ManejoRiesgo)
admin.site.register(BuenGobiernoExterno)
admin.site.register(BuenGobiernoInterno)
admin.site.register(ProduccionSocialAmbientalAmigable)


