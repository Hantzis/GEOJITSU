<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs q-pt-xs1 q-pl-xs q-pr-xs">
          <q-btn-toggle
            style="border-radius: 0; flex-wrap: wrap; max-width: 96px"
            v-model="herramienta_estandar_activa"
            dense
            unelevated
            text-color="grey-7"
            toggle-text-color="white"
            toggle-color="primary"
            :options="[
              {value: 'desplazar', slot: 'desplazar'},
              {value: 'info', slot: 'info'},
              {value: 'zoom-in', slot: 'zoom-in'},
              {value: 'seleccion', slot: 'seleccion'},
              {value: 'medicion', slot: 'medicion'},
              {value: 'zoom-out', slot: 'zoom-out'},
            ]"
          >
            <template v-slot:desplazar>
              <q-icon name="mdi-hand-right">
                <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Desplazar
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:zoom-in>
              <q-icon name="mdi-magnify-plus">
                <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Acercar
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:seleccion>
              <q-icon name="mdi-selection-drag">
                <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Selección
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:info>
              <q-icon name="mdi-information">
                <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Información
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:zoom-out>
              <q-icon name="mdi-magnify-minus">
                <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Alejar
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:medicion>
              <q-icon name="mdi-ruler">
                <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Medición
                </q-tooltip>
              </q-icon>
            </template>
          </q-btn-toggle>
        </div>
      </div>
    </div>
    <div class="row justify-between">
      <div class="col-auto">
        <div class="row q-px-sm"/>
      </div>
      <div class="col-auto">
        Principal
      </div>
      <div class="col-auto">
        <div class="row q-px-sm"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MapaBloquePrincipal",
  data() {
    return {
      herramienta_estandar_activa: "desplazar"
    }
  }
}
</script>

