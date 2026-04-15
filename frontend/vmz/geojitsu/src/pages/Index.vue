<template>
  <q-page>
    <q-layout view="lHh Lpr lff" container :style="{height: screenHeight}">
      <q-header class="bg-gray">
        <GISRibbon/>
      </q-header>

      <mapa-drawer-capas
        @update="refreshMap()"
        :strokeServicios="strokeServicios"
        :strokeSituaciones="strokeSituaciones"
      />

      <q-page-container>
        <q-page>
          <div class="row">
            <div class="col" :style="{'min-height': mapHeight}">
              <vl-map @click="onClickInMap" ref="olmap" :load-tiles-while-animating="true"
                      :load-tiles-while-interacting="true"
                      data-projection="EPSG:4326"
                      :style="{'min-height': 'inherit', 'max-height': '1px', 'width': '100%', 'background-color': mapaBase.bgcolor}">
                <vl-view ref="olview" :zoom.sync="zoom" :center.sync="center"></vl-view>
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
                  <vl-source-vector
                    url="https://development.demo.geonode.org/geoserver/ows?service=WMS&version=1.1.1&request=GetFeatureInfo&layers=geonode:mgenmex_municipios&query_layers=geonode:mgenmex_municipios&styles=geonode:mgenmex_municipios&x=51&y=51&height=101&width=101&srs=EPSG:3857&bbox=-11528274.230741149,2360353.554394476,-11512833.951027544,2375793.8341080816&feature_count=10&info_format=application%2Fjson">
                  </vl-source-vector>
                  <vl-style-box>
                    <vl-style-stroke color="black" :width="3"></vl-style-stroke>
                    <vl-style-fill color="rgba(44,55,0,0.05)"></vl-style-fill>
                  </vl-style-box>
                </vl-layer-vector>

                <div :key="mapkey">
                  <div v-for="capa of capasMapa" :key="capa.value">
                    <vl-layer-tile v-if="capa.type==='wms' && capa.tiled===true" :opacity="capa.opacity"
                                   :visible="capa.visible">
                      <vl-source-wms
                        :key="mapkey"
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
                    <vl-layer-vector-tile
                      v-if="capa.type==='mvt'"
                      :opacity="capa.opacity"
                      :visible="capa.visible"
                    >
                      <vl-source-vector-tile
                        :url="buildMVTUrl(capa)"
                        :format="mvtFormat"
                      />
                      <vl-style-func :factory="() => styleReportes"/>
                    </vl-layer-vector-tile>
                  </div>
                </div>

                <vl-overlay v-if="position && selectedFeatures.length > 0" :position="position" :auto-pan="true"
                            style="background: white; padding: 8px">
                  <div style="max-width: 300px; min-width: 300px;">

                    <q-table
                      class="detalles"
                      style="max-height: 400px; max-width: 300px"
                      :title="`${selectedFeatureInfo.tipo} (${selectedFeatureInfo.id})`"
                      square
                      wrap-cells
                      dense
                      :rows-per-page-options="[15]"
                      virtual-scroll
                      separator="cell"
                      hide-bottom
                      :data="getEntries(selectedFeatureInfo)"
                    >
                      <template v-slot:header>
                        <q-th colspan="2" style="padding: 0">
                        </q-th>
                      </template>
                      <template v-slot:top-right>
                        <q-btn flat dense size="sm" style="margin-right: -11px;">
                          <q-icon name="close" @click="position = undefined; selectedFeatures = []"/>
                        </q-btn>
                      </template>
                    </q-table>

                    <div class="row q-pt-sm">
                      <q-btn dense no-caps class="full-width"
                             v-if="this.is_user_staff && !selectedFeatureInfo.evidencia_reporte"
                             @click="showEvidenciaRegistroForm=true">
                        Agregar evidencia reporte
                      </q-btn>
                    </div>
                    <div class="row q-pt-sm">
                      <q-btn dense no-caps class="full-width" v-if="selectedFeatureInfo.evidencia_reporte"
                             :color="selectedFeatureInfo.estatus === 'Abierto' ? 'accent' : 'green'"
                             @click="showEvidenciaReporte=true">
                        Fotografía reporte
                      </q-btn>
                    </div>

                    <div class="row q-pt-sm">
                      <q-btn dense no-caps class="full-width" v-if="selectedFeatureInfo.evidencia_atencion"
                             @click="showEvidenciaAtencion=true">
                        Evidencia atención
                      </q-btn>
                    </div>

                    <div class="row q-pt-sm">
                      <q-select
                        :readonly="(!(selectedFeatureInfo.tipo === 'Servicios' && this.userGroups.includes(4)) && !(selectedFeatureInfo.tipo === 'Situaciones' && this.userGroups.includes(5)))"
                        v-model="selectedFeatureInfo.estatus"
                        :options="['Abierto', 'Atendiendo', 'Resuelto']"
                        label="Estatus" name="estatus" outlined class="full-width" behavior="menu"/>
                    </div>
                  </div>
                </vl-overlay>

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

    <q-dialog v-model="showEvidenciaReporte" full-width>
      <q-card>
        <q-card-section>
          <q-img :src="selectedFeatureInfo.evidencia_reporte"/>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showEvidenciaAtencion" full-width>
      <q-card>
        <q-card-section>
          <q-img :src="selectedFeatureInfo.evidencia_atencion"/>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showEvidenciaAtencionForm">
      <q-card>
        <q-card-section>
          <q-form>
            <q-file outlined v-model="evidencia_atencion" label="Evidencia atención"/>
            <q-btn :disable="!evidencia_atencion" @click="saveEvidenciaAtencion" label="Guardar" color="green"/>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showEvidenciaRegistroForm">
      <q-card>
        <q-card-section>
          <q-form>
            <q-file outlined v-model="evidencia_reporte_staff" label="Evidencia atención"/>
            <q-btn :disable="!evidencia_reporte_staff" @click="saveEvidenciaStaff" label="Guardar" color="green"/>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>


    <q-dialog ref="agregarreportemarcador_dialog" v-model="agregarreportemarcador_dialog" persistent>
      <q-card style="width: 680px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-map-marker-plus" color="pink" text-color="white"/>
          <q-toolbar-title>Agregar reporte</q-toolbar-title>
          <!-- localización -->
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <p>Agrear reporte.</p>
          </div>

          <q-form ref="form_reporte_marcador" autocomplete="off" greedy>
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
                        emit-value map-options option-value="nombre" option-label="nombre"/>
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
            <div class="row q-py-xs">
              <q-file v-model="evidencia_reporte" label="Adjuntar evidencia (opcional)"
                      name="evidencia_reporte" class="full-width" clearable outlined accept=".jpg, image/*">
                <template v-slot:prepend>
                  <q-icon name="attach_file"/>
                </template>
              </q-file>
            </div>
          </q-form>
          <br/>
          <div class="row">
            <div class="col">
              <q-btn :disabled="false"
                     @click="saveReporteMarcador()" color="green"
                     label="Guardar reporte" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog ref="reporte_agregado_dialog" v-model="reporte_agregado_dialog">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="red" text-color="white"/>
          <q-toolbar-title>Reporte agregado</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <p>El reporte se ha agregado satisfactoriamente, recargue la página en unos minutos para ver reflejado
                su aporte</p>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <q-btn @click="reporte_agregado_dialog = false" no-caps color="green"
                     label="Aceptar" class="full-width"/>
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

