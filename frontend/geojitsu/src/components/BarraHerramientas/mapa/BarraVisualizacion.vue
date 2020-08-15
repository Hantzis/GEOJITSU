<template>
  <div class="row q-pa-xs q-pt-xs1 q-pl-xs q-pr-xs">
    <q-btn-toggle
      style="border-radius: 0;"
      v-model="toggle_drawers_model"
      dense
      unelevated
      text-color="grey-6"
      toggle-text-color="white"
      toggle-color="primary"
      size="md"
      :options="[
        {value: 'hide', slot: 'hide'},
        {value: 'layers', slot: 'layers'},
        {value: 'grid', slot: 'grid'},
        {value: 'stats', slot: 'stats'},
        {value: 'charts', slot: 'charts'}
      ]"
    >
      <template v-slot:hide>
        <q-icon name="mdi-eye-off">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Ocultar panel
          </q-tooltip>
        </q-icon>
      </template>
      <template v-slot:layers>
        <q-icon name="mdi-layers">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Capas de información
          </q-tooltip>
        </q-icon>
      </template>
      <template v-slot:grid>
        <q-icon name="mdi-grid">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Tabla de atributos
          </q-tooltip>
        </q-icon>
      </template>
      <template v-slot:stats>
        <q-icon name="mdi-sigma">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Resumen
          </q-tooltip>
        </q-icon>
      </template>
      <template v-slot:charts>
        <q-icon name="mdi-chart-bar">
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
  name: "BarraVisualizacion",
  data() {
    return {
      toggle_drawers_model: "hide"
    }
  }
}
</script>
