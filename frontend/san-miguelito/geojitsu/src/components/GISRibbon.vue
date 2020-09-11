<template>
  <div>
    <q-tabs
      v-model="activeTab"
      dense
      class="bg-grey-4 text-grey-7"
      active-color="grey-9"
      indicator-color="primary"
      active-bg-color="grey-1"
      align="left">
      <q-tab v-for="(tab, index) in GISRibbonEnabledTabs" :key="index" :name="tab[0]" :label="tab[1].label"
             class="q-tab--no-caps tabs-title" @click="showGISRibbon = true"/>
    </q-tabs>

    <q-tab-panels v-show="showGISRibbon" v-model="activeTab" class="bg-grey-1 text-grey-9">

      <q-tab-panel name="mapa" class="no-padding">
        <div class="row no-wrap">
          <q-separator vertical/>

          <mapa-bloque-principal/>

          <!-- <q-separator vertical/>

          <mapa-bloque-seleccion/> -->

          <q-separator vertical/>

          <mapa-bloque-capas/>

          <q-separator vertical/>

          <mapa-bloque-mapa-base />

          <q-separator vertical/>

        </div>

      </q-tab-panel>

      <q-tab-panel name="herramientas" class="no-padding">
        <div class="row no-wrap" style="padding: 46.5px;">
        </div>

      </q-tab-panel>

    </q-tab-panels>
    <q-separator color="grey-5"/>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

//import BarraVisualizacion from "components/gisribbon_components/mapa/BarraVisualizacion";
import MapaBloquePrincipal from "./gisribbon_components/mapa/MapaBloquePrincipal";
//import MapaBloqueSeleccion from "./gisribbon_components/mapa/MapaBloqueSeleccion";
import MapaBloqueCapas from "components/gisribbon_components/mapa/MapaBloqueCapas";
import MapaBloqueMapaBase from "components/gisribbon_components/mapa/MapaBloqueMapaBase";

export default {
  name: "GISRibbon",
  // eslint-disable-next-line vue/no-unused-components
  components: {
    MapaBloqueCapas,
    MapaBloquePrincipal,
//    MapaBloqueSeleccion,
//    BarraVisualizacion,
    MapaBloqueMapaBase,
  },
  data() {
    return {
      activeTab: 'mapa',
      GISRibbonTabs: {
        proyecto: {label: "Proyecto", is_enabled: false},
        mapa: {label: "Mapa", is_enabled: true},
        //herramientas: {label: "Herramientas", is_enabled: true},
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
