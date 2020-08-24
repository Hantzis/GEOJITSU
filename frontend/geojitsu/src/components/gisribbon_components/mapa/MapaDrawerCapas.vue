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
          <q-btn dense flat icon="close" @click="drawerCapas = false"/>
        </q-bar>
      </q-header>

      <q-page-container>
        <q-page style="height: inherit; min-height: inherit">

          <q-input
            ref="filter"
            filled
            v-model="filter"
            label="Filtrar - labels that have also '(*)'"
          >
            <template v-slot:append>
              <q-icon v-if="filter !== ''" name="clear" class="cursor-pointer" @click="resetFilter"/>
            </template>
          </q-input>

          <q-tree
            class="q-pt-xs capas-qtree"
            :nodes="capasMapa"
            node-key="value"
            tick-strategy="strict"
            :selected.sync="selected"
            :ticked.sync="ticked"
            :expanded.sync="expanded"
            :filter="filter"
            :filter-method="myFilterMethod"
            selected-color="primary"
          >
            <template v-slot:default-header="prop">
              <div class="row justify-between">
                <div class="col" style="padding-top: 4px;">
                  {{ prop.node.label }}
                </div>
                <div class="col">
                  <q-btn-group dense flat>
                    <q-btn dense flat icon="mdi-arrow-up"></q-btn>
                    <q-btn dense flat icon="mdi-arrow-down"></q-btn>
                  </q-btn-group>
                </div>
              </div>
            </template>
            <template v-slot:body-story="prop">
              <span class="text-weight-thin">The story is:</span> {{ prop.node.story }}
            </template>
            <template v-slot:default-body="prop">
              <div v-if="prop.node.children">
                <span class="text-weight-light text-black">Contenido de la capa {{ prop.node }}</span>
              </div>
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

Vue.filter('truncarCapas', (value) => {
  console.log("value, ", value)
  return value.substring(0, 10);
})


export default {
  name: "MapaDrawerCapas",
  data() {
    return {
      expanded: [],
      ticked: [],
      selected: 'conflictos',
      filter: '',
      simple: [
        {
          label: 'Good food (with icon)',
          icon: 'restaurant_menu',
          children: [
            {label: 'Quality ingredients'},
            {label: 'Good recipe'}
          ]
        },
        {
          label: 'Good service (disabled node with icon) ',
          icon: 'room_service',
          disabled: true,
          children: [
            {label: 'Prompt attention'},
            {label: 'Professional waiter'}
          ]
        },
        {
          label: 'Pleasant surroundings (with icon)',
          icon: 'photo',
          children: [
            {
              label: 'Happy atmosphere (with image)',
              img: 'https://cdn.quasar.dev/img/logo_calendar_128px.png'
            },
            {label: 'Good table presentation'},
            {label: 'Pleasing decor'}
          ]
        }
      ]
    }
  },
  watch: {
    selected() {
      console.log("selected", this.selected)
      if (!this.selected) {
        this.selected = 'conflictos'
      }
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getDrawerCapas', 'capasMapaGetter']),
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
    ...mapActions('geojitsu', ['setDrawerCapas']),

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
/*
.capas-qtree >>> .q-tree__node-collapsible .q-mr-xs.q-checkbox.cursor-pointer.no-outline.row.inline.no-wrap.items-center.q-checkbox--dense {
  display: none;
}
.capas-qtree >>> .q-tree__node-collapsible .q-tree__node--link {
  cursor: initial;
}
.capas-qtree >>> .q-tree__node-collapsible .q-focus-helper {
  display: none;
}
*/
.capas-qtree >>> .q-tree__children {
  display: none;
}
</style>
