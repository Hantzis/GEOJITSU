<template>
  <q-card square class="capas-qcard text-grey-10">
    <div v-if="capa.server_type === 'geoserver'">
      <q-img :src="String(capa.url).slice(0, -1) + '/reflect?layers=' + capa.layers + '&format=image/png'">
        <div class="absolute-bottom" style="background: initial">
          <q-slider v-model="opacityStep" dense label :label-value="parseInt(opacityStep * 100) + '%'"
                    color="primary" label-color="primary" :min="0.0" :max="1" :step="0.05"/>
        </div>
      </q-img>
    </div>
    <div v-if="capa.server_type === 'geojson'">
      <q-img :src="'/statics/reflects/geojson_' + capa.value + '.png'">
        <div class="absolute-bottom" style="background: initial">
          <q-slider v-model="opacityStep" dense label :label-value="parseInt(opacityStep * 100) + '%'"
                    color="primary" label-color="primary" :min="0.0" :max="1" :step="0.05"/>
        </div>
      </q-img>
    </div>
    <q-tabs
      v-model="tab"
      class="text-grey"
      active-color="black"
      indicator-color="primary"
      align="justify"
    >
      <q-tab name="simbologia" dense icon="mdi-texture"/>
      <q-tab name="metadatos" dense icon="mdi-information"/>
      <q-tab name="filtrado" dense icon="mdi-filter" disable/>
      <q-tab name="ajustes" dense icon="mdi-cog" disable/>
      <q-tab name="descarga" dense icon="mdi-cloud-download"/>
    </q-tabs>

    <q-separator/>

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="simbologia">
        <p class="text-h6">Simbología</p>
        <img v-if="capa.type==='wms'" :src="capa.url + 'SERVICE=WMS&REQUEST=GetLegendGraphic&VERSION=' + capa.url + '&FORMAT=image/png&LAYER=' + capa.layers">
      </q-tab-panel>

      <q-tab-panel name="metadatos">
        <p class="text-h6">Metadatos</p>
        "Aún no se cuentan con metadatos para esta capa."
      </q-tab-panel>

      <q-tab-panel name="filtrado">
        <p class="text-h6">Filtrado</p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit.
      </q-tab-panel>

      <q-tab-panel name="ajustes">
        <p class="text-h6">Ajustes</p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit.
      </q-tab-panel>

      <q-tab-panel name="descarga">
        <p class="text-h6">Descarga</p>
        <q-btn v-if="capa.type==='wms' && capa.url.endsWith('?')" label="Descargar datos" type="a" no-caps :href="`${capa.url}service=WFS&version=1.1.1&request=GetFeature&typeName=${capa.layers}&outputFormat=SHAPE-ZIP`"/>
        <q-btn v-if="capa.type==='wms' && !capa.url.endsWith('?')" label="Descargar datos" type="a" no-caps :href="`${capa.url}?service=WFS&version=1.1.1&request=GetFeature&typeName=${capa.layers}&outputFormat=SHAPE-ZIP`"/>
        <q-btn v-if="capa.type==='vector'" label="Descargar datos" @click.stop="saveGeoJSON(capa)" />
      </q-tab-panel>
    </q-tab-panels>

    <q-separator/>
    <q-card-section>
      <span style="font-weight: 300; font-size: 17px;">{{ capa.label }}</span>
    </q-card-section>

  </q-card>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import { saveAs } from 'file-saver';

export default {
  name: "CardCapa",
  data() {
    return {
      tab: 'mails',
      smallStep: 0.3,
      capaIndex: undefined
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['capasMapaGetter']),
    capasMapa: {
      get() {
        return this.capasMapaGetter
      }
    },
    opacityStep: {
      get() {
        return this.capasMapaGetter[this.capasMapa.indexOf(this.capa)].opacity
      },
      set(value) {
        this.setCapaOpacity({capa: this.capasMapa.indexOf(this.capa), value:value})
      }
    }
  },
  methods: {
    ...mapActions('geojitsu', ['setCapaOpacity']),
    saveGeoJSON(capa) {
      saveAs(`${capa.features}`, `${capa.value}.${capa.server_type}`)
    }
  },
  props: ['capa'],
  created() {
    this.capaIndex = this.capasMapa.indexOf(this.capa)
  },
  updated() {
    this.capaIndex = this.capasMapa.indexOf(this.capa)
  }
}
</script>
