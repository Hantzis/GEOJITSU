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
      align="left"
    >
      <q-tab name="simbologia" dense icon="mdi-texture"/>
      <!-- <q-tab name="alarms" dense icon="mdi-information"/>
      <q-tab name="movies" dense icon="mdi-filter"/>
      <q-tab name="alarms2" dense icon="mdi-cog"/>
      <q-tab name="movies3" dense icon="mdi-cloud-download"/> -->
    </q-tabs>

    <q-separator/>

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="simbologia">
        <p class="text-h6">Simbología</p>
        <q-img :src="capa.url + 'REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&LAYER=' + capa.layers"></q-img>
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
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "CardCapa",
  data() {
    return {
      tab: 'simbologia',
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
