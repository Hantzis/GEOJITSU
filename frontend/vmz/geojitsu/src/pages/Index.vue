<template>
  <q-page>
    <q-layout view="lHh Lpr lff" container :style="{height: screenHeight}">
      <q-header class="bg-gray">
        <GISRibbon/>
      </q-header>

      <mapa-drawer-capas/>

      <q-page-container>
        <q-page>
          <div class="row">
            <div class="col" :style="{'min-height': mapHeight}">
              <vl-map @click="clic" ref="olmap" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
                      data-projection="EPSG:4326"
                      :style="{'min-height': 'inherit', 'max-height': '1px', 'width': '100%', 'background-color': mapaBase.bgcolor}">
                <vl-view ref="olview" :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>
                <vl-geoloc @update:position="geolocPosition = $event">
                  <template slot-scope="geoloc">
                    <vl-feature v-if="geoloc.position" id="position-feature">
                      <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
                      <vl-style-box>
                        <vl-style-icon
                          src="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png"
                          :scale="0.1" :anchor="[0.5, 1]"></vl-style-icon>
                      </vl-style-box>
                    </vl-feature>
                  </template>
                </vl-geoloc>
                <vl-layer-tile>
                  <vl-source-xyz
                    :url="mapaBase.url"
                    attributions="Mapbox, <a href='https://www.saeba.click' target='_blank'>Saeba</a>"/>
                </vl-layer-tile>
                <vl-layer-vector>
                  <vl-source-vector :features.sync="zapopan">
                  </vl-source-vector>
                </vl-layer-vector>

                <div :key="mapkey">
                  <div v-for="capa of capasMapa" :key="capa.value">
                    <vl-layer-tile v-if="capa.type==='wms' && capa.tiled===true" :opacity="capa.opacity"
                                   :visible="capa.visible">
                      <vl-source-wms
                        :ref="capa.value"
                        :url="capa.url"
                        :format="capa.format"
                        :server_type="capa.server_type"
                        :layers="capa.layers"
                        :attributions="capa.attribution"
                        :ext-params="capa.params"/>
                    </vl-layer-tile>
                    <vl-layer-image v-if="capa.type==='wms' && capa.tiled===false" :opacity="capa.opacity"
                                    :visible="capa.visible">
                      <vl-source-image-wms
                        :ref="capa.value"
                        :url="capa.url"
                        :format="capa.format"
                        :server_type="capa.server_type"
                        :layers="capa.layers"
                        :attributions="capa.attribution"
                        :ext-params="capa.params"/>
                    </vl-layer-image>
                  </div>
                </div>

                <vl-interaction-select :features.sync="selectedFeatures" :layers="this.layers">
                  <vl-overlay v-if="position && selectedFeatures.length > 0" :position="position" :auto-pan="true"
                              style="background: white; padding: 8px">
                    <div style="max-width: 300px; min-width: 300px;">
                      <q-table
                        class="detalles"
                        style="max-height: 400px; max-width: 300px"
                        :title="selectedFeatures[0].properties.tipo[1] + ' (id:' + selectedFeatures[0].properties.pk + ')'"
                        square
                        wrap-cells
                        dense
                        :rows-per-page-options="[15]"
                        virtual-scroll
                        separator="cell"
                        hide-bottom
                        :data="getEntries(selectedFeatures[0].properties)"
                      >
                        <template v-slot:header>
                          <q-th colspan="2" align="left">
                            <q-td style="padding: 0">{{ selectedFeatures[0].properties.resumen }}</q-td>
                          </q-th>
                        </template>
                        <template v-slot:top-right>
                          <q-btn flat dense size="sm" style="margin-right: -11px;">
                            <q-icon name="close" @click="position = undefined; selectedFeatures = []"/>
                          </q-btn>
                        </template>
                      </q-table>
                    </div>
                  </vl-overlay>
                </vl-interaction-select>

              </vl-map>

            </div>

          </div>
        </q-page>
      </q-page-container>
    </q-layout>
    <q-ajax-bar
      ref="bar"
      position="top"
      color="black"
      size="4px"
      skip-hijack
    />

    <q-dialog ref="agregarreportemarcador_dialog" v-model="agregarreportemarcador_dialog" persistent>
      <q-card style="width: 680px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-map-marker-plus" color="pink" text-color="white"/>
          <q-toolbar-title>Agregar reporte</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <p>Agrear reporte.</p>
          </div>

          <q-form ref="form_reporte_domicilio" autocomplete="off" greedy>
            <div class="row q-py-xs">
              <div class="col-6">
                <q-input outlined class="full-width" mask="date"
                         name="fecha_reporte" v-model="fecha_reporte_marcador"
                         label="Fecha" :rules="[val => !!val || 'Fecha obligatoria']">
                  <template v-slot:default>
                    <q-popup-proxy ref="qDateProxy" transition-show="scale" mask="date" transition-hide="scale">
                      <q-date v-model="fecha_reporte_marcador">
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Cerrar" color="primary" flat/>
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </template>
                  <template v-slot:append>
                    <q-icon name="event"/>
                  </template>
                </q-input>
              </div>
              <div class="col-6" style="padding-left: 20px;">
                <q-input outlined class="full-width" mask="time"
                         name="hora_reporte" v-model="hora_reporte_marcador"
                         label="Hora" :rules="[val => !!val || 'Hora obligatoria']">
                  <template v-slot:default>
                    <q-popup-proxy transition-show="scale" mask="time" transition-hide="scale">
                      <q-time v-model="hora_reporte_marcador" format24h>
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Cerrar" color="primary" flat/>
                        </div>
                      </q-time>
                    </q-popup-proxy>
                  </template>
                  <template v-slot:append>
                    <q-icon name="access_time"/>
                  </template>
                </q-input>
              </div>

            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined name="colonia" v-model="reporte_marcador_data.colonia"
                        :options="colonias"
                        label="Colonia" :rules="[val => !!val || 'Colonia obligatoria']"
                        emit-value map-options option-value="id" option-label="nombre" />
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="calle" v-model="reporte_marcador_data.calle"
                       :rules="[val => !!val || 'Calle obligatoria']"
                       label="Calle"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 20px;">
              <q-input outlined class="full-width" name="calle" type="number" v-model="reporte_marcador_data.numero"
                       label="Número exterior"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 20px;">
              <q-input outlined class="full-width" name="entre_interseccion"
                       v-model="reporte_marcador_data.entre_interseccion"
                       label="Calle intersección"/>
            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined name="tipo" v-model="reporte_marcador_data.tipo"
                        :options="['Servicios', 'Situaciones']"
                        label="Tipo de reporte" :rules="[val => !!val || 'Tipo obligatorio']"/>
            </div>
            <div v-if="reporte_marcador_data.tipo === 'Servicios'">
              <div class="row q-py-xs">
                <q-select class="full-width" outlined name="tipo_servicio"
                          v-model="reporte_marcador_data.tipo_servicio"
                          :options="tipos_servicio"
                          label="Tipo de servicio" :rules="[val => !!val || 'Tipo de servicio obligatorio']"
                          emit-value map-options option-value="id" option-label="nombre"/>
              </div>
              <div class="row q-py-xs">
                <q-select v-if="reporte_marcador_data.tipo_servicio < 1000000" class="full-width" outlined
                          name="estado_servicio" v-model="reporte_marcador_data.estado_servicio"
                          :options="estados_servicio"
                          :rules="[val => !!val || 'Estado de servicio obligatorio']"
                          label="Estado de servicio"
                          emit-value map-options option-value="id" option-label="nombre"/>
                <q-input v-if="reporte_marcador_data.tipo_servicio === 1000000" outlined class="full-width"
                         name="estado_servicio_otro"
                         v-model="reporte_marcador_data.estado_servicio_otro"
                         :rules="[val => !!val || 'Otro servicio obligatorio']"
                         label="Otro tipo de servicio"/>
              </div>
            </div>
            <div v-if="reporte_marcador_data.tipo === 'Situaciones'">
              <div class="row q-py-xs">
                <q-select class="full-width" outlined name="situacion_peligrosa"
                          v-model="reporte_marcador_data.situacion_peligrosa"
                          :options="situaciones_peligro"
                          label="Situación de peligro" :rules="[val => !!val || 'Situación de peligro obligatoria']"
                          emit-value map-options option-value="id" option-label="nombre"/>
              </div>
              <div class="row q-py-xs">
                <q-input v-if="reporte_marcador_data.situacion_peligrosa === 1000000" outlined class="full-width"
                         name="situacion_peligrosa_otra"
                         v-model="reporte_marcador_data.situacion_peligrosa_otra"
                         :rules="[val => !!val || 'Otra situación obligatorio']"
                         label="Detalle de estado de servicio"/>
              </div>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 20px;">
              <q-input outlined class="full-width" name="comentarios" autogrow
                       v-model="reporte_marcador_data.comentarios"
                       label="Comentarios adicionales"/>
            </div>
          </q-form>
          <div v-if="false" class="row q-px-xs">
            <p class="text-red">Las contraseñas no coinciden</p>
          </div>
          <br/>
          <div class="row">
            <div class="col">
              <q-btn :disabled="false"
                     @click="saveReporteDomicilio()" color="green"
                     label="Guardar reporte" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
