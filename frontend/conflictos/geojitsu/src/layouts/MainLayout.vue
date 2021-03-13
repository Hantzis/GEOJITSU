<template>
  <q-layout view="LHH LPR FFF">
    <q-header class="bg-black text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left"/>

        <q-toolbar-title>
          Maptitude XYZ
        </q-toolbar-title>
        <q-btn v-if="this.$route.path==='/'" dense flat round
               :icon="showGISRibbon ? 'mdi-chevron-up' : 'mdi-chevron-down'"
               @click="showGISRibbon = !showGISRibbon">
          <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            {{ showGISRibbon ? "Ocultar cinta" : "Mostrar cinta" }}
          </q-tooltip>
        </q-btn>

        <q-btn dense flat round icon="mdi-dots-vertical">
          <q-menu content-style="border-radius: 2px;">
            <q-list style="min-width: 130px;">
              <q-item dense clickable v-close-popup style="padding: 0;" @click="inicioDialog=true">
                <q-avatar>
                  <q-icon name="info"/>
                </q-avatar>
                <q-item-section>Acerca de</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>

    </q-header>

    <q-drawer v-model="left" side="left" elevated overlay behavior="mobile">
      <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd">
        <q-list padding>
          <q-item to="/" clickable v-ripple exact>
            <q-item-section avatar>
              <q-icon name="home"/>
            </q-item-section>

            <q-item-section>
              Mapa
            </q-item-section>

          </q-item>

          <q-item to="acerca" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-information"/>
            </q-item-section>

            <q-item-section>
              Acerca de
            </q-item-section>
          </q-item>

          <q-item to="metodologia" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-file-edit"/>
            </q-item-section>

            <q-item-section>
              Metodología
            </q-item-section>
          </q-item>

        </q-list>
      </q-scroll-area>
      <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/logo_unam.jpg" alt="UNAM">
          </q-avatar>
          <div class="text-weight-bold">Conflictos Socioambientales de México</div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>

    <q-dialog v-model="inicioDialog">
      <q-card>
        <q-card-section class="row items-center no-wrap ">
          <q-avatar icon="mdi-map" color="black" text-color="white" style="margin-right: 14px; align-self: end;"/>
          <div class="text-h6">{{ paginaInicio.title }}</div>
          <q-space/>
          <q-btn icon="close" flat round dense v-close-popup @click="inicioDialog=false" style="align-self: start;"/>
        </q-card-section>

        <q-separator/>

        <q-card-section style="max-height: 50vh" class="scroll">
          <div v-for="item of paginaInicio.cuerpo" :key="item.id">
            <div v-if="item.type=='paragraph_block'" v-html="item.value"></div>
          </div>
        </q-card-section>

        <q-separator/>

        <q-card-actions align="right">
          <q-btn unelevated no-caps label="Cerrar" color="green" v-close-popup/>
        </q-card-actions>
      </q-card>
    </q-dialog>

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
      inicioDialog: false,
      left: false,
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getPaginaInicio']),
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      },
      set(value) {
        this.GISRibbonIsOpenAction(value)
      }
    },
    paginaInicio: {
      get() {
        return this.getPaginaInicio
      },
      set(value) {
        this.setPaginaInicio(value)
      }
    },
  },
  methods: {
    ...mapActions('geojitsu', ['GISRibbonIsOpenAction', 'setPaginaInicio']),
    testa(val) {
      alert(val);
    },
  },
  mounted() {
    this.inicioDialog = true
  }
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
