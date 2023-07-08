<template>
  <q-page>
    <q-layout view="lHh LpR lfr" container :style="{height: screenHeight}">
      <q-header class="bg-gray">
        <MapRibbon class="bg-grey-1 text-gobmx-gris-5"></MapRibbon>
      </q-header>


      <!-- mapa drawer capas -->
      <map-drawer-capas/>

      <q-page-container class="no-scroll">
        <q-page>
          <div class="row">
            <div class="col" :style="{'min-height': mapHeight}">

              <!-- mapa -->

              <ol-map
                ref="olmap"
                :loadTilesWhileAnimating="true"
                :loadTilesWhileInteracting="true"
                style="height: 100%; width:100%; display:inline-block;"
                renderer="webgl"
              >
                <ol-view
                  ref="olview"
                  :center="center"
                  :rotation="rotation"
                  :zoom="zoom"
                  :projection="projection"
                />
                <ol-attribution-control
                  collapsible
                  collapsed="false"/>
                <ol-overviewmap-control>
                  <ol-tile-layer>
                    <ol-source-osm/>
                  </ol-tile-layer>
                </ol-overviewmap-control>
                <ol-zoom-control></ol-zoom-control>
                <ol-fullscreen-control/>
                <ol-mouseposition-control/>
                <ol-scaleline-control/>
                <ol-rotate-control/>
                <ol-zoom-control/>
                <ol-zoomslider-control/>
                <ol-overlay :position="[-102, 25]">
                  <template v-slot="slotProps">
                    <div class="overlay-content">
                      Hello world!<br/>
                      Position: {{ slotProps.position }}
                      <q-card>
                        <q-card-section>
                          <q-card-title>
                            <div class="text-h6">Card Title</div>
                          </q-card-title>
                          <q-card-main>
                            <div class="text-subtitle2">Card content</div>
                          </q-card-main>
                        </q-card-section>
                      </q-card>
                    </div>
                  </template>
                </ol-overlay>


                <ol-tile-layer>
                  <ol-source-osm/>
                </ol-tile-layer>

                <div :key="mapkey">
                  <div v-for="layer in mapStore.capasMapa" :key="layer.value">
                    <ol-tile-layer
                      :opacity="layer.opacity"
                      :visible="layer.visible">
                      <ol-source-tile-wms
                        :url="layer.url"
                        :layers="layer.layers"
                        :serverType="layer.server_type"
                      />
                    </ol-tile-layer>
                  </div>
                </div>

              </ol-map>
            </div>
          </div>

        </q-page>
      </q-page-container>
    </q-layout>
  </q-page>
</template>

<script setup lang="ts">
import {ref, onMounted, computed, watch, getCurrentInstance} from 'vue'
import {useQuasar} from 'quasar'
import MapRibbon from 'components/mapa/ribbon/MapRibbon.vue'
import MapDrawerCapas from "components/mapa/capas/MapDrawerCapas.vue";
import {useMapStore} from 'stores/map-store'

const $q = useQuasar()
const mapStore = useMapStore()

const center = ref([-102, 24]);
const projection = ref('EPSG:4326');
const zoom = ref(6);
const rotation = ref(0);
const mapkey = ref(0);
const olmap = ref(null);
const olview = ref(null);

const screenHeight = computed(() => {
  return $q.screen.lt.md ? $q.screen.height - 50 + 'px' : $q.screen.height - 50 + 'px'
})

const mapHeight = computed(() => {
  return $q.screen.lt.md ? $q.screen.height - 135 + 'px' : $q.screen.height - 135 + 'px'
})

onMounted(() => {
  const scroll = document.querySelector('.scroll')
})

watch(mapStore.capasMapa, async (currentValue, oldValue) => {
  mapkey.value++

  /*
    olmap.value.map.getLayers().forEach(layer => {
      console.log("layer", layer)
      const source  = layer.getSource()
      console.log("source", source)
      source.refresh()

    })
  */


  //olmap.value.getLayers().forEach(layer => layer.getSource().refresh())

})

</script>
