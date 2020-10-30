<template>
  <div>


    <q-toolbar style="padding: 0" v-show="showGISRibbon" v-model="activeTab" class="bg-white text-grey-9">
      <div name="mapa" class="no-padding">

          <div class="row no-wrap">

            <div class="col-auto">
              <div class="row">
                <div class="col align-stretch">
                  <div class="row q-pa-xs q-pt-xs1 q-pl-xs q-pr-xs">
                    <q-btn-toggle
                      style="border-radius: 0;"
                      v-model="herramienta_activa"
                      unelevated
                      text-color="grey-7"
                      toggle-text-color="white"
                      toggle-color="primary"
                      :options="[
                      {value: 'info', slot: 'info'},
                      {value: 'agregar_domicilio', slot: 'agregar_domicilio'},
                      {value: 'agregar_marcador', slot: 'agregar_marcador'},
                    ]"
                    >
                      <template v-slot:info>
                        <q-icon name="mdi-information" size="lg" style="margin: 0 -10px 0 -10px;">
                          <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                     anchor="top middle"
                                     self="bottom middle">
                            Obtener información de un punto
                          </q-tooltip>
                        </q-icon>
                      </template>
                      <template v-slot:agregar_domicilio>
                        <q-icon name="mdi-playlist-plus" size="lg" style="margin: 0 -10px 0 -10px;">
                          <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                     anchor="top middle"
                                     self="bottom middle">
                            Agregar nuevo reporte mediante domicilio
                          </q-tooltip>
                        </q-icon>
                      </template>
                      <template v-slot:agregar_marcador>
                        <q-icon name="mdi-map-marker-plus" size="lg" style="margin: 0 -10px 0 -10px;">
                          <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                     anchor="top middle"
                                     self="bottom middle">
                            Agregar nuevo reporte ubicando en el mapa
                          </q-tooltip>
                        </q-icon>
                      </template>
                    </q-btn-toggle>
                  </div>
                </div>
              </div>
              <div class="row justify-between" style="margin-top: 18px;">
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

            <q-separator vertical/>

            <mapa-bloque-mapa-base/>

            <q-separator vertical/>

          </div>

      </div>
    </q-toolbar>


    <q-separator color="grey-5"/>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

import MapaBloqueMapaBase from "components/gisribbon_components/mapa/MapaBloqueMapaBase";

export default {
  name: "GISRibbon",
  // eslint-disable-next-line vue/no-unused-components
  components: {
    MapaBloqueMapaBase,
  },
  data() {
    return {
      herramienta_activa: "desplazar",
      activeTab: 'mapa',
      GISRibbonTabs: {
        proyecto: {label: "Proyecto", is_enabled: false},
        mapa: {label: "Mapa", is_enabled: true},
        herramientas: {label: "Herramientas", is_enabled: true},
      }
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter']),
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      },
      set(value) {
        this.GISRibbonIsOpenAction(value)
      }
    },
    GISRibbonEnabledTabs() {
      let enabled_tabs = [];
      for (let tab of Object.entries(this.GISRibbonTabs)) {
        if (tab[1].is_enabled) {
          enabled_tabs.push(tab)
        }
      }
      return enabled_tabs
    }
  },
  methods: {
    ...mapActions('geojitsu', ['GISRibbonIsOpenAction']),
    onMainClick(e) {
      console.log(e);
      console.log("onMainClick")
    },
    onItemClick(e) {
      console.log(e);
      console.log("onItemClick")
    }
  }
}
</script>

<style lang="css" scoped>
.tabs-title >>> .q-tab__label {
  font-size: 16px;
  font-weight: 300;
}

.q-separator--vertical {
  flex-shrink: 0;
}
</style>
