<template>
  <q-drawer
    elevated
    v-model="mapStore.showDrawerCapas"

    side="right"
    :breakpoint="319"

  >
    <q-layout view="lHh lpr lFf" container :style="{'min-height': mapHeight, 'max-height': mapHeight}">
      <q-header>
        <q-bar class="bg-grey-4 text-grey-9">
          <q-icon name="mdi-layers-triple"/>
          <div>Capas</div>
          <q-space/>
          <q-btn dense flat icon="close" @click="mapStore.showDrawerCapas = false">
            <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                       self="bottom middle">
              Cerrar panel de capas
            </q-tooltip>
          </q-btn>
        </q-bar>

        <q-input
          ref="filter"
          square
          outlined
          v-model="inputFilter"
          label="Filtrar"
          style="padding-right: 0;"
          dense
          @keyup.esc="resetFilter"
          bg-color="grey-1"
        >
          <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle" delay="1200">
            Listar capas que coincidan con la búsqueda
          </q-tooltip>
          <template v-slot:prepend>
            <q-icon name="mdi-filter"/>
          </template>
          <template v-slot:append>
            <q-icon v-if="inputFilter !== ''" name="clear" class="cursor-pointer" @click="resetFilter"/>
          </template>
        </q-input>

      </q-header>

      <q-page-container>
        <q-page style="height: inherit; min-height: inherit">
          <q-tree
            class="q-pt-xs capas-qtree"
            :nodes="mapStore.capasMapa"
            v-model:ticked="ticked"
            v-model:expanded="expanded"
            v-model:selected="mapStore.capaSeleccionada"
            color="grey-8"
            selected="primary"
            no-connectors
            node-key="value"
            tick-strategy="strict"
            selected-color="primary"
          >
            <template v-slot:default-header="prop">
              {{ shrinkName(prop.node.label) }}
              <q-space/>
              <q-btn-group flat>
                <q-btn :disabled="mapStore.capasMapa.indexOf(prop.node) === 0" dense flat color="grey-8"
                       icon="mdi-chevron-up" size="xs"
                       @click.stop.prevent="subirCapa(prop.node)"></q-btn>
                <q-btn :disabled="mapStore.capasMapa.indexOf(prop.node) === mapStore.capasMapa.length-1" dense flat
                       color="grey-8" icon="mdi-chevron-down" size="xs"
                       @click.stop.prevent="bajarCapa(prop.node)"></q-btn>
                <q-btn v-if="false" :disabled="prop.node.permanent" dense flat color="red" icon="mdi-delete" size="xs"
                       @click.stop.prevent="print('borrar')"></q-btn>
              </q-btn-group>
            </template>
            <template v-slot:default-body="prop">
              <map-card-capa :capa="prop.node"/>
            </template>
          </q-tree>

        </q-page>
      </q-page-container>

    </q-layout>
  </q-drawer>
</template>

<script setup lang="ts">
import {useMapStore} from 'stores/map-store'
import {computed, ref, watch} from 'vue'
import {useQuasar} from "quasar";
import MapCardCapa from "components/mapa/capas/MapCardCapa.vue";

const mapStore = useMapStore()
const $q = useQuasar()

const filter = ref(null)
const inputFilter = ref('')
const expanded = ref([])
const ticked = ref([])

const resetFilter = () => {
  inputFilter.value = ''
  filter.value.blur()
}


const print = (msg: string) => {
  console.log(msg)
}

const shrinkName = (name: string) => {
  if (name) {
    return name.length > 25 ? name.substring(0, 25) + '...' : name
  } else {
    return ''
  }
}

watch(ticked, (currentValue, oldValue) => {
  console.log('ticked', currentValue, oldValue)
})

watch(expanded, (currentValue, oldValue) => {
  console.log('expanded', currentValue, oldValue)
})

const subirCapa = (capa: any) => {
  const index = mapStore.capasMapa.indexOf(capa)
  mapStore.capasMapa.splice(index, 1)
  mapStore.capasMapa.splice(index - 1, 0, capa)
}

const bajarCapa = (capa: any) => {
  const index = mapStore.capasMapa.indexOf(capa)
  mapStore.capasMapa.splice(index, 1)
  mapStore.capasMapa.splice(index + 1, 0, capa)
}

const mapHeight = computed(() => {
  return $q.screen.lt.md ? $q.screen.height - 135 + 'px' : $q.screen.height - 135 + 'px'
})

</script>

<style scoped lang="css">
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
