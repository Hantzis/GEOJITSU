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
      <q-tab v-for="(tab, index) in GISRibbonTabsEnabled" :key="index" :name="tab.name" :label="tab.label"
             class="q-tab--no-caps tabs-title"/>
    </q-tabs>

    <q-tab-panels v-model="activeTab" class="bg-grey-1 text-grey-9">

      <q-tab-panel name="proyecto" class="no-padding">
        <div class="row no-wrap">
          <div class="col-auto">
            <barra-visualizacion/>
            <barra-visualizacion/>
            <div class="row no-wrap">
              <div class="col">
                Panel de datos
              </div>
              <div class="col">
                <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right"/>
              </div>
            </div>
          </div>
          <q-separator vertical style="flex-shrink: 0"/>
          <div class="col-auto">
            <barra-visualizacion/>
            <barra-visualizacion/>
          </div>
        </div>

      </q-tab-panel>

      <q-tab-panel name="mapa" class="no-padding">
        <div class="row no-wrap q-px-sm">
          <q-separator vertical />
          <mapa-bloque-principal />

          <q-separator vertical />

          <mapa-bloque-seleccion />

          <q-separator vertical />

          <mapa-bloque-seleccion />

          <q-separator vertical />

          <mapa-bloque-seleccion />

          <q-separator vertical />

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
  import BarraVisualizacion from "components/gisribbon_components/mapa/BarraVisualizacion";
  import MapaBloquePrincipal from "./gisribbon_components/mapa/MapaBloquePrincipal";
  import MapaBloqueSeleccion from "./gisribbon_components/mapa/MapaBloqueSeleccion";

  export default {
    name: "GISRibbon",
    // eslint-disable-next-line vue/no-unused-components
    components: {
      MapaBloquePrincipal,
      MapaBloqueSeleccion,
      BarraVisualizacion,
    },
    data() {
      return {
        activeTab: 'mapa',
        GISRibbonTabs: {
          proyecto: {label: "Proyecto", is_enabled: false },
          mapa: { label: "Mapa", is_enabled: true},
          herramientas: { label: "Herramientas", is_enabled: true},
        }
      }
    },
    mounted() {
      console.log(this.GISRibbonTabsEnabled)
    },
    computed: {
      GISRibbonTabsEnabled() {
        let enabled_tabs = [];
          for (let tab of this.GISRibbonTabs) {
            if (tab.is_enabled) {
              enabled_tabs.push(tab)
              console.log(tab)
            }
        }
        return enabled_tabs
      }
    },
    methods: {
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
