<template>
  <div>
    <q-tabs style="padding: 0" align="left" v-show="showGISRibbon" class="bg-white text-grey-9">
      <div name="mapa" class="no-padding">
        <div class="row no-wrap">
          <div class="col-auto">
            <div class="row">
              <div class="col align-stretch">
                <div class="row q-pa-xs q-pt-xs1 q-pl-xs q-pr-xs">
                  <q-btn-toggle
                    v-if="!auth_logged"
                    style="border-radius: 0;"
                    v-model="herramientaActiva"
                    unelevated
                    text-color="grey-7"
                    toggle-text-color="white"
                    toggle-color="pink"
                    :options="[
                        {value: 'info', slot: 'info'},
                      ]"
                  >
                    <template v-slot:info>
                      <q-icon name="mdi-information" size="lg" style="margin: 0 -10px 0 -10px;">
                        <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                   anchor="top middle"
                                   self="bottom middle">
                          Obtener información de un punto
                        </q-tooltip>
                      </q-icon>
                    </template>
                    <template v-slot:agregar_domicilio>
                      <q-icon name="mdi-playlist-plus" size="lg" style="margin: 0 -10px 0 -10px;">
                        <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                   anchor="top middle"
                                   self="bottom middle">
                          Agregar nuevo reporte mediante domicilio
                        </q-tooltip>
                      </q-icon>
                    </template>
                    <template v-slot:agregar_marcador>
                      <q-icon name="mdi-map-marker-plus" size="lg" style="margin: 0 -10px 0 -10px;">
                        <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                   anchor="top middle"
                                   self="bottom middle">
                          Agregar nuevo reporte ubicando en el mapa
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-btn-toggle>
                  <q-btn-group unelevated v-if="!auth_logged">
                    <q-btn unelevated dense size="lg" disable icon="mdi-playlist-plus"/>
                    <q-btn unelevated dense size="lg" disable icon="mdi-map-marker-plus"/>
                  </q-btn-group>
                  <q-btn-toggle
                    @click="showHerramientaActiva()"
                    v-if="auth_logged"
                    style="border-radius: 0;"
                    v-model="herramientaActiva"
                    unelevated
                    text-color="grey-7"
                    toggle-text-color="white"
                    toggle-color="pink"
                    :options="[
                        {value: 'info', slot: 'info'},
                        {value: 'agregar_domicilio', slot: 'agregar_domicilio'},
                        {value: 'agregar_marcador', slot: 'agregar_marcador'},
                      ]"
                  >
                    <template v-slot:info>
                      <q-icon name="mdi-information" size="lg" style="margin: 0 -10px 0 -10px;">
                        <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                   anchor="top middle"
                                   self="bottom middle">
                          Obtener información de un punto
                        </q-tooltip>
                      </q-icon>
                    </template>
                    <template v-slot:agregar_domicilio>
                      <q-icon name="mdi-playlist-plus" size="lg" style="margin: 0 -10px 0 -10px;"
                              @click="agregarreportedomicilio_dialog=true">
                        <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                   anchor="top middle"
                                   self="bottom middle">
                          Agregar nuevo reporte mediante domicilio
                        </q-tooltip>
                      </q-icon>
                    </template>
                    <template v-slot:agregar_marcador>
                      <q-icon name="mdi-map-marker-plus" size="lg" style="margin: 0 -10px 0 -10px;">
                        <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px"
                                   anchor="top middle"
                                   self="bottom middle">
                          Agregar nuevo reporte ubicando en el mapa
                        </q-tooltip>
                      </q-icon>
                    </template>
                  </q-btn-toggle>
                </div>
              </div>
            </div>
            <div class="row justify-between" style="margin-top: 15px;">
              <div class="col-auto">
                <div class="row q-px-sm"/>
              </div>
              <div class="col-auto">
                Herramientas
              </div>
              <div class="col-auto">
                <div class="row q-px-sm"/>
              </div>
            </div>
          </div>

          <q-separator vertical/>

          <mapa-bloque-mapa-base/>

          <q-separator vertical/>

        </div>

      </div>
    </q-tabs>

    <q-separator color="grey-5"/>

    <q-dialog ref="agregarreportedomicilio_dialog" v-model="agregarreportedomicilio_dialog" persistent>
      <q-card style="width: 680px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-playlist-plus" color="pink" text-color="white"/>
          <q-toolbar-title>Agregar reporte</q-toolbar-title>
          <!-- domicilio -->
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <p>Agrear reporte utilizando el domicilio textual con calle y número o intersección de calle.</p>
          </div>

          <q-form ref="form_reporte_domicilio" autocomplete="off" greedy>
            <div class="row q-py-xs">
              <div class="col-6">
                <q-input outlined class="full-width" mask="date"
                         name="fecha_reporte" v-model="fecha_reporte_domicilio"
                         label="Fecha" :rules="[val => !!val || 'Fecha obligatoria']">
                  <template v-slot:default>
                    <q-popup-proxy ref="qDateProxy" transition-show="scale" mask="date" transition-hide="scale">
                      <q-date v-model="fecha_reporte_domicilio">
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
                         name="hora_reporte" v-model="hora_reporte_domicilio"
                         label="Hora" :rules="[val => !!val || 'Hora obligatoria']">
                  <template v-slot:default>
                    <q-popup-proxy transition-show="scale" mask="time" transition-hide="scale">
                      <q-time v-model="hora_reporte_domicilio" format24h>
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
              <q-select class="full-width" outlined name="colonia" v-model="reporte_domicilio_data.colonia"
                        :options="colonias"
                        label="Colonia" :rules="[val => !!val || 'Colonia obligatoria']"
                        emit-value map-options option-value="id" option-label="nombre"/>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="calle" v-model="reporte_domicilio_data.calle"
                       :rules="[val => !!val || 'Calle obligatoria']"
                       label="Calle"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 20px;">
              <q-input outlined class="full-width" name="calle" type="number" v-model="reporte_domicilio_data.numero"
                       label="Número exterior"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 20px;">
              <q-input outlined class="full-width" name="entre_interseccion"
                       v-model="reporte_domicilio_data.entre_interseccion"
                       label="Calle intersección"/>
            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined name="tipo" v-model="reporte_domicilio_data.tipo"
                        :options="['Servicios', 'Situaciones']"
                        label="Tipo de reporte" :rules="[val => !!val || 'Tipo obligatorio']"/>
            </div>
            <div v-if="reporte_domicilio_data.tipo === 'Servicios'">
              <div class="row q-py-xs">
                <q-select class="full-width" outlined name="tipo_servicio"
                          v-model="reporte_domicilio_data.tipo_servicio"
                          :options="tipos_servicio"
                          label="Tipo de servicio" :rules="[val => !!val || 'Tipo de servicio obligatorio']"
                          emit-value map-options option-value="id" option-label="nombre"/>
              </div>
              <div class="row q-py-xs">
                <q-select v-if="reporte_domicilio_data.tipo_servicio < 1000000" class="full-width" outlined
                          name="estado_servicio" v-model="reporte_domicilio_data.estado_servicio"
                          :options="estados_servicio"
                          :rules="[val => !!val || 'Estado de servicio obligatorio']"
                          label="Estado de servicio"
                          emit-value map-options option-value="id" option-label="nombre"/>
                <q-input v-if="reporte_domicilio_data.tipo_servicio === 1000000" outlined class="full-width"
                         name="estado_servicio_otro"
                         v-model="reporte_domicilio_data.estado_servicio_otro"
                         :rules="[val => !!val || 'Otro servicio obligatorio']"
                         label="Otro tipo de servicio"/>
              </div>
            </div>
            <div v-if="reporte_domicilio_data.tipo === 'Situaciones'">
              <div class="row q-py-xs">
                <q-select class="full-width" outlined name="situacion_peligrosa"
                          v-model="reporte_domicilio_data.situacion_peligrosa"
                          :options="situaciones_peligro"
                          label="Situación de peligro" :rules="[val => !!val || 'Situación de peligro obligatoria']"
                          emit-value map-options option-value="id" option-label="nombre"/>
              </div>
              <div class="row q-py-xs">
                <q-input v-if="reporte_domicilio_data.situacion_peligrosa === 1000000" outlined class="full-width"
                         name="situacion_peligrosa_otra"
                         v-model="reporte_domicilio_data.situacion_peligrosa_otra"
                         :rules="[val => !!val || 'Otra situación obligatorio']"
                         label="Detalle de estado de servicio"/>
              </div>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 20px;">
              <q-input outlined class="full-width" name="comentarios" autogrow
                       v-model="reporte_domicilio_data.comentarios"
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

  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

