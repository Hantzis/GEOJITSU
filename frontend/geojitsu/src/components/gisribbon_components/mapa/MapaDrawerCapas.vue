<template>
  <q-drawer
    elevated
    v-model="drawerCapas"
    show-if-above
    side="right"
    :breakpoint="319"
  >
    <q-layout view="lHh lpr lFf" :style="{'min-height': mapHeight, 'max-height': mapHeight}">
      <q-header>
        <q-bar class="bg-grey-4 text-grey-9">
          <q-icon name="mdi-layers-triple"/>
          <div>Capas</div>
          <q-space/>
          <q-btn dense flat icon="close" @click="drawerCapas = false">
            <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                       self="bottom middle">
              Cerrar panel de capas
            </q-tooltip>
          </q-btn>
        </q-bar>
      </q-header>

      <q-page-container>
        <q-page style="height: inherit; min-height: inherit">

          <q-input
            ref="filter"
            square
            outlined
            v-model="filter"
            label="Filtrar"
            style="padding-right: 0px;"
            dense
          >
            <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                       self="bottom middle">
              Filtrar y listar solo las capas que coinciden
            </q-tooltip>
            <template v-slot:prepend>
              <q-icon name="mdi-filter"/>
            </template>
            <template v-slot:append>
              <q-icon v-if="filter !== ''" name="clear" class="cursor-pointer" @click="resetFilter"/>
            </template>
          </q-input>

          <q-tree
            color="grey-8"
            class="q-pt-xs capas-qtree"
            :nodes="capasMapa"
            node-key="value"
            tick-strategy="strict"
            :selected.sync="capaSeleccionada"
            :ticked.sync="capasTicked"
            :expanded.sync="expanded"
            :filter="filter"
            :filter-method="myFilterMethod"
            selected-color="primary"
          >
            <template v-slot:default-header="prop">
              {{ String(prop.node.label) | truncate(24, '...') }}
              <q-space/>
              <q-btn-group flat >
                <q-btn dense flat color="grey-8"  icon="mdi-chevron-up" size="xs" @click.stop.prevent="print('arriba')"></q-btn>
                <q-btn dense flat color="grey-8" icon="mdi-chevron-down" size="xs" @click.stop.prevent="print('abajo')"></q-btn>
                <q-btn dense flat color="red" icon="mdi-delete" size="xs" @click.stop.prevent="print('borrar')"></q-btn>
              </q-btn-group>
            </template>
            <template v-slot:default-body="prop">
              <q-card square class="capas-qcard text-grey-10">
                <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" basic>
                  <div class="absolute-bottom" style="background: initial">
                    <q-slider v-model="smallStep" dense label :label-value="parseInt(smallStep * 100) + '%'"
                              color="primary" label-color="primary" :min="0.0" :max="1" :step="0.05"/>
                  </div>
                </q-img>
                <q-tabs
                  v-model="tab"
                  class="text-grey"
                  active-color="black"
                  indicator-color="primary"
                  align="justify"
                >
                  <q-tab name="mails" dense icon="mdi-texture"/>
                  <q-tab name="alarms" dense icon="mdi-information"/>
                  <q-tab name="movies" dense icon="mdi-filter"/>
                  <q-tab name="alarms2" dense icon="mdi-cog"/>
                  <q-tab name="movies3" dense icon="mdi-cloud-download"/>
                </q-tabs>

                <q-separator/>

                <q-tab-panels v-model="tab" animated>
                  <q-tab-panel name="mails">
                    <p class="text-h6">Simbología</p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  </q-tab-panel>

                  <q-tab-panel name="alarms">
                    <p class="text-h6">Metadatos</p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  </q-tab-panel>

                  <q-tab-panel name="movies">
                    <p class="text-h6">Filtrado</p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  </q-tab-panel>
                </q-tab-panels>


                <q-separator/>
                <q-card-section>
                  <header>{{ prop.node.label }}</header>
                </q-card-section>

              </q-card>

            </template>
          </q-tree>

        </q-page>
      </q-page-container>
    </q-layout>
  </q-drawer>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import Vue from 'vue'

/** Vue Filters Start */
Vue.filter('truncate', function (text, length, suffix) {
  if (text.length > length) {
    return text.substring(0, length) + suffix;
  } else {
    return text;
  }
});
/** Vue Filters End */

export default {
  name: "MapaDrawerCapas",
  data() {
    return {
      tab: 'mails',
      smallStep: 0.3,
      expanded: [],
      filter: '',
    }
  },
  watch: {
    capaSeleccionada() {
      console.log("selected", this.capaSeleccionada)
      if (!this.capaSeleccionada) {
        this.capaSeleccionada = 'conflictos'
      }
    },
    expanded() {
      console.log("expanded", this.expanded)
    },
    ticked() {
      console.log("ticked", this.ticked)
    },
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getDrawerCapas', 'capasMapaGetter', 'capaSeleccionadaGetter']),

    capaSeleccionada: {
      get() {
        return this.capaSeleccionadaGetter
      },
      set(value) {
        this.capaSeleccionadaAction(value)
      }
    },
    capasTicked: {
      get() {
        let ticked = []
        for (let capa of this.capasMapaGetter) {
          if (capa.visible) ticked.push(capa.value)
        }
        return ticked
      },
      set(value) {
        this.setCapasTicked(value)
      }
    },

    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      }
    },
    drawerCapas: {
      get() {
        return this.getDrawerCapas
      },
      set(value) {
        this.setDrawerCapas(value)
      }
    },
    capasMapa: {
      get() {
        return this.capasMapaGetter
      }
    },
    mapHeight() {
      let ribbon_height = 93
      if (this.showGISRibbon) ribbon_height = 180
      return this.$q.screen.height - ribbon_height + "px"
    },
  },
  methods: {
    ...mapActions('geojitsu', ['capaSeleccionadaAction', 'setDrawerCapas', 'setCapasTicked']),
    print(value) {
      console.log(value)
    },
    myFilterMethod(node, filter) {
      const filt = filter.toLowerCase()
      return node.label && node.label.toLowerCase().indexOf(filt) > -1
    },
    resetFilter() {
      this.filter = ''
      this.$refs.filter.focus()
    }
  },
}
</script>

<style lang="css" scoped>
.capas-qtree >>> .q-tree__children {
  display: none;
}

.capas-qtree >>> .q-tree__node-body {
  padding-right: 6px;
}

.capas-qtree >>> .q-tab {
  padding: 0;
}

.capas-qtree >>> .q-tab__icon {
  height: 30px;
  font-size: 26px;
}


.capas-qtree >>> .q-card1 {
  color: #424242;
}
</style>
