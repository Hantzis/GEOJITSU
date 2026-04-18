<template>
  <div>
    <q-card square class="capas-qcard text-grey-10">
      <div v-if="capa.server_type === 'geoserver'">
        <div class="q-pa-sm ">
          <q-slider v-model="opacityStep" dense label :label-value="parseInt(opacityStep * 100) + '%'"
                    color="primary" label-color="primary" :min="0.0" :max="1" :step="0.05"/>
        </div>
      </div>
      <div v-if="capa.server_type === 'mvt'">
        <div class="q-pa-sm ">
          <q-slider v-model="opacityStep" dense label :label-value="parseInt(opacityStep * 100) + '%'"
                    color="primary" label-color="primary" :min="0.0" :max="1" :step="0.05"/>
        </div>
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
        indicator-color="grey-13"
        align="left"
        dense
      >
        <q-tab name="simbologia" dense icon="mdi-texture"/>
        <q-tab :disable="capa.value!=='reportes'" name="filtro" dense icon="mdi-filter"/>
        <!--<q-tab name="movies" dense icon="mdi-filter"/>
        <q-tab name="alarms2" dense icon="mdi-cog"/>
        <q-tab name="movies3" dense icon="mdi-cloud-download"/> -->
      </q-tabs>

      <q-separator/>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="simbologia">
          <p class="text-h6">Simbología</p>

          <!-- 🟢 MVT (tu caso reportes) -->
          <reportes-map-legend
            v-if="capa.type === 'mvt' && capa.value === 'reportes'"
            :servicios="servicios"
            :situaciones="situaciones"
            :strokeServicios="strokeServicios"
            :strokeSituaciones="strokeSituaciones"
            :filtro="capa.params"
          />

          <!-- 🔵 WMS (todo lo demás) -->
          <img
            v-if="capa.type === 'wms'"
            :src="capa.url + 'SERVICE=WMS&REQUEST=GetLegendGraphic&VERSION=1.3.0&FORMAT=image/png&LAYER=' + capa.layers"
          />

        </q-tab-panel>

        <q-tab-panel name="filtro">
          <p class="text-h6">Filtro</p>
          <q-btn :disable="capa.value!=='reportes'" class="full-width" no-caps color="primary"
                 @click="showFilterDialog=true">Aplicar filtro
          </q-btn>
        </q-tab-panel>

      </q-tab-panels>

      <!--
      <q-separator/>
      <q-card-section>
        <span style="font-weight: 300; font-size: 17px;">{{ capa.label }}</span>
      </q-card-section>
      -->

    </q-card>

    <q-dialog v-model="showFilterDialog">
      <q-card style="width: 560px;">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-filter" color="primary" text-color="white"/>
          <q-toolbar-title>Aplicar filtro</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <q-form ref="form_reporte_marcador" autocomplete="off" greedy>
                <div class="row q-py-xs">
                  <q-select class="full-width" outlined name="tipo" v-model="tipo"
                            :options="['Servicios', 'Situaciones']"
                            label="Tipo"
                  />
                </div>
                <div class="row q-py-xs"></div>
                <div v-if="tipo==='Servicios'" class="row q-py-xs">
                  <q-select class="full-width" outlined name="servicio" v-model="servicio"
                            :options="servicios"
                            label="Servicio"
                            emit-value map-options option-value="id" option-label="nombre"/>
                </div>
                <div v-if="tipo==='Situaciones'" class="row q-py-xs">
                  <q-select class="full-width" outlined name="situacion" v-model="situacion"
                            :options="situaciones"
                            label="Situación"
                            emit-value map-options option-value="id" option-label="nombre"/>
                </div>
              </q-form>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <q-btn @click="aplicarFiltro()" no-caps color="green"
                     label="Aceptar" class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import ReportesMapLegend from "components/drawer_components/ReportesMapLegend";

export default {
  name: "CardCapa",
  data() {
    return {
      tab: 'simbologia',
      tipo: undefined,
      servicio: undefined,
      situacion: undefined,
      showFilterDialog: false,
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
        this.setCapaOpacity({capa: this.capasMapa.indexOf(this.capa), value: value})
      }
    },
    cqlFilter: {
      get() {
        return this.capasMapaGetter[this.capasMapa.indexOf(this.capa)].params.cql_filter
      },
      set(value) {
        this.setCapaCQLFilter({capa: this.capasMapa.indexOf(this.capa), filtro: value})
      }
    }
  },
  methods: {
    ...mapActions('geojitsu', ['setCapaOpacity', 'setCapaCQLFilter', 'setCapaParams']),
    aplicarFiltro() {

      const idx = this.capasMapa.indexOf(this.capa)

      let params = {
        tipo: null,
        servicio: null,
        situacion: null
      }

      if (this.tipo === 'Servicios') {
        params.tipo = 'Servicios'
        params.servicio = this.servicio
      }

      if (this.tipo === 'Situaciones') {
        params.tipo = 'Situaciones'
        params.situacion = this.situacion
      }

      // 🔥 actualizar capa MVT
      this.setCapaParams({
        capa: idx,
        params: params
      })

      this.showFilterDialog = false
      this.$emit('update')
    }
  },
  watch: {
    showFilterDialog() {
      if (!this.showFilterDialog) {
        this.tipo = undefined;
        this.servicio = undefined;
        this.situacion = undefined;
      }
    }
  },
  props: [
    'capa',
    'servicios',
    'situaciones',
    'strokeServicios',
    'strokeSituaciones'
  ],
  components: {ReportesMapLegend},
  created() {
    this.capaIndex = this.capasMapa.indexOf(this.capa)
  },
  updated() {
    this.capaIndex = this.capasMapa.indexOf(this.capa)
  }
}
</script>
