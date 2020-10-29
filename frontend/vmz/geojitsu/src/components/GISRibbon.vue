<template>
  <div>

    <q-toolbar style="padding: 0" v-show="showGISRibbon" v-model="activeTab" class="bg-white text-grey-9">

      <div name="mapa" class="no-padding">
        <div class="row no-wrap">

          <mapa-bloque-principal/>

          <q-separator vertical/>

          <mapa-bloque-capas/>

          <q-separator vertical/>

          <mapa-bloque-mapa-base />

          <q-separator vertical/>

        </div>

      </div>



    </q-toolbar>
    <q-separator color="grey-5"/>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

import MapaBloquePrincipal from "./gisribbon_components/mapa/MapaBloquePrincipal";
import MapaBloqueCapas from "components/gisribbon_components/mapa/MapaBloqueCapas";
import MapaBloqueMapaBase from "components/gisribbon_components/mapa/MapaBloqueMapaBase";

export default {
  name: "GISRibbon",
  // eslint-disable-next-line vue/no-unused-components
  components: {
    MapaBloqueCapas,
    MapaBloquePrincipal,
    MapaBloqueMapaBase,
  },
  data() {
    return {
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
