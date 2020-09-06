<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs q-pt-xs1 q-pl-xs q-pr-xs">
          <q-btn-toggle
            class="bloque"
            v-model="herramientaSeleccion"
            dense
            :disable="!BloqueSeleccionIsEnabled"
            unelevated
            text-color="grey-7"
            toggle-text-color="white"
            toggle-color="primary"
            :options="[
              {value: 'rectangulo', slot: 'rectangulo'},
              {value: 'poligono', slot: 'poligono'},
              {value: 'atributos', slot: 'atributos'},
              {value: 'limpiar', slot: 'limpiar'},
              {value: 'lazo', slot: 'lazo'},
              {value: 'seleccionar-todo', slot: 'seleccionar-todo'},
              {value: 'invertir', slot: 'invertir'},
              {value: 'limpiar-todo', slot: 'limpiar-todo'},
            ]"
          >
            <template v-slot:rectangulo>
              <q-icon name="mdi-selection-drag">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;" anchor="top middle"
                           self="bottom middle">
                  Seleccionar objetos
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:poligono>
              <q-icon name="mdi-shape-polygon-plus">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;"
                           anchor="top middle"
                           self="bottom middle">
                  Seleccionar con polígono
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:atributos>
              <q-icon name="mdi-form-textbox">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;"
                           anchor="top middle"
                           self="bottom middle">
                  Seleccionar por atributos
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:limpiar>
              <q-icon name="mdi-selection-off">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;"
                           anchor="top middle"
                           self="bottom middle">
                  Limpiar selección
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:lazo>
              <q-icon name="mdi-sine-wave">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;"
                           anchor="top middle"
                           self="bottom middle">
                  Seleccionar a mano alzada
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:seleccionar-todo>
              <q-icon name="mdi-select-all">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;"
                           anchor="top middle"
                           self="bottom middle">
                  Seleccionar todo
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:invertir>
              <q-icon name="mdi-select-inverse">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;"
                           anchor="top middle"
                           self="bottom middle">
                  Invertir selección
                </q-tooltip>
              </q-icon>
            </template>
            <template v-slot:limpiar-todo>
              <q-icon name="mdi-square-off">
                <q-tooltip v-if="BloqueSeleccionIsEnabled" content-class="bg-black"
                           content-style="font-size: 16px; border-radius: 0;"
                           anchor="top middle"
                           self="bottom middle">
                  Limpiar selección (todas las capas)
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
               style="border-radius: 0; margin-bottom: 0; margin-right: 1px;"/>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "MapaBloquePrincipal",
  data() {
    return {
      herramientaSeleccion: undefined,
      BloqueSeleccionIsEnabled: true
    }
  }
}
</script>

<style lang="css" scoped>
.bloque {
  border-radius: 0;
  flex-wrap: wrap;
  max-width: 128px;
}

.bloque >>> .disabled,
.bloque >>> .disabled *,
.bloque >>> [disabled],
.bloque >>> [disabled] * {
  cursor: initial !important;
}
</style>