import axios from 'axios'
import * as turf from '@turf/turf'

import Vue from 'vue'
import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'
import GISRibbon from "components/GISRibbon"; // needs css-loader
import Style from 'ol/style/Style'
import Icon from 'ol/style/Icon'
import MapaDrawerCapas from "components/drawer_components/MapaDrawerCapas";
import {Point as turfPoint, Coord as turfCoord, FeatureCollection as turfFeatureCollection} from '@turf/helpers'
import {transform} from 'ol/proj';


Vue.use(VueLayers)

export default {
  name: 'PageIndex',
  components: {MapaDrawerCapas, GISRibbon},
  data() {
    return {
      zapopan: [],
      layers: [],
      loadingBar: undefined,
      clickCoords: undefined,
      position: undefined,
      agregarreportemarcador_dialog: false,
      fecha_reporte_marcador: "",
      hora_reporte_marcador: "",
      zoom: 15,
      center: [-103.38890075683594, 20.72561197927564],
      center3857: [-11268847.24, 2231060.47],
      rotation: 0,
      geolocPosition: [-101.22977709999999, 19.6453138],
      conflictos: [],
      loading: false,
      conflictos_geojson_url: "https://conflictossocioambientales.iies.unam.mx/conflictos/conflictos.geojson",
      conflictos_features: [],
      conflictos_selectedFeatures: [],
      selectedFeatures: [],
      conflictos_styles: {},
      colonias: undefined,
      tipos_servicio: undefined,
      estados_servicio: undefined,
      situaciones_peligro: undefined,
      reporte_marcador_data: {
        colonia: undefined, calle: undefined, numero: undefined, entre_interseccion: undefined,
        tipo: undefined, tipo_servicio: undefined, estado_servicio: undefined, estado_servicio_otro: undefined,
        situacion_peligrosa: undefined, situacion_peligrosa_otra: undefined, comentarios: undefined,
        fecha: "", hora: "", ubicacion: undefined
      }
    }
  },
  watch: {
    capasMapa() {
      this.mapkey = this.mapkey + 1
    },
    mapHeight() {
      this.$refs["olmap"].remount()
    },
    mapaBase() {
      this.$refs["olmap"].updateSize()
    },
    selectedFeatures() {
      console.log(this.selectedFeatures)
      if (this.selectedFeatures.length > 0 && this.herramientaActiva == 'info') {
        this.layers = [this.$refs.reportes[0]]
        for (let feat of this.selectedFeatures) {
        }
        this.position = transform(this.selectedFeatures[0].geometry.coordinates, 'EPSG:3857', 'EPSG:4326')
        console.log(this.position)
      }
    },
    'reporte_marcador_data.tipo': function (newVal, oldVal) {
      this.reporte_marcador_data.estado_servicio = undefined
      this.reporte_marcador_data.estado_servicio_otro = undefined
      this.reporte_marcador_data.situacion_peligrosa = undefined
      this.reporte_marcador_data.situacion_peligrosa_otra = undefined
      console.log(this.reporte_marcador_data)
    },
    'reporte_marcador_data.tipo_servicio': function (newVal, oldVal) {
      if (newVal) {
        this.reporte_marcador_data.estado_servicio = undefined
        this.getEstadosServicio(newVal)
      }
    },
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getHerramientaActiva', 'mapaBaseGetter', 'mapasBaseGetter',
      'capasMapaGetter', 'getDrawerCapas', 'getMapkey']),
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      }
    },
    herramientaActiva: {
      get() {
        return this.getHerramientaActiva
      },
      set(value) {
        this.setHerramientaActiva(value)
      }
    },
    mapkey: {
      get() {
        return this.getMapkey
      },
      set(value) {
        this.setMapkey(value)
      }
    },
    mapaBase: {
      get() {
        let base
        for (let map of this.mapasBaseGetter) {
          if (map.value === this.mapaBaseGetter) {
            base = map
          }
        }
        if (!base) base = {
          bgcolor: "#75cff0",
          url: "https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"
        }
        return base
      }
    },
    capasMapa: {
      get() {
        return this.capasMapaGetter
      }
    },
    drawerCapas: {
      get() {
        return this.getDrawerCapas
      }
    },
    mapHeight() {
      let ribbon_height = 99 + 24
      if (this.showGISRibbon) ribbon_height = 192 + 24
      return this.$q.screen.height - ribbon_height + "px"
    },
    screenHeight() {
      return this.$q.screen.height - 98 - 24 + "px"
    }
  },
  methods: {
    ...mapActions('geojitsu', ['capasMapaAction', 'setCapaFeatures', 'setCapaTicked', 'setHerramientaActiva', 'setMapkey']),
    getEntries(properties) {
      let limpio = []
      Object.entries(properties).forEach((row) => {
        if (row[1] && row[1].length > 0 && row[0] !== 'resumen' && row[0] !== 'tipo' && row[0] !== 'pk' && row[0] !== 'bibliografia') {
          if (Array.isArray(row[1])) {
            row[1] = row[1].join(", ")
          }
          row[0] = row[0].split("_").join(" ")
          if (row[0] === 'secretarias') row[0] = 'secretarías'
          limpio.push(row)
        }
      })
      return limpio
    },
    loaderFactory(capa) {
      if (this.capasMapa[capa].features.length == 0) {
        axios.get(this.capasMapa[capa].url).then(response => {
          this.setCapaFeatures({capa: capa, features: response.data.features})
        }).catch(error => {
          console.log(error)
        }).finally(() => {
          this.loadingBar.stop()
          this.setCapaTicked({capa: this.capasMapa[capa], visible: true})
        })
      }
    },
    clic(evt) {
      this.selectedFeatures = []
      console.log("clic event", evt)
      console.log("clic event", evt.coordinate)
      console.log("herramientaActiva", this.herramientaActiva)
      this.clickCoords = evt.coordinate
      if (this.herramientaActiva === 'info') {
        console.log(this.$refs.olview)
        console.log(this.$refs.olview.$view.values_.resolution)
        const coord = transform(evt.coordinate, 'EPSG:4326', 'EPSG:3857')
        const viewResolution = /** @type {number} */ this.$refs.olview.$view.values_.resolution;
        let url = this.$refs.reportes[0].getFeatureInfoUrl(coord, viewResolution, 'EPSG:3857', {'INFO_FORMAT': 'application/json'})
        console.log(url)
        axios.get(url).then(response => {
          console.log(response)
          console.log(response.data)
          this.selectedFeatures = response.data.features
        }).catch(error => console.log(error))
      }
      if (this.herramientaActiva === 'agregar_marcador') {
        const coord = transform(evt.coordinate, 'EPSG:4326', 'EPSG:3857')
        const viewResolution = this.$refs.olview.$view.values_.resolution;
        axios.get(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${evt.coordinate[1]},${evt.coordinate[0]}&key=AIzaSyAPJOFYKRav1z3IxoK-URalWtPY4KKTAb0`)
          .then(response => {
            console.log("response", response)
            if (response.data.results.length > 0) {

              const addr = response.data.results[0].address_components

              console.log("addr", addr)
              if (addr[0].types[0] === 'street_number') {
                this.reporte_marcador_data.numero = parseInt(addr[0].long_name)
              }
              if (addr[1].types[0] === 'route') {
                this.reporte_marcador_data.calle = addr[1].long_name
              }

              let url = this.$refs.colonias_zapopan[0].getFeatureInfoUrl(coord, viewResolution, 'EPSG:3857', {'INFO_FORMAT': 'application/json'})
              axios.get(url).then(response => {
                console.log(response)
                const col = response.data.features[0]
                this.reporte_marcador_data.colonia = col.id.split(".")[1]
                // this.selectedFeatures = response.data.features
              }).catch(error => console.log(error))

              this.agregarreportemarcador_dialog = true
            }
          })


      }


    },
    getColonias() {
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/colonias/?municipio=120`).then(response => {
        this.colonias = response.data
        console.log("colonias", this.colonias)
      }).catch(error => console.log(error))
    },
    getTiposServicio() {
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/tipos-servicio/`).then(response => {
        this.tipos_servicio = response.data
        console.log("tipos_servicio", this.tipos_servicio)
      }).catch(error => console.log(error))
    },
    getEstadosServicio(val) {
      if (val && val < 1000000) {
        axios.get(`https://repvmz.maptitude.xyz/back/api/v1/estados-servicio/?tipo=${val}`).then(response => {
          this.estados_servicio = response.data
          console.log("estados_servicio", this.estados_servicio)
        }).catch(error => console.log(error))
      } else {
        this.estados_servicio = undefined
      }
    },
    getSituacionesPeligrosas() {
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/situaciones-peligro/`).then(response => {
        this.situaciones_peligro = response.data
        console.log("situaciones_peligrosas", this.situaciones_peligro)
      }).catch(error => console.log(error))
    },
    pointsStyleFunc() {
      return (feature) => {
        let img_url = "https://conflictossocioambientales.iies.unam.mx" + feature.values_.tipo[2]
        let style = new Style({image: new Icon({src: img_url})})
        return style
      }
    }
  },
  mounted() {
    this.loadingBar = this.$refs.bar
    axios.get('statics/zapopan.geojson').then(res => {
      console.log(res.data.features)
      this.zapopan = res.data.features
    }).then(() => {
      this.getColonias()
      this.getTiposServicio()
      this.getSituacionesPeligrosas()
    }).finally(() => {
      this.loadingBar.stop()
    })
  }
}
</script>

<style lang="css" scoped>
.detalles >>> .q-table__top.relative-position.row.items-center {
  flex-wrap: nowrap;
  align-items: flex-start;
}
</style>
