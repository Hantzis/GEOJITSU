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
                :loadTilesWhileAnimating="true"
                :loadTilesWhileInteracting="true"
                style="height: 100%; width:100%; display:inline-block;"
              >
                <ol-view
                  ref="view"
                  :center="center"
                  :rotation="rotation"
                  :zoom="zoom"
                  :projection="projection"
                />

                <ol-tile-layer>
                  <ol-source-osm/>
                </ol-tile-layer>
              </ol-map>
            </div>
          </div>
        </q-page>
      </q-page-container>
    </q-layout>
  </q-page>
</template>

<script setup lang="ts">
import {ref, onMounted, computed} from 'vue'
import {useQuasar} from 'quasar'
import MapRibbon from 'components/mapa/ribbon/MapRibbon.vue'
import MapDrawerCapas from "components/mapa/capas/MapDrawerCapas.vue";

const $q = useQuasar()

const center = ref([-102, 26]);
const projection = ref('EPSG:4326');
const zoom = ref(8);
const rotation = ref(0);

const screenHeight = computed(() => {
  return $q.screen.lt.md ? $q.screen.height - 50 + 'px' : $q.screen.height - 50 + 'px'
})

const mapHeight = computed(() => {
  return $q.screen.lt.md ? $q.screen.height - 135 + 'px' : $q.screen.height - 135 + 'px'
})

onMounted(() => {
  const scroll = document.querySelector('.scroll')
})

</script>
