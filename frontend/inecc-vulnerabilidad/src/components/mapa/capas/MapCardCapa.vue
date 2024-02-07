<template>
  <div>
    <div class=" q-pr-md q-py-sm">
      <q-card square class="capas-qcard text-grey-10">
        <div v-if="capa.server_type === 'geoserver'">
          <q-img :src="capa.url + '/reflect?layers=' + capa.layers + '&format=image/png'">
            <div class="absolute-bottom" style="background: initial">
              <q-slider v-model="opacityStep" dense label :label-value="(Math.floor(opacityStep * 100)) + '%'"
                        color="primary" label-color="primary" :min="0.0" :max="1" :step="0.05"/>
            </div>
          </q-img>
        </div>
        <div v-if="capa.server_type === 'geojson'">
          <q-img :src="'/statics/reflects/geojson_' + capa.value + '.png'">
            <div class="absolute-bottom" style="background: initial">
              <q-slider v-model="opacityStep" dense label :label-value="(Math.floor(opacityStep * 100)) + '%'"
                        color="primary" label-color="primary" :min="0.0" :max="1" :step="0.05"/>
            </div>
          </q-img>
        </div>
        <q-tabs
          v-model="tab"
          class="text-grey-7 "
          active-color="black"
          active-bg-color="grey-4"
          indicator-color="accent"
          align="justify"
        >
          <q-tab name="simbologia" dense icon="mdi-texture"/>
          <q-tab name="metadatos" dense icon="mdi-information"/>
          <q-tab name="filtro" dense icon="mdi-filter"/>
          <q-tab name="ajustes" dense icon="mdi-cog"/>
          <q-tab name="descarga" dense icon="mdi-cloud-download"/>
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
          <span style="font-weight: 300; font-size: 17px;">{{ capa.label }}</span>
        </q-card-section>

      </q-card>
    </div>
    <div class="q-pt-xs" style="margin-left: -22px;">
      <q-separator/>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue'
import {useMapStore} from 'stores/map-store'

const tab = ref('simbologia')
const mapStore = useMapStore()
const props = defineProps({
  capa: {
    type: Object, required: true, default(rawProps: object) {
      return {...rawProps}
    }
  }
})
const capa = ref(props.capa)

const capaIndex = computed(() => {
  console.log('capa.value: ', capa.value)
  return mapStore.capasMapa.indexOf(capa.value)
  //return mapStore.capasMapa.findIndex((capa) => capa.value === props.capa.value)
})

const opacityStep = computed({
  get() {
    return mapStore.capasMapa[capaIndex.value].opacity
  },
  set(value) {
    mapStore.capasMapa[capaIndex.value].opacity = value
  }
})

</script>

<style scoped lang="css">

</style>
