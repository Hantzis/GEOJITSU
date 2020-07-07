from django.contrib import admin
from .models import WMSServer, WMSLayer, CRS, Project, BaseMapLayer

# Register your models here.

admin.site.register(WMSServer)
admin.site.register(WMSLayer)
admin.site.register(CRS)
admin.site.register(Project)
admin.site.register(BaseMapLayer)