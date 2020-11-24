<template>
  <q-drawer
    elevated
    v-model="drawerCapas"
    show-if-above
    side="right"
    :breakpoint="319"
    overlay
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
          <!-- <q-input
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
              Listar solo las capas que coinciden con la busqueda del filtro
            </q-tooltip>
            <template v-slot:prepend>
              <q-icon name="mdi-filter"/>
            </template>
            <template v-slot:append>
              <q-icon v-if="filter !== ''" name="clear" class="cursor-pointer" @click="resetFilter"/>
            </template>
          </q-input> -->

          <q-tree
            class="q-pt-xs capas-qtree"
            :nodes="capasMapa"
            node-key="value"
            tick-strategy="strict"
            :ticked.sync="capasTicked"
            :expanded.sync="expanded"
            :filter="filter"
            :filter-method="myFilterMethod"
            selected-color="primary"
          >
            <template v-slot:default-header="prop">
              {{ String(prop.node.label) | truncate(24, '...') }}
              <q-space/>
              <q-btn-group flat>
                <q-btn :disabled="capasMapa.indexOf(prop.node) === 0" dense flat color="grey-8" icon="mdi-chevron-up" size="xs"
                       @click.stop.prevent="subirCapa(prop.node)"></q-btn>
                <q-btn :disabled="capasMapa.indexOf(prop.node) === capasMapa.length-1" dense flat color="grey-8" icon="mdi-chevron-down" size="xs"
                       @click.stop.prevent="bajarCapa(prop.node)"></q-btn>
              </q-btn-group>
            </template>
            <template v-slot:default-body="prop">
              <card-capa :capa="prop.node" />
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
import CardCapa from "components/drawer_components/CardCapa";

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
  components: {CardCapa},
  data() {
    return {
      expanded: ["reportes"],
      filter: '',
    }
  },
  watch: {
    expanded() {
      // console.log("expanded", this.expanded)
    },
    ticked() {
      // console.log("ticked", this.ticked)
    },
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getDrawerCapas', 'capasMapaGetter']),

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
    ...mapActions('geojitsu', ['setDrawerCapas', 'setCapasTicked', 'bajarCapaAction', 'subirCapaAction']),
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
    },
    bajarCapa(node) {
      let idx = this.capasMapaGetter.indexOf(node)
      this.bajarCapaAction(idx)
    },
    subirCapa(node) {
      let idx = this.capasMapaGetter.indexOf(node)
      this.subirCapaAction(idx)
    }
  },
  mounted() {
    //console.log("platform", this.$q.screen.width)

    if (this.$q.screen.width < 768) {
      this.drawerCapas = false;
    }
  }
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

</style>
