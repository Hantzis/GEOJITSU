<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs">
          <q-select outlined name="base" label="Capa seleccionada"
                    :options="mapStore.mapasBase" v-model="mapStore.mapaBase"
                    emit-value map-options>
            <template v-slot:prepend>
              <q-icon name="mdi-layers"/>
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
        Capas
      </div>
      <div class="col-auto">
        <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right" @click="drawerCapas = !drawerCapas"
               style="border-radius: 0; margin-bottom: 0; margin-right: 1px;"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {useMapStore} from 'stores/map-store'
const mapStore = useMapStore()
</script>

