from django.contrib.gis.db import models


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


class Financiamiento(models.Model):
    fuente = models.CharField(max_length=200)
    anyo = models.IntegerField()
    monto = models.FloatField()

    def __str__(self):
        return f'{self.fuente} ({self.anyo}) : ${self.monto}'


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
    relacion_proyecto_onsses = models.BooleanField(default=False, blank=True, null=True)
    relacion_proyecto = models.BooleanField(default=False, blank=True, null=True)


    def __str__(self):
        return self.nombre


class CasoExito(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
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
    domicilio = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    representante = models.ForeignKey(Representante, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    numero_miembros = models.PositiveIntegerField()
    tipo_organizacion = models.CharField(max_length=30, choices=(
        ('', 'Tipo de organización'), ('sociedad_civil', 'Sociedad Civil'), ('otra', 'Otra')))
    grupo_etnico = models.ForeignKey(GrupoEtnico, on_delete=models.PROTECT)
    inclusion_genero = models.BooleanField(default=False, null=True)
    numero_hombres = models.IntegerField()
    numero_mujeres = models.IntegerField()
    actividad_principal = models.ForeignKey(ActividadEconomica, on_delete=models.PROTECT, related_name='casoexito_actividadprincipal')
    actividad_secundaria = models.ForeignKey(ActividadEconomica, on_delete=models.PROTECT, related_name='casoexito_actividadsecundaria', blank=True, null=True)
    otra_actividad = models.ForeignKey(ActividadEconomica, on_delete=models.PROTECT, blank=True, null=True)
    descripcion_proyecto = models.TextField()
    logros_proyecto = models.TextField()
    certificaciones = models.ManyToManyField(Certificacion, blank=True)
    reconocimientos = models.ManyToManyField(Reconocimiento, blank=True)
    redes = models.TextField()
    financiamientos = models.ManyToManyField(Financiamiento, blank=True)
    estructura_gobierno = models.CharField(max_length=255)
    promovente = models.ForeignKey(Promovente, on_delete=models.PROTECT)
