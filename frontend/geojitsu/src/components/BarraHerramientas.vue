<template>
  <div class="col-auto q-pa-xs prueba">
    <q-btn-toggle
      style="border-radius: 0;"
      v-model="opcion"
      dense
      glossy
      color="white"
      text-color="primary"
      toggle-color="orange"
      :options="[
        {value: 'mover', slot: 'mover'},
        {value: 'info', slot: 'info'},
        {value: 'zoom', slot: 'zoom', opciones: [1,2,3]},
        {value: 'seleccion', slot: 'seleccion'},
        {value: 'medicion', slot: 'medicion'},
        {value: 'mover2', slot: 'mover2'}

      ]"
    >
      <template v-slot:mover>
        <q-icon name="mdi-hand-right">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Desplazar mapa
          </q-tooltip>
        </q-icon>
      </template>

      <q-separator vertical/>
      <template v-slot:info>
        <q-icon name="info">
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Mostrar info
          </q-tooltip>
        </q-icon>
      </template>
      <template v-slot:zoom>
        <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle" self="bottom middle">
          Zoom general
        </q-tooltip>
        <q-btn-dropdown
          split
          flat
          icon="mdi-arrow-expand-all"
          @click="onMainClick"
          class="no-border-radius"
        >
          <q-list dense bordered>
            <q-item dense clickable v-close-popup @click="onItemClick">
              <q-item-section side style="padding-right: 6px;">
                <q-icon name="mdi-arrow-expand-all" color="primary"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>Zoom general</q-item-label>
              </q-item-section>
            </q-item>
            <q-item dense clickable v-close-popup @click="onItemClick">
              <q-item-section side style="padding-right: 6px;">
                <q-icon name="mdi-layers-search" color="primary"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>Zoom a la capa activa</q-item-label>
              </q-item-section>
            </q-item>
            <q-item dense clickable v-close-popup @click="onItemClick">
              <q-item-section side style="padding-right: 6px;">
                <q-icon name="mdi-select-search" color="primary"/>
              </q-item-section>
              <q-item-section>
                <q-item-label>Zoom a la selección</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </template>
      <template v-slot:seleccion>
        <div>
          <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Seleccionar objetos
          </q-tooltip>
          <q-btn-dropdown
            split
            flat
            icon="mdi-selection-drag"
            @click="onMainClick"
            class="no-border-radius"
          >
            <q-list dense>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-selection-drag" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar objetos</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-shape-polygon-plus" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar dibujando un polígono</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-gesture" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar a mano alzada</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-form-textbox-password" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar por atributos</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-select-all" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Seleccionar todos</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-select-inverse" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Invertir selección</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
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
        <div>
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
          >
            <q-list dense>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-ruler" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Medir distancia</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
                <q-item-section side style="padding-right: 6px;">
                  <q-icon name="mdi-texture-box" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>Medir área</q-item-label>
                </q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup @click="onItemClick">
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
      </template>
      <template v-slot:mover2>
        <boton-barra-herramientas/>
      </template>
    </q-btn-toggle>
  </div>

</template>

<script>
  import BotonBarraHerramientas from "./BarraHerramientas/BotonBarraHerramientas";

  export default {
    name: "BarraHerramientas",
    components: {BotonBarraHerramientas},
    data() {
      return {
        opcion: 'mover',
      }
    },
    methods: {
      onMainClick() {
        console.log('Clicked on main button')
      },
      onItemClick() {
        console.log('Clicked on an Item')
      }
    }
  }
</script>

<style lang="css" scoped>
  .q-menu > .q-list--dense > .q-item--dense {
    padding: 4px 12px 4px 4px;
  }

  .prueba >>> .q-btn-group button:nth-child(3) span:nth-child(2),
  .prueba >>> .q-btn-group button:nth-child(4) span:nth-child(2),
  .prueba >>> .q-btn-group button:nth-child(5) span:nth-child(2) {
    padding: 0;
  }

  .prueba >>> .q-btn__wrapper {
    min-height: 2.6em;
    min-width: 2.6em;
  }



  .prueba >>> .q-btn-group button:nth-child(3) span:nth-child(2) button:nth-child(2) span.q-btn__wrapper,
  .prueba >>> .q-btn-group button:nth-child(4) span:nth-child(2) button:nth-child(2) span.q-btn__wrapper,
  .prueba >>> .q-btn-group button:nth-child(5) span:nth-child(2) button:nth-child(2) span.q-btn__wrapper {
    min-width: 19px;
    width: 19px;
  }
</style>