import Vue from 'vue'
import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'
import GISRibbon from "components/GISRibbon"; // needs css-loader
import MapaDrawerCapas from "components/drawer_components/MapaDrawerCapas";
import {transform} from 'ol/proj';
import cookies from 'browser-cookies'
import MVT from 'ol/format/MVT'
import {Style, Circle, Fill, Stroke, RegularShape} from 'ol/style'

Vue.use(VueLayers)

export default {
  name: 'PageIndex',
  components: {MapaDrawerCapas, GISRibbon},
  data() {
    return {
      clickRequestId: 0,
      ignoreNextEstatusChange: false,
      mvtFormat: new MVT(),
      // 🔑 Stroke por ID (SERVICIOS)
      strokeServicios: {
        10: '#de9a39',
        11: '#fdfd4d',
        17: '#0d6b18',
        15: '#b26489',
        6: '#2fc4fa',
        12: '#2d96e5',
        1: '#3582c5',
        3: '#0ebf6f',
        21: '#9e9624',
        20: '#fd4eb7',
        19: '#181818',
        9: '#a61875',
        16: '#4b0ef4',
        4: '#b26489',
        5: '#2fc4fa',
        7: '#2d96e5',
        8: '#3582c5',
        13: '#0ebf6f',
        22: '#69204c',
        23: '#69201c',
        24: '#8b236a',
        2: '#939393',
        18: '#a61875',
        1000000: '#000000'
      },

      // 🔑 Stroke por ID (SITUACIONES)
      strokeSituaciones: {
        2: '#8c2df1',
        4: '#e9b37a',
        7: '#f4f442',
        10: '#8ca65a',
        1: '#8c2df1',
        3: '#9f6829',
        5: '#6eadc8',
        6: '#ef7021',
        8: '#e9b37a',
        9: '#42ddf4',
        1000000: '#232323'
      },
      zapopan: [],
      layers: [],
      loadingBar: undefined,
      clickCoords: undefined,
      position: undefined,
      agregarreportemarcador_dialog: false,
      showEvidenciaRegistroForm: false,
      showEvidenciaReporte: false,
      showEvidenciaAtencion: false,
      reporte_agregado_dialog: false,
      fecha_reporte_marcador: "",
      hora_reporte_marcador: "",
      zoom: 12,
      center: [-103.3810, 20.6930],
      center3857: [-11268847.24, 2231060.47],
      geolocPosition: [-101.22977709999999, 19.6453138],
      conflictos: [],
      loading: false,
      selectedFeatures: [],
      selectedFeatureInfo: {},
      conflictos_styles: {},
      colonias: undefined,
      tipos_servicio: undefined,
      estados_servicio: undefined,
      situaciones_peligro: undefined,
      evidencia_reporte_staff: undefined,
      evidencia_reporte: undefined,
      evidencia_atencion: undefined,
      reporte_marcador_data: {
        colonia: undefined, calle: undefined, numero: undefined, entre_interseccion: null,
        tipo: undefined, tipo_servicio: undefined, estado_servicio: undefined, estado_servicio_otro: undefined,
        situacion_peligrosa: undefined, situacion_peligrosa_otra: undefined, comentarios: null,
        fecha: "", hora: "", ubicacion: undefined,
      },
      showEvidenciaAtencionForm: false,
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
    'selectedFeatureInfo.estatus': function (newVal, oldVal) {

      // 🔴 ignorar cambio por carga de feature
      if (this.ignoreNextEstatusChange) {
        this.ignoreNextEstatusChange = false
        return
      }

      // 🔴 ignorar si no hay cambio real
      if (!oldVal || !newVal || oldVal === newVal) return

      const token = cookies.get("auth_token")
      const formData = new FormData()
      formData.append("estatus", newVal)

      axios.patch(
        `https://api.zapopanentrenosotras.com/rest/v1/reportes/${this.selectedFeatureInfo.id}/`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      )
        .then(() => {
          this.showEvidenciaAtencionForm = true
        })
        .catch(() => {
        })
    },
    'reporte_marcador_data.tipo': function (newVal, oldVal) {
      this.reporte_marcador_data.estado_servicio = undefined
      this.reporte_marcador_data.estado_servicio_otro = undefined
      this.reporte_marcador_data.situacion_peligrosa = undefined
      this.reporte_marcador_data.situacion_peligrosa_otra = undefined
    },
    'reporte_marcador_data.tipo_servicio': function (newVal, oldVal) {
      if (newVal) {
        this.reporte_marcador_data.estado_servicio = undefined
        this.getEstadosServicio(newVal)
      }
    },
    'reporte_marcador_data.colonia': function (newVal, oldVal) {
      console.log(this.reporte_marcador_data.colonia)
    },
    agregarreportemarcador_dialog() {
      if (this.agregarreportemarcador_dialog === false) {
        this.herramientaActiva = 'info'
        this.fecha_reporte_marcador = ""
        this.hora_reporte_marcador = ""
        this.reporte_marcador_data = {
          colonia: undefined, calle: undefined, numero: undefined, entre_interseccion: null,
          tipo: undefined, tipo_servicio: undefined, estado_servicio: undefined, estado_servicio_otro: undefined,
          situacion_peligrosa: undefined, situacion_peligrosa_otra: undefined, comentarios: null,
          fecha: "", hora: "", ubicacion: undefined
        }
      }
    },
    'fecha_reporte_marcador': function () {
      if (this.fecha_reporte_marcador !== "") {
        this.reporte_marcador_data.fecha = this.fecha_reporte_marcador.split("/").join("-")
      }
    },
    'hora_reporte_marcador': function () {
      if (this.hora_reporte_marcador !== "") {
        this.reporte_marcador_data.hora = this.hora_reporte_marcador
      }
    },
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getHerramientaActiva', 'mapaBaseGetter', 'mapasBaseGetter',
      'capasMapaGetter', 'getDrawerCapas', 'getMapkey', 'getUserGroups', 'getIsUserStaff']),
    // ...mapGetters('auth', ['logged', 'user', 'token']),
    is_user_staff: {
      get() {
        return this.getIsUserStaff
      },
      set(value) {
        this.setUserIsStaff(value)
      }
    },
    auth_user: {
      get() {
        return this.user
      }
    },
    auth_logged: {
      get() {
        return this.logged
      }
    },
    auth_token: {
      get() {
        return this.token
      }
    },
    userGroups: {
      get() {
        return this.getUserGroups
      },
      set(value) {
        this.setUserGroups(value)
      }
    },
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
          url: "https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}"
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
    ...mapActions('geojitsu', ['capasMapaAction', 'setCapaTicked', 'setHerramientaActiva', 'setMapkey',
      'setUserGroups', 'setUserIsStaff']),
    // ...mapActions('auth', ['login', 'logout', 'setToken']),
    getEntries(properties) {
      let limpio = [];
      limpio.push(["ID", properties.id]);
      limpio.push(["Fecha", properties.fecha]);
      limpio.push(["Hora", properties.hora]);
      // let colonia = properties.colonia_display;
      // if (properties.colonia_cp_display) colonia = colonia + " (" + properties.colonia_cp_display + ")";
      limpio.push(["Colonia", properties.colonia]);
      let calle = properties.calle;
      if (properties.numero) calle = calle + " #" + properties.numero;
      limpio.push(["Calle", calle]);
      if (properties.entre_interseccion) limpio.push(["Calle intersección", properties.entre_interseccion]);
      if (properties.tipo === "Servicios") {
        if (properties.tipo_servicio && properties.tipo_servicio < 1000000) limpio.push(["Tipo de servicio", properties.tipo_servicio_display])
        if (properties.estado_servicio && properties.tipo_servicio < 1000000) limpio.push(["Estado de servicio", properties.estado_servicio_display])
        if (properties.estado_servicio_otro && properties.tipo_servicio !== 1000000) limpio.push(["Estado de servicio", properties.estado_servicio_otro])
      }
      if (properties.tipo === "Situaciones") {
        if (properties.situacion_peligrosa && properties.situacion_peligrosa < 1000000) limpio.push(["Situación de peligro", properties.situacion_peligrosa_display])
        if (properties.estado_servicio_otro && properties.situacion_peligrosa !== 1000000) limpio.push(["Situación de peligro", properties.situacion_peligrosa_otra])
      }
      if (properties.comentarios) limpio.push(["Comentarios", properties.comentarios])
      return limpio
    },
    saveEvidenciaAtencion() {
      const token = cookies.get("auth_token");
      const formData = new FormData();
      formData.append("evidencia_atencion", this.evidencia_atencion);
      axios.patch(`https://api.zapopanentrenosotras.com/rest/v1/reportes/${this.selectedFeatureInfo.id}/`,
        formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          //console.log(response)
          this.showEvidenciaAtencionForm = false
        })
        .catch(error => {
          //console.log(error)
        })
    },
    saveEvidenciaStaff() {
      const token = cookies.get("auth_token");
      const formData = new FormData();
      formData.append("evidencia_reporte", this.evidencia_reporte_staff);
      axios.patch(`https://api.zapopanentrenosotras.com/rest/v1/reportes/${this.selectedFeatureInfo.id}/`,
        formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          //console.log(response)
          this.showEvidenciaRegistroForm = false
        })
        .catch(error => {
          //console.log(error)
        })
    },
    loaderFactory(capa) {
      if (this.capasMapa[capa].features.length === 0) {
        axios.get(this.capasMapa[capa].url).then(response => {
          this.setCapaFeatures({capa: capa, features: response.data.features})
        }).catch(error => {
          //console.log(error)
        }).finally(() => {
          this.loadingBar.stop()
          this.setCapaTicked({capa: this.capasMapa[capa], visible: true})
        })
      }
    },
    refreshMap() {
      console.log("refresh", this.capasMapa)
      this.mapkey++
      this.$refs['olmap'].refresh()
      this.$refs['olmap'].remount()
    },
    onClickInMap(evt) {
      this.clickCoords = evt.coordinate

      if (this.herramientaActiva === 'info') {
        this.clickRequestId++
        const currentRequest = this.clickRequestId

        const map = this.$refs.olmap.$map

        let found = null

        map.forEachFeatureAtPixel(evt.pixel, (feature) => {
          // 🔴 VALIDAR que sea un feature real de tus reportes
          const tipo = feature.get('tipo')
          const id = feature.get('id') || feature.getId()

          if (tipo && id) {
            found = feature
            return true
          }

          return false
        })

        if (!found) {
          this.selectedFeatures = []
          this.selectedFeatureInfo = {}
          this.position = null
          return
        }

        this.selectedFeatures = [found]

        const geometry = found.getGeometry()
        let coords = null

        if (geometry && typeof geometry.getCoordinates === 'function') {
          coords = geometry.getCoordinates()
        } else if (geometry && typeof geometry.getFlatCoordinates === 'function') {
          const flat = geometry.getFlatCoordinates()
          if (flat && flat.length >= 2) {
            coords = [flat[0], flat[1]]
          }
        }

        if (coords) {
          this.position = transform(coords, 'EPSG:3857', 'EPSG:4326')
        } else {
          this.position = null
        }

        const rawId = found.get('id') || found.getId()

        if (!rawId) {
          this.selectedFeatureInfo = {}
          this.selectedFeatures = []
          this.position = null
          return
        }

        let id = rawId

        if (typeof rawId === 'string' && rawId.includes('.')) {
          id = rawId.split('.').pop()
        }

        // 🔴 VALIDACIÓN FINAL
        if (!id || isNaN(parseInt(id))) {
          this.selectedFeatureInfo = {}
          this.selectedFeatures = []
          this.position = null
          return
        }

        id = parseInt(id)

        axios.get(`https://api.zapopanentrenosotras.com/rest/v1/reportes/${id}/`)
          .then(res => {

            // 🔴 IGNORA respuestas viejas
            if (currentRequest !== this.clickRequestId) return

            this.ignoreNextEstatusChange = true
            this.selectedFeatureInfo = res.data
          })
          .catch(() => {
            if (currentRequest !== this.clickRequestId) return
            this.selectedFeatureInfo = {}
          })

        return
      }

      if (this.herramientaActiva === 'agregar_marcador') {
        const coord = transform(evt.coordinate, 'EPSG:4326', 'EPSG:3857')
        const viewResolution = this.$refs.olview.$view.values_.resolution

        axios.get(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${evt.coordinate[1]},${evt.coordinate[0]}&key=AIzaSyAPJOFYKRav1z3IxoK-URalWtPY4KKTAb0`)
          .then(response => {
            if (response.data.results.length > 0) {
              this.reporte_marcador_data.ubicacion = `SRID=4326;POINT (${evt.coordinate[0]} ${evt.coordinate[1]})`

              const addr = response.data.results[0].address_components

              if (addr[0] && addr[0].types[0] === 'street_number') {
                this.reporte_marcador_data.numero = parseInt(addr[0].long_name)
              }

              if (addr[1] && addr[1].types[0] === 'route') {
                this.reporte_marcador_data.calle = addr[1].long_name
              }

              const url = this.$refs.colonias_zapopan[0].getFeatureInfoUrl(
                coord,
                viewResolution,
                'EPSG:3857',
                {'INFO_FORMAT': 'application/json'}
              )

              axios.get(url).then(response => {
                if (response.data.features.length > 0) {
                  const col = response.data.features[0]
                  // this.reporte_marcador_data.colonia = parseInt(col.id.split('.').pop())
                  this.reporte_marcador_data.colonia = col.properties.nombre
                  this.agregarreportemarcador_dialog = true
                } else {
                  this.setHerramientaActiva('info')
                }
              }).catch(() => {
              })
            }
          }).catch(() => {
        })
      }
    },
    getColonias() {
      axios.get(`https://development.demo.geonode.org/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=geonode:coloniasmex_ine2025&outputFormat=application/json&CQL_FILTER=cve_ent=%2714%27%20AND%20cve_mun=%27120%27`).then(response => {
        this.colonias = response.data.features.map(f => f.properties)
      }).catch(error => {
        //console.log(error)
      })
    },
    getTiposServicio() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/tipos-servicio/`).then(response => {
        this.tipos_servicio = response.data
      }).catch(error => {
        //console.log(error)
      })
    },
    getEstadosServicio(val) {
      if (val && val < 1000000) {
        axios.get(`https://api.zapopanentrenosotras.com/rest/v1/estados-servicio/?tipo=${val}`).then(response => {
          this.estados_servicio = response.data
        }).catch(error => {
          //console.log(error)
        })
      } else {
        this.estados_servicio = undefined
      }
    },
    getSituacionesPeligrosas() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/situaciones-peligro/`).then(response => {
        this.situaciones_peligro = response.data
      }).catch(error => {
        //console.log(error)
      })
    },
    saveReporteMarcador() {
      this.$refs.form_reporte_marcador.validate().then(valid => {
        if (valid) {
          const token = cookies.get("auth_token");

          this.reporte_marcador_data.reporta = this.auth_user.pk;
          const formData = new FormData();
          formData.append("reporta", this.reporte_marcador_data.reporta);
          formData.append("ubicacion", this.reporte_marcador_data.ubicacion);
          formData.append("colonia", this.reporte_marcador_data.colonia);
          formData.append("calle", this.reporte_marcador_data.calle);
          formData.append("numero", this.reporte_marcador_data.numero);
          formData.append("entre_interseccion", this.reporte_marcador_data.entre_interseccion);
          formData.append("tipo", this.reporte_marcador_data.tipo);
          if (this.reporte_marcador_data.tipo === "Servicios") {
            formData.append("tipo_servicio", this.reporte_marcador_data.tipo_servicio);
            if (this.reporte_marcador_data.tipo_servicio < 1000000) {
              formData.append("estado_servicio", this.reporte_marcador_data.estado_servicio);
            } else {
              formData.append("estado_servicio_otro", this.reporte_marcador_data.estado_servicio_otro);
            }
          } else {
            formData.append("situacion_peligrosa", this.reporte_marcador_data.situacion_peligrosa);
            if (this.reporte_marcador_data.situacion_peligrosa < 1000000) {
              formData.append("situacion_peligrosa", this.reporte_marcador_data.situacion_peligrosa);
            } else {
              formData.append("situacion_peligrosa_otra", this.reporte_marcador_data.situacion_peligrosa_otra);
            }
          }
          formData.append("comentarios", this.reporte_marcador_data.comentarios);
          formData.append("fecha", this.reporte_marcador_data.fecha);
          formData.append("hora", this.reporte_marcador_data.hora);
          formData.append("estatus", 'Abierto');

          if (this.evidencia_reporte) {
            formData.append("evidencia_reporte", this.evidencia_reporte);
          }

          axios.post(`https://api.zapopanentrenosotras.com/rest/v1/reportes/`, formData,
            {
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
              }
            }).then(response => {
            this.agregarreportemarcador_dialog = false
            this.reporte_agregado_dialog = true
            this.reporte_marcador_data = {
              colonia: undefined,
              ubicacion: undefined,
              calle: undefined,
              numero: undefined,
              entre_interseccion: undefined,
              tipo: undefined,
              tipo_servicio: undefined,
              estado_servicio: undefined,
              estado_servicio_otro: undefined,
              situacion_peligrosa: undefined,
              situacion_peligrosa_otra: undefined,
              comentarios: undefined,
              fecha: "",
              hora: ""
            }
            this.herramientaActiva = 'info'
          }).then(() => {
            this.mapkey++
            this.$refs.olview.refresh()
            this.$refs.olview.remount()

          }).catch(error => {
            //console.log(error)
          })
        } else {
          return false;
        }
      }).catch(error => {
      });
    },
    buildMVTUrl(capa) {
      let url = capa.url

      const p = capa.params

      const query = []

      if (p.tipo) query.push(`tipo=${p.tipo}`)
      if (p.servicio) query.push(`servicio=${p.servicio}`)
      if (p.situacion) query.push(`situacion=${p.situacion}`)

      if (query.length > 0) {
        url += '?' + query.join('&')
      }

      return url
    },

    // 🎨 FILL EXACTO SEGÚN SLD
    getFill(feature) {
      const estatus = feature.get('estatus')
      const semaforo = (feature.get('color_semaforo') || '').toLowerCase()

      // prioridad por estatus
      if (estatus === 'Atendiendo') return '#ffffff'
      if (estatus === 'Resuelto') return '#00ff00'

      // abierto depende del semáforo
      if (semaforo === 'rojo') return '#ff0000'
      if (semaforo === 'amarillo') return '#f0ff00'

      return '#999999'
    },

    // 🧠 STYLE PRINCIPAL (equivalente al SLD)
    styleReportes(feature) {
      const tipo = feature.get('tipo')
      const estado = feature.get('estado_servicio_id')
      const situacion = feature.get('situacion_peligrosa_id')

      const fill = this.getFill(feature)

      // 🔲 SITUACIONES → cuadrado
      if (tipo === 'Situaciones') {
        const stroke = this.strokeSituaciones[situacion] || '#000000'
        return this.square(fill, stroke)
      }

      // 🔴 SERVICIOS → círculo
      const stroke = this.strokeServicios[estado] || '#000000'
      return this.circle(fill, stroke)
    },

    // 🔴 helper círculo
    circle(fill, stroke) {
      return new Style({
        image: new Circle({
          radius: 7,
          fill: new Fill({color: fill}),
          stroke: new Stroke({
            color: stroke,
            width: 2
          })
        })
      })
    },

    // 🔲 helper cuadrado
    square(fill, stroke) {
      return new Style({
        image: new RegularShape({
          points: 4,
          radius: 10,
          angle: Math.PI / 4,
          fill: new Fill({color: fill}),
          stroke: new Stroke({
            color: stroke,
            width: 2
          })
        })
      })
    }

  },
  mounted() {
    if (this.$q.screen.width < 768) {
      this.zoom = 13;
    }

    this.loadingBar = this.$refs.bar
    // axios.get('statics/zapopan.geojson').then(res => {
    axios.get('https://development.demo.geonode.org/geoserver/ows?service=WMS&version=1.1.1&request=GetFeatureInfo&layers=geonode:mgenmex_municipios&query_layers=geonode:mgenmex_municipios&styles=geonode:mgenmex_municipios&x=51&y=51&height=101&width=101&srs=EPSG:3857&bbox=-11528274.230741149,2360353.554394476,-11512833.951027544,2375793.8341080816&feature_count=10&info_format=application%2Fjson&format=image%2Fpng').then(res => {
      this.zapopan = res.data.features
    }).then(() => {

      this.getColonias()
      this.getTiposServicio()
      this.getSituacionesPeligrosas()
    }).catch(error => {
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
