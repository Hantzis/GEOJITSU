<template>
  <q-layout view="LHH LPR FFF">
    <q-header class="bg-black text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left"/>

        <q-toolbar-title>
          Maptitude XYZ
        </q-toolbar-title>
        <q-btn v-if="this.$route.path==='/'" dense flat round
               :icon="showGISRibbon ? 'mdi-arrow-collapse-up' : 'mdi-arrow-collapse-down'"
               @click="showGISRibbon = !showGISRibbon">
          <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            {{ showGISRibbon ? "Ocultar cinta" : "Mostrar cinta" }}
          </q-tooltip>
        </q-btn>

        <q-btn dense flat round icon="mdi-dots-vertical">
          <q-menu content-style="border-radius: 2px;">
            <q-list style="min-width: 130px;">
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="info"/>
                </q-avatar>
                <q-item-section>Acerca de</q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="mdi-clippy"/>
                </q-avatar>
                <q-item-section>Ayuda</q-item-section>
              </q-item>
              <q-separator/>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="login"/>
                </q-avatar>
                <q-item-section>Ingresar</q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="logout"/>
                </q-avatar>
                <q-item-section>Salir</q-item-section>
              </q-item>
              <q-separator/>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="mdi-cog"/>
                </q-avatar>
                <q-item-section>Ajustes</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>

    </q-header>

    <!--
    <q-drawer v-model="left" side="left" bordered overlay behavior="mobile">
      drawer content
    </q-drawer>

    <q-drawer v-model="right" side="right" bordered :breakpoint="319" overlay>
      - drawer content -
    </q-drawer>

    <q-drawer v-model="drawer_layers" side="right" bordered :breakpoint="319" overlay>
      <q-tabs
        v-model="layers_tabs"
        dense
        class="text-grey-14"
        active-color="primary"
        indicator-color="primary"
      >
        <q-tab name="layers" icon="mail" label="Capas"/>
        <q-tab name="servers" icon="mail" label="Servidores"/>
        <q-tab name="basemaps" icon="mail" label="Mapas base"/>
      </q-tabs>

      <q-separator/>

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
    -->

    <q-page-container>
      <router-view/>
    </q-page-container>

    <!--- <q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          2020 &copy; Maptitude XYZ
        </q-toolbar-title>
      </q-toolbar>
    </q-footer> -->

  </q-layout>
</template>

<script>
import {mapGetters} from 'vuex'
import {mapActions} from 'vuex'

export default {
  data() {
    return {
      left: false,
      right: false,
      drawer_layers: false,
      drawer_grid: false,
      drawer_stats: false,
      drawer_charts: false,
      toggle_drawers_model: 'hide',
      layers_tabs: 'layers',
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
    }
  },
  methods: {
    ...mapActions('geojitsu', ['GISRibbonIsOpenAction']),
    testa(val) {
      alert(val);
    },
  },
  watch: {
    toggle_drawers_model() {
      console.log(this.toggle_drawers_model)
      if (this.toggle_drawers_model === 'hide') {
        this.drawer_layers = false;
        this.drawer_grid = false;
        this.drawer_stats = false;
        this.drawer_charts = false;
      }
      if (this.toggle_drawers_model === 'layers') {
        this.drawer_layers = true;
        this.drawer_grid = false;
        this.drawer_stats = false;
        this.drawer_charts = false;
      }
      if (this.toggle_drawers_model === 'grid') {
        this.drawer_layers = false;
        this.drawer_grid = true;
        this.drawer_stats = false;
        this.drawer_charts = false;
      }
      if (this.toggle_drawers_model === 'stats') {
        this.drawer_layers = false;
        this.drawer_grid = false;
        this.drawer_stats = true;
        this.drawer_charts = false;
      }
      if (this.toggle_drawers_model === 'charts') {
        this.drawer_layers = false;
        this.drawer_grid = false;
        this.drawer_stats = false;
        this.drawer_charts = true;
      }
    }
  },
}
</script>

<style lang="css" scoped>
.q-drawer--right {
  z-index: 999;
  border-left: 1px solid rgba(0, 0, 0, 0.12);
}

.top-menu {
  border-radius: 0;
}
</style>
