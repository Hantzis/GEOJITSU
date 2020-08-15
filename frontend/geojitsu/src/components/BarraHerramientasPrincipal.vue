<template>
  <div class="row q-pa-xs q-pt-xs1 q-pl-xs q-pr-xs">
    <q-btn-toggle
      class="wrapp"
      style="border-radius: 0; flex-wrap: wrap; max-width: 96px"
      v-model="herramienta_estandar_activa"
      dense
      unelevated
      text-color="grey-6"
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
</template>

<script>
export default {
  name: "BarraHerramientasPrincipal",
  data() {
    return {
      herramienta_estandar_activa: "desplazar"
    }
  }
}
</script>

<style scoped>

</style>
