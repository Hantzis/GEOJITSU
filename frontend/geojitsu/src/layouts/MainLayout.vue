<template>
  <q-layout view="lHh LpR fFf">
    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left"/>

        <q-toolbar-title>
          Maptitude XYZ
        </q-toolbar-title>
        <q-btn dense flat round icon="help" @click="testa('help')"/>
        <q-btn dense flat round icon="mdi-login" @click="testa('login')"/>
      </q-toolbar>

      <div class="row justify-between">
        <div class="col-xs-12 col-sm-7">
          <q-tabs align="left">
            <q-route-tab to="/" label="Vectorial"/>
            <q-route-tab to="/" label="Raster"/>
            <q-route-tab to="/" label="Herramientas"/>
          </q-tabs>
        </div>
        <div class="col-xs-12 col-sm-5">
          <div class="row q-pt-sm q-pr-sm justify-between">
            <div class="col">
            </div>
            <div class="col-auto">
              <div class="row justify-end">
                <div class="col-auto q-pa-xs">
                  <q-btn-toggle
                    style="border-radius: 0;"
                    v-model="model"
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
                        <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                                   self="bottom middle">
                          Desplazar mapa
                        </q-tooltip>
                      </q-icon>
                    </template>
                    <template v-slot:info>
                      <q-icon name="info">
                        <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                                   self="bottom middle">
                          Mostrar info
                        </q-tooltip>
                      </q-icon>
                    </template>
                    <template v-slot:zoom style="padding: 0">
                      <div class="qqqq">
                        <q-tooltip content-class="bg-black" content-style="font-size: 16px" anchor="top middle"
                                   self="bottom middle">
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
                    </template>
                  </q-btn-toggle>
                </div>
                <div class="col-auto q-pa-xs q-pb-sm">
                  <q-btn-toggle
                    style="border-radius: 0;"
                    v-model="toggle_drawers_model"
                    dense
                    glossy
                    color="white"
                    text-color="primary"
                    toggle-color="light-blue"
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
              </div>

            </div>

          </div>
        </div>
      </div>

    </q-header>

    <q-drawer v-model="left" side="left" bordered overlay behavior="mobile">
      <!-- drawer content -->
    </q-drawer>

    <q-drawer v-model="right" side="right" bordered :breakpoint="319" overlay >
      <!-- drawer content -->
    </q-drawer>

    <q-drawer v-model="drawer_layers" side="right" bordered :breakpoint="319" overlay>
      <q-tabs
          v-model="layers_tabs"
          dense
          class="text-grey-14"
          active-color="primary"
          indicator-color="primary"
        >
          <q-tab name="layers" icon="mail" label="Capas" />
          <q-tab name="servers" icon="mail" label="Servidores" />
          <q-tab name="basemaps" icon="mail" label="Mapas base" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="layers_tabs" animated>
          <q-tab-panel name="layers">
            <div class="text-h6">Mails</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>

          <q-tab-panel name="servers">
            <div class="text-h6">Alarms</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>

          <q-tab-panel name="basemaps">
            <div class="text-h6">Movies</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>
        </q-tab-panels>
    </q-drawer>

    <q-drawer v-model="drawer_grid" side="right" bordered :breakpoint="319" overlay>
      Drawer de atributos
    </q-drawer>

    <q-drawer v-model="drawer_stats" side="right" bordered :breakpoint="319" overlay>
      Drawer de stats
    </q-drawer>

    <q-drawer v-model="drawer_charts" side="right" bordered :breakpoint="319" overlay>
      Drawer de charts
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>

    <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          2020 &copy; Maptitude XYZ
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
  export default {
    data() {
      return {
        left: false,
        right: false,
        drawer_layers: false,
        drawer_grid: false,
        drawer_stats: false,
        drawer_charts: false,
        model: 'mover',
        toggle_drawers_model: 'hide',
        layers_tabs: 'layers'
      }
    },
    methods: {
      testa(val) {
        alert(val);
      },
      onMainClick() {
        console.log('Clicked on main button')
      },

      onItemClick() {
        console.log('Clicked on an Item')
      }
    },
    watch: {
      model() {
        console.log(this.model)
      },
      toggle_drawers_model() {
        console.log(this.toggle_drawers_model)
        if (this.toggle_drawers_model == 'hide') {
          this.drawer_layers = false;
          this.drawer_grid = false;
          this.drawer_stats = false;
          this.drawer_charts = false;
        }
        if (this.toggle_drawers_model == 'layers') {
          this.drawer_layers = true;
          this.drawer_grid = false;
          this.drawer_stats = false;
          this.drawer_charts = false;
        }
        if (this.toggle_drawers_model == 'grid') {
          this.drawer_layers = false;
          this.drawer_grid = true;
          this.drawer_stats = false;
          this.drawer_charts = false;
        }
        if (this.toggle_drawers_model == 'stats') {
          this.drawer_layers = false;
          this.drawer_grid = false;
          this.drawer_stats = true;
          this.drawer_charts = false;
        }
        if (this.toggle_drawers_model == 'charts') {
          this.drawer_layers = false;
          this.drawer_grid = false;
          this.drawer_stats = false;
          this.drawer_charts = true;
        }
      }
    }
  }
</script>

<style lang="scss">
  .q-drawer--right {
    z-index: 999;
    border-left: 1px solid rgba(0, 0, 0, 0.12);
  }

  .btn {
    padding: 3px; /* qyutar ? */
  }

  .q-btn--dense .q-btn__wrapper {
    padding: 0 0.14em;
  }

  .1
  q-btn__wrapper .col .row .q-anchor--skip {
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

  .material-icons.q-icon.notranslate.q-btn-dropdown__arrow {
    width: 0.6em;
    /* padding-left: 0.1em;  posiblemente quitar */
  }

  .q-btn__desplegable .q-btn--dense.q-btn__wrapper {
    padding: 0;
  }

  .q-btn__desplegable.no-border-radius .q-btn.q-btn-item.non-selectable.no-outline.q-btn--flat.q-btn--rectangle.q-btn--actionable.q-focusable.q-hoverable.q-btn-dropdown--current {
    padding: 0 0.14em;
  }

  .qqqq .q-btn__wrapper.col.row.q-anchor--skip {
    padding: 0;
  }

  .q-btn.q-btn-item.non-selectable.no-outline.q-btn--flat.q-btn--rectangle.q-btn--actionable.q-focusable.q-hoverable.q-btn-dropdown--current {
    padding: 0;
  }

  .qqqq .material-icons.q-icon.notranslate.q-btn-dropdown__arrow {
    font-size: 1em;
    padding: 0 2.5px 0 2px;
  }

  .q-menu {
    border-radius: 0;
  }

</style>
