<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs">
          <q-select outlined name="base" label="Mapa base"
                    :options="mapStore.mapasBase" v-model="mapStore.mapaBase"
                    emit-value map-options>
            <template v-slot:prepend>
              <q-icon name="mdi-layers-outline"/>
            </template>
          </q-select>
        </div>
      </div>
    </div>
    <div class="row justify-between">
      <div class="col-auto">
        <div class="row q-px-sm"/>
      </div>
      <div class="col-auto">
        Mapa base
      </div>
      <div class="col-auto">
        <div class="col-auto">
          <div class="row q-px-sm"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {useMapStore} from 'stores/map-store'
const mapStore = useMapStore()
</script>

