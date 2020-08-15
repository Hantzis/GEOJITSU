<template>
  <div>
    <q-tabs
      v-model="tab"
      dense
      class="bg-grey-4 bg-animate text-grey-7"
      active-color="grey-9"
      indicator-color="primary"
      active-bg-color="grey-1"
      align="left">
      <q-tab v-if="false" name="proyecto" label="Proyecto" class="q-tab--no-caps tabs-title" />
      <q-tab name="mapa" label="Mapa" class="q-tab--no-caps tabs-title" />
      <!-- <q-tab name="vectorial" label="Vectorial" class="q-tab--no-caps tabs-title" />
      <q-tab name="raster" label="Raster" class="q-tab--no-caps tabs-title" />
      <q-tab name="herramientas" label="Herramientas" class="q-tab--no-caps tabs-title" /> -->
    </q-tabs>

    <q-tab-panels v-model="tab" class="bg-grey-1 text-grey-9">
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
        <div class="row no-wrap">
          <mapa-bloque-principal />

          <q-separator vertical style="flex-shrink: 0"/>

          <div class="col-auto">
            <div class="row">
              <div class="col">
                <barra-visualizacion/>
              </div>
            </div>
            <div class="row justify-between">
              <div class="col-auto">
                <div class="row q-px-sm"/>
              </div>
              <div class="col-auto items-end">
                Selección
              </div>
              <div class="col-auto">
                <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right"/>
              </div>
            </div>
          </div>

          <q-separator vertical style="flex-shrink: 0"/>

        </div>

      </q-tab-panel>


    </q-tab-panels>
    <q-separator color="grey-5"/>
  </div>
</template>

<script>
  import BarraHerramientas from "components/BarraHerramientas";
  import MenuZoom from "components/MenuZoom";
  import BarraVisualizacion from "components/BarraVisualizacion";
  import BarraHerramientasPrincipal from "./BarraHerramientasPrincipal";
  import MapaBloquePrincipal from "./BarraHerramientas/mapa/MapaBloquePrincipal";

  export default {
    name: "PrincipalTab",
    // eslint-disable-next-line vue/no-unused-components
    components: {MapaBloquePrincipal, BarraHerramientasPrincipal, BarraVisualizacion, MenuZoom, BarraHerramientas},
    data() {
      return {
        tab: 'mapa'
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
</style>
