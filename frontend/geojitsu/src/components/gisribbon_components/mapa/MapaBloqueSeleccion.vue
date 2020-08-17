<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs q-pt-xs1 q-pl-xs q-pr-xs">
          <q-btn-toggle
            class="wrapp"
            style="border-radius: 0; flex-wrap: wrap; max-width: 128px;"
            v-model="herramienta_seleccion_activa"
            dense
            unelevated
            text-color="grey-7"
            toggle-text-color="white"
            toggle-color="primary"
            :options="[
        {value: 'seleccion-objetos', slot: 'seleccion-objetos'},
        {value: 'info', slot: 'info'},
        {value: 'zoom-in', slot: 'zoom-in'},
        {value: 'seleccion', slot: 'seleccion'},
        {value: 'medicion', slot: 'medicion'},
        {value: 'zoom-out', slot: 'zoom-out'},
        {value: 'zoom-out', slot: 'zoom-out'},
        {value: 'zoom-out', slot: 'zoom-out'},
      ]"
          >
            <template v-slot:seleccion-objetos>
              <q-icon name="mdi-selection-drag">
                <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Ocultar panel
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:zoom-in>
              <q-icon name="mdi-magnify-plus">
                <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Capas de información
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:seleccion>
              <q-icon name="mdi-selection-drag">
                <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Tabla de atributos
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:info>
              <q-icon name="mdi-information">
                <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Resumen
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:zoom-out>
              <q-icon name="mdi-magnify-minus">
                <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Gráficas
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:medicion>
              <q-icon name="mdi-ruler">
                <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                           self="bottom middle">
                  Gráficas
                </q-tooltip>
              </q-icon>
            </template>
          </q-btn-toggle>
        </div>
      </div>
    </div>
    <!-- <div class="row" style="padding: 20px;"></div> -->
    <div class="row justify-between">
      <div class="col-auto">
        <div class="row q-px-sm"/>
      </div>
      <div class="col-auto">
        Selección
      </div>
      <div class="col-auto">
        <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right"
               style="border-radius: 0; margin-bottom: -3px; margin-right: -1px;"/>
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
