from django.shortcuts import render
from django.views.generic import View
from django.core.serializers import serialize
from django.http import Http404, HttpResponse
from . models import *


# Create your views here.

class ConflictosGEOJSON(View):
    def get(self, request):
        try:
            conflictos = Conflicto.objects.all()
            geojson = serialize('geojson', conflictos, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            return HttpResponse(geojson, content_type='application/json')
        except Exception as e:
            raise Http404
