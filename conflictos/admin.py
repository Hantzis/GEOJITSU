from django.contrib import admin

from . models import *

from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.



admin.site.register(Conflicto, OSMGeoAdmin)
admin.site.register(Organizacion)
admin.site.register(Empresa)
admin.site.register(Secretaria)
admin.site.register(Pueblo)
admin.site.register(Publicacion)
