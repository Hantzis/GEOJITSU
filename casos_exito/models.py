from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Estado(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Localidad(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Representante(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class GrupoEtnico(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class ActividadEconomica(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Certificacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Reconocimiento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class ActividadPreponderantePromovente(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class AreaConocimiento(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Promovente(models.Model):
    fecha_registro = models.DateField()
    nombre = models.CharField(max_length=255, unique=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=30, choices=(
        ('', 'Género'), ('masculino', 'Masculino'), ('femenino', 'Femenìno'), ('otro', 'Otro')))
    edad = models.PositiveIntegerField()
    actividad_preponderante = models.ForeignKey(ActividadPreponderantePromovente, on_delete=models.PROTECT)
    escolaridad = models.CharField(max_length=30, choices=(
        ('', 'Escolaridad'), ('primaria', 'Primaria'), ('secundaria', 'Secundaria'),
        ('preparatoria', 'Preparatoria'), ('licenciatura', 'Licenciatura'),
        ('maestria', 'Maestría'), ('doctorado', 'Doctorado')))
    area_conocimiento = models.ForeignKey(AreaConocimiento, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    vinculo = models.CharField(max_length=30,
                               choices=(('', 'Vinculo o relación con proyecto ONSSES'), ('voluntario', 'Voluntario'),
                                        ('estudiante', 'Estudiante'), ('servicio_social', 'Servicio Social'),
                                        ('tecnico', 'Técnico'), ('investigador', 'Investigador')))
    fecha_adscripcion_onsses = models.DateField()
    miembro_proyecto = models.BooleanField(default=False, blank=True, null=True)
    fecha_adscripcion_proyecto = models.DateField()

    def __str__(self):
        return self.nombre


class TipoProgramaOrdenamiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre




class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=255, unique=True)
    nombre_corto = models.CharField(max_length=50, unique=True)
    fecha_inicio = models.DateField()
    etapa = models.CharField(max_length=20, choices=(
        ('', 'Etapa del proyecto'), ('inicial', 'Inicial'), ('intermedio', 'Intermedio'), ('avanzado', 'Avanzado')))
    fecha_registro = models.DateField()
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    ubicacion = models.PointField()
    territorio = models.PolygonField()
    escala = models.CharField(max_length=20, choices=(
        ('', 'Escala del proyecto'), ('regional', 'Regional'), ('municipal', 'Municipal'), ('local', 'Local')))
    area_influencia = models.CharField(max_length=255, blank=True, null=True)
    domicilio = models.TextField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    representante = models.ForeignKey(Representante, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    numero_miembros = models.PositiveIntegerField()
    tipo_organizacion = models.CharField(max_length=30, choices=(
        ('', 'Tipo de organización'), ('sociedad_civil', 'Sociedad Civil'), ('otra', 'Otra')))
    grupo_etnico = models.ForeignKey(GrupoEtnico, on_delete=models.PROTECT, null=True, blank=True)
    inclusion_genero = models.BooleanField(default=False, null=True)
    numero_hombres = models.IntegerField(validators=[MinValueValidator(0)])
    numero_mujeres = models.IntegerField(validators=[MinValueValidator(0)])
    actividad_principal = models.ForeignKey(ActividadEconomica, on_delete=models.PROTECT, related_name='proyecto_actividadprincipal')
    actividad_secundaria = models.ForeignKey(ActividadEconomica, on_delete=models.PROTECT, related_name='proyecto_actividadsecundaria', blank=True, null=True)
    otra_actividad = models.ForeignKey(ActividadEconomica, on_delete=models.PROTECT, related_name='proyecto_actividadotra', blank=True, null=True)
    descripcion_proyecto = models.TextField()
    logros_proyecto = models.TextField()
    certificaciones = models.ManyToManyField(Certificacion, blank=True)
    reconocimientos = models.ManyToManyField(Reconocimiento, blank=True)
    redes = models.TextField()
    financiamientos = models.TextField(null=True, blank=True)
    estructura_gobierno = models.CharField(max_length=100)
    promovente = models.ForeignKey(Promovente, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_proyecto


class Evaluacion(models.Model):
    fecha = models.DateField()
    promovente = models.ForeignKey(Promovente, on_delete=models.PROTECT)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.fecha}, {self.promovente}"


class GeneracionConocimiento(models.Model):
    estrategias_sistematizacion_conocimiento = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    formacion_investigadores_comunitarios = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    inovacion_saberes_locales = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    gestion_documental_generacion_conocimiento = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

    def __str__(self):
        promedio = (self.estrategias_sistematizacion_conocimiento + self.formacion_investigadores_comunitarios +
                    self.inovacion_saberes_locales + self.gestion_documental_generacion_conocimiento) / 4
        return f"{self.pk} :: {self.evaluacion} ({promedio})"

class EconomiaSocialSolidaria(models.Model):
    cooperacion_colaboracion = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    intercambio_organizaciones = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    intercambio_local = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    insumos_locales = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    autonomia_financiera = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    economia_circular = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

class GestionAmbiental(models.Model):
    gestion_agua = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    gestion_residuos_solidos = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    gestion_residuos_peligrosos = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    materiales_regionales = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    materiales_amigables_ambiente = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    programa_manejo_flora = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    programa_manejo_ambiental_avalado = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    estrategia_trafico_especies_riesgo = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

class IdentidadBiocultural(models.Model):
    fomenta_lengua_local = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    participacion_celebraciones_locales = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    participacion_intercambio_saberes_locales = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    conservacion_patrimonio_biocultural = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    promocion_practicas_tradicionales = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

class IntegridadTerritorial(models.Model):
    alineado_programas_ordenamiento = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    tipos_programa_ordenamiento = models.ManyToManyField(TipoProgramaOrdenamiento, null=True, blank=True)
    otro_programa_ordenamiento = models.CharField(max_length=50, null=True, blank=True)
    alineado_programas_ordenamiento_comunitario = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    alineado_plan_desarrollo_local = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    participa_comite_comunitario = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    aporta_beneficios_comunidad = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

class ManejoRiesgo(models.Model):
    alineado_diagnostico_riesgo = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    programa_contingencia_riesgo = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    participa_comites_proteccion_civil = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    fondo_ahorro_contingencia = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    programas_capacitacion_riesgo = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

class BuenGobiernoExterno(models.Model):
    participacion_activa_reglamentos = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    participacion_equitativa_reglamentos = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    participacion_previa_libre_informada = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    participacion_otros_actores = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

class BuenGobiernoInterno(models.Model):
    regulacion_actores_externos = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    decisiones_internas_colectivas = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    acuerdos_comunes_resolucion_conflictos = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    espacios_participacion = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    incorpora_cosmovision_local = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)

class ProduccionSocialAmbientalAmigable(models.Model):
    insumos_bajo_impacto_ambiental = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    tecnologia_respetuosa_naturaleza = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    respeta_saberes_locales = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    privilegia_trabajo_local = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)])
    evaluacion = models.OneToOneField(Evaluacion, on_delete=models.CASCADE)
