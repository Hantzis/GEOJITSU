<template>
  <div class="col">
    <q-tabs
      v-model="tab"
      dense
      align="left">
      <q-tab name="proyecto" label="Proyecto"/>
      <q-tab name="vectorial" label="Vectorial"/>
      <q-tab name="raster" label="Raster"/>
      <q-tab name="herramientas" label="Herramientas"/>
    </q-tabs>
    <q-separator/>
    <q-tab-panels v-model="tab" class="bg-primary text-white">
      <q-tab-panel name="proyecto" class="no-padding">
        <div class="row">
          <div class="col">
            <barra-visualizacion/>
            <barra-visualizacion/>
            <div class="row justify-end">
              <div class="col">
                <div class="row justify-center">
                  Panel de datos
                </div>
              </div>
              <div class="col">
                <div class="row justify-end">
                  <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right" />
                </div>
              </div>
            </div>
          </div>
          <q-separator vertical/>
          <div class="col">
            <barra-visualizacion/>
            <barra-visualizacion/>
          </div>
        </div>

      </q-tab-panel>

      <q-tab-panel name="vectorial" class="no-padding">
        <div class="row">
          <div class="col">
            <barra-visualizacion/>
          </div>
        </div>
      </q-tab-panel>

      <q-tab-panel name="raster" class="no-padding">
        <div class="row">
          <div class="col">
            <barra-visualizacion/>
          </div>
        </div>
      </q-tab-panel>

      <q-tab-panel name="herramientas" class="no-padding">
        <div class="row">
          <barra-herramientas/>


          <menu-zoom/>

        </div>
      </q-tab-panel>
    </q-tab-panels>
    <q-separator/>
  </div>
</template>

<script>
import BarraHerramientas from "components/BarraHerramientas";
import MenuZoom from "components/MenuZoom";
import BarraVisualizacion from "components/BarraVisualizacion";

export default {
  name: "PrincipalTab",
  components: {BarraVisualizacion, MenuZoom, BarraHerramientas},
  data() {
    return {
      tab: 'herramientas'
    }
  }
}
</script>

<style scoped>

</style>
