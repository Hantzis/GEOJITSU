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


    <q-page-container>
      <router-view/>
    </q-page-container>

    <!---
    <q-footer elevated class="bg-grey-9 text-grey-4">
      <q-toolbar style="min-height: 22px; font-size: 11px;">
          Geojitsu
        <q-space/>
          2020 &copy; Maptitude XYZ
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
