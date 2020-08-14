<template>
  <div class="col">
    <q-tabs
      v-model="tab"
      dense
      class="bg-grey-4 bg-animate text-grey-7"
      active-color="grey-9"
      indicator-color="primary"
      active-bg-color="grey-1"
      align="left">
      <q-tab name="proyecto" label="Proyecto" class="q-tab--no-caps tabs-title" />
      <q-tab name="vectorial" label="Vectorial" class="q-tab--no-caps tabs-title" />
      <q-tab name="raster" label="Raster" class="q-tab--no-caps tabs-title" />
      <q-tab name="herramientas" label="Herramientas" class="q-tab--no-caps tabs-title" />
    </q-tabs>

    <q-tab-panels v-model="tab" class="bg-grey-1 text-grey-9">
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
                  <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right"/>
                </div>
              </div>
            </div>
          </div>
          <q-separator vertical/>
          <div class="col q-pa-xs">
            <q-btn-dropdown
              split
              icon="home"
              flat
              @click="onMainClick"
            >
              <q-list>
                <q-item clickable v-close-popup @click="onItemClick">
                  <q-item-section avatar>
                    <q-avatar icon="folder" color="primary" text-color="white"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Photos</q-item-label>
                    <q-item-label caption>February 22, 2016</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-icon name="info" color="amber"/>
                  </q-item-section>
                </q-item>

                <q-item clickable v-close-popup @click="onItemClick">
                  <q-item-section avatar>
                    <q-avatar icon="assignment" color="secondary" text-color="white"/>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>Vacation</q-item-label>
                    <q-item-label caption>February 22, 2016</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-icon name="info" color="amber"/>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>
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
          <barra-visualizacion/>
          <q-separator vertical />


          <menu-zoom/>

        </div>
      </q-tab-panel>
    </q-tab-panels>
  </div>
</template>

<script>
import BarraHerramientas from "components/BarraHerramientas";
import MenuZoom from "components/MenuZoom";
import BarraVisualizacion from "components/BarraVisualizacion";

export default {
  name: "PrincipalTab",
  // eslint-disable-next-line vue/no-unused-components
  components: {BarraVisualizacion, MenuZoom, BarraHerramientas},
  data() {
    return {
      tab: 'herramientas'
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