import MapaBloqueMapaBase from "components/gisribbon_components/mapa/MapaBloqueMapaBase";
import axios from "axios";
import cookies from 'browser-cookies'

export default {
  name: "GISRibbon",
  // eslint-disable-next-line vue/no-unused-components
  components: {
    MapaBloqueMapaBase,
  },
  data() {
    return {
      colonias: undefined,
      tipos_servicio: undefined,
      estados_servicio: undefined,
      situaciones_peligro: undefined,
      fecha_reporte_domicilio: "",
      hora_reporte_domicilio: "",
      agregarreportedomicilio_dialog: false,
      reporte_agregado_dialog: false,
      reporte_domicilio_data: {
        colonia: undefined, calle: undefined, numero: undefined, entre_interseccion: undefined,
        tipo: undefined, tipo_servicio: undefined, estado_servicio: undefined, estado_servicio_otro: undefined,
        situacion_peligrosa: undefined, situacion_peligrosa_otra: undefined, comentarios: undefined,
        fecha: "", hora: ""
      }
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getHerramientaActiva']),
    ...mapGetters('auth', ['logged', 'user']),
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
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      },
      set(value) {
        this.GISRibbonIsOpenAction(value)
      }
    },
  },
  methods: {
    ...mapActions('geojitsu', ['GISRibbonIsOpenAction', 'setHerramientaActiva', 'setMapkey']),
    showHerramientaActiva() {
      console.log(this.herramientaActiva)
    },
    getColonias() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/colonias/?municipio=120`).then(response => {
        this.colonias = response.data
        console.log("colonias", this.colonias)
      }).catch(error => console.log(error))
    },
    getTiposServicio() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/tipos-servicio/`).then(response => {
        this.tipos_servicio = response.data
        console.log("tipos_servicio", this.tipos_servicio)
      }).catch(error => console.log(error))
    },
    getEstadosServicio(val) {
      if (val && val < 1000000) {
        axios.get(`https://api.zapopanentrenosotras.com/rest/v1/estados-servicio/?tipo=${val}`).then(response => {
          this.estados_servicio = response.data
          console.log("estados_servicio", this.estados_servicio)
        }).catch(error => console.log(error))
      } else {
        this.estados_servicio = undefined
      }
    },
    getSituacionesPeligrosas() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/situaciones-peligro/`).then(response => {
        this.situaciones_peligro = response.data
        console.log("situaciones_peligrosas", this.situaciones_peligro)
      }).catch(error => console.log(error))
    },
    saveReporteDomicilio() {

      this.$refs.form_reporte_domicilio.validate().then(valid => {
        if (valid) {

          let domicilio = `${this.reporte_domicilio_data.calle}, `
          if (this.reporte_domicilio_data.numero) {
            domicilio += `${this.reporte_domicilio_data.numero}, `
          } else if (this.reporte_domicilio_data.entre_interseccion) {
            domicilio += `${this.reporte_domicilio_data.entre_interseccion}, `
          }
          for (let col of this.colonias)
            if (col.id === this.reporte_domicilio_data.colonia)
              domicilio += `${col.nombre}, `
          domicilio += 'Zapopan'
          this.token = cookies.get("auth_token")

          axios.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${domicilio}&key=AIzaSyAPJOFYKRav1z3IxoK-URalWtPY4KKTAb0`)
            .then(response => {
              console.log("API", response)

              if (response.data.results[0]) {
                let punto = response.data.results[0].geometry.location
                this.reporte_domicilio_data.ubicacion = `SRID=4326;POINT (${punto.lng} ${punto.lat})`
                this.reporte_domicilio_data.reporta = this.auth_user.pk
                console.log(this.reporte_domicilio_data)
                this.token = cookies.get("auth_token")
                axios.post(`https://api.zapopanentrenosotras.com/rest/v1/reportes/`, this.reporte_domicilio_data,
                  {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
                  console.log(response.data)
                  this.reporte_agregado_dialog = true
                  this.agregarreportedomicilio_dialog = false
                  this.reporte_domicilio_data = {
                    colonia: undefined,
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
                }).catch(error => {
                  console.log(error)
                })
              }


            }).then(() => {
            console.log("despues")

          }).catch(error => {
            console.log(error)
          }).finally(() => {
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });

    }

  },
  watch: {
    agregarreportedomicilio_dialog() {
      if (this.agregarreportedomicilio_dialog === false) {
        this.herramientaActiva = 'info'
        this.fecha_reporte_domicilio = ""
        this.hora_reporte_domicilio = ""
        this.reporte_domicilio_data = {
          colonia: undefined, calle: undefined, numero: undefined, entre_interseccion: undefined,
          tipo: undefined, tipo_servicio: undefined, estado_servicio: undefined, estado_servicio_otro: undefined,
          situacion_peligrosa: undefined, situacion_peligrosa_otra: undefined, comentarios: undefined,
          fecha: "", hora: ""
        }
      }
    },
    'reporte_domicilio_data.tipo': function () {
      this.reporte_domicilio_data.estado_servicio = undefined
      this.reporte_domicilio_data.estado_servicio_otro = undefined
      this.reporte_domicilio_data.situacion_peligrosa = undefined
      this.reporte_domicilio_data.situacion_peligrosa_otra = undefined
    },
    'reporte_domicilio_data.tipo_servicio': function (newVal, oldVal) {
      console.log(newVal)
      console.log(oldVal)
      if (newVal) {
        this.reporte_domicilio_data.estado_servicio = undefined
        this.getEstadosServicio(newVal)
      }
    },
    'fecha_reporte_domicilio': function () {
      if (this.fecha_reporte_domicilio !== "") {
        this.reporte_domicilio_data.fecha = this.fecha_reporte_domicilio.split("/").join("-")
      }
    },
    'hora_reporte_domicilio': function () {
      if (this.hora_reporte_domicilio !== "") {
        this.reporte_domicilio_data.hora = this.hora_reporte_domicilio
      }
    },
  },
  mounted() {
    this.getColonias()
    this.getTiposServicio()
    this.getSituacionesPeligrosas()
  }
}
</script>

<style lang="css" scoped>
.tabs-title >>> .q-tab__label {
  font-size: 16px;
  font-weight: 300;
}

.q-separator--vertical {
  flex-shrink: 0;
}
</style>
