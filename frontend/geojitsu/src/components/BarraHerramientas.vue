<template>
  <div class="col-auto q-pa-xs">
    <q-btn-toggle
      style="border-radius: 0;"
      v-model="opcion"
      dense
      glossy
      color="white"
      text-color="primary"
      toggle-color="light-blue"
      :options="[
        {value: 'mover', slot: 'mover'},
        {value: 'info', slot: 'info'},
        {value: 'zoom', slot: 'zoom'},
        {value: 'seleccion', slot: 'seleccion'},
        {value: 'medicion', slot: 'medicion'}
      ]"
    >
      <template v-slot:mover>
        <q-icon name="mdi-hand-right">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle" self="bottom middle">
            Desplazar mapa
          </q-tooltip>
        </q-icon>
      </template>
      <template v-slot:info>
        <q-icon name="info">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle" self="bottom middle">
            Mostrar info
          </q-tooltip>
        </q-icon>
      </template>
      <template v-slot:zoom>
        <div>
          <q-btn-dropdown
            split
            class="glossy"
            color="teal"
            label="Folders"
            @click="onMainClick"
          >
          </q-btn-dropdown>
        </div>
      </template>
      <!-- <template v-slot:zoom style="padding: 0">
        <div class="margenminimoboton">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle" self="bottom middle">
            Zoom general
          </q-tooltip>
          <q-btn-dropdown
            split
            flat
            icon="mdi-arrow-expand-all"
            @click="onMainClick"
            class="q-btn__desplegable no-border-radius"
            style="margin: 0 -0.14em;"
          >
            <q-list dense>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-arrow-expand-all" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Zoom general</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-layers-search" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Zoom a la capa activa</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-select-search" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Zoom a la selección</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </template>
      <template v-slot:seleccion style="padding: 0">
        <div class="qqqq">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Seleccionar objetos
          </q-tooltip>
          <q-btn-dropdown
            split
            flat
            icon="mdi-selection-drag"
            @click="onMainClick"
            class="q-btn__desplegable no-border-radius"
            style="margin: 0 -0.14em;"
          >
            <q-list dense>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-selection-drag" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar objetos</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-shape-polygon-plus" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar dibujando un polígono</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-gesture" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar a mano alzada</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-form-textbox-password" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar por atributos</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-select-all" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar todos</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-select-inverse" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Invertir selección</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-selection-off" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Eliminar selección</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </template>
      <template v-slot:medicion style="padding: 0">
        <div class="qqqq">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Medir distancia
          </q-tooltip>
          <q-btn-dropdown
            split
            flat
            icon="mdi-ruler"
            @click="onMainClick"
            class="q-btn__desplegable no-border-radius"
            style="margin: 0 -0.14em;"
          >
            <q-list dense>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-ruler" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Medir distancia</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-texture-box" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Medir área</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-angle-acute" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Medir ángulo</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </template> -->
    </q-btn-toggle>
  </div>
</template>

<script>
export default {
  name: "BarraHerramientas",
  data() {
    return {
      opcion: 'mover',
    }
  },
  methods: {
    onMainClick() {
      console.log('Clicked on main button')
    },
  }
}
</script>

<style lang="scss" scoped>

.q-btn__wrapper.col.row.q-anchor--skip {
  padding: 110px;
}
/*
.q-btn__wrapper .col .row .q-anchor--skip {
  padding: 0;
}

.q-list--dense > .q-item, .q-item--dense {
  padding: 2px 4px;
}

.q-focus-helper > .q-item__section--side {
  padding-right: 36px;
}

.q-btn-dropdown--split .q-btn-dropdown__arrow-container .q-btn__wrapper {
  padding: 0;
}

.material-icons.q-icon.notranslate.q-btn-dropdown__arrow222222222222222 {
  width: 0.6em;
}

.q-btn__desplegable .q-btn--dense.q-btn__wrapper {
  padding: 0;
}

.q-btn__desplegable.no-border-radius .q-btn.q-btn-item.non-selectable.no-outline.q-btn--flat.q-btn--rectangle.q-btn--actionable.q-focusable.q-hoverable.q-btn-dropdown--current {
  padding: 0 0.14em;
}

.margenminimoboton .q-btn__wrapper.col.row.q-anchor--skip {
  padding: 0;
}

.q-btn.q-btn-item.non-selectable.no-outline.q-btn--flat.q-btn--rectangle.q-btn--actionable.q-focusable.q-hoverable.q-btn-dropdown--current {
  padding: 0;
}

.margenminimoboton .material-icons.q-icon.notranslate.q-btn-dropdown__arrow {
  font-size: 1em;
  padding: 0 2.5px 0 2px;
}
*/

</style>
