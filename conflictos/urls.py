from django.conf.urls import url
from . views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^conflictos.geojson$', cache_page(60*360)(ConflictosGEOJSON.as_view()), name='conflictos_geojson'),
]
