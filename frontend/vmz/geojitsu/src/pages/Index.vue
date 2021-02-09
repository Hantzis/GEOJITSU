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
                  <vl-source-vector :features.sync="zapopan">
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
                        :title="selectedFeatureInfo.tipo"
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
                        <q-select
                          :readonly="!(selectedFeatureInfo.tipo === 'Servicios' && this.userGroups.includes(5)) && !(selectedFeatureInfo.tipo === 'Situaciones' && this.userGroups.includes(6))"
                          v-model="selectedFeatureInfo.estatus"
                          :options="['Abierto', 'Atendiendo', 'Resuelto']"
                          label="Estatus" name="estatus" outlined class="full-width" behavior="menu"/>
                      </div>
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
                        emit-value map-options option-value="id" option-label="nombre"/>
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

    <q-dialog style="width: 1000px" ref="reporte_agregado_dialog" v-model="bienvenida_dialog">
      <q-card style="width: 1000px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-home" color="red" text-color="white"/>
          <q-toolbar-title>Ciudad÷Nosotras</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <div v-for="block of homeData.contenido" :key="block.id">
                <div v-if="block.type === 'image'">
                  <div v-html="block.value"></div>
                </div>
                <div v-if="block.type === 'paragraph'">
                  <span v-html="block.value"></span>
                </div>
                <div v-if="block.type === 'title'">
                  <h5>{{ block.value }}</h5>
                </div>

                <q-list bordered class="rounded-borders">
                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="mdi-account-plus"
                    label="Crear cuenta"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Para poder utilizar esta plataforma es necesario acceder con una cuenta de usuario, si no se
                          tiene una cuenta es muy sencillo crear una. Para crear una cuenta de usuario hay que ir al
                          menú principal ubicado en la esquina superior derecha, en la opción <strong>Crear
                            cuenta</strong>.</p>
                        <img src="statics/bienvenida/crear_cuenta.PNG" width="474">
                        <p>Al acceder a la opción crear cuenta, se desplegará un cuadro de dialogo con varios campos que
                          se deben llenar, estos se detallan a continuación:</p>
                        <p>Nota: todos los campos son obligatorios excepto los que se especifique lo contrario.</p>
                        <ul>
                          <li><strong>Nombre de usuario</strong>: es el identificador (username) a usar para iniciar
                            sesión
                            posteriormente
                          </li>
                          <li><strong>Nombre(s)</strong>: Nombre o nombres, sin apellidos</li>
                          <li><strong>Apellidos</strong>: Apellidos como constan en el registro civil</li>
                          <li><strong>Email</strong>: Dirección de correo electrónico actual</li>
                          <li><strong>Fecha de nacimiento</strong>: Fecha de nacimiento en formato AAAA-MM-DD</li>
                          <li><strong>Sexo</strong>: Género sexual</li>
                          <li><strong>Etnia</strong>: En caso de pertenecer a alguna etnia, seleccionarla, de lo
                            contrario omitirla.
                            (campo no obligatorio)
                          </li>
                          <li><strong>Municipio</strong>: Municipio donde se radica actualmente</li>
                          <li><strong>Colonia</strong>: Colonia donde se radica actualmente</li>
                          <li><strong>Discapacidades</strong>: Si se tiene algúna (o más) tipo de discapacidad, de lo
                            contrario omitir.
                            (campo no obligatorio)
                          </li>
                          <li><strong>Contraseña</strong>: Contraseña (password) para ingresar a la plataforma</li>
                          <li><strong>Confirmar Contraseña</strong>: Contraseña (password) para ingresar a la
                            plataforma, debe ser
                            identica que en campo anterior y se usa una confirmación para asegurar que se ha escrito
                            correctamente.
                          </li>
                        </ul>
                        <p>Una vez llenados todos los campos, se puede pulsar sobre el botón "Crear cuenta", seguido de
                          lo
                          cual, la cuenta estará creada y lista para usar.</p>

                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="login"
                    label="Ingresar (iniciar sesión)"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Como ya se menciona en el punto de arriba, es importante tener una cuenta para poder crear
                          reportes, con dicha cuenta se puede ingresar y entonces registrar reportes.</p>
                        <p>Para ingresar, hay que ir al menú principal ubicado en la esquina superior derecha, en la
                          opción <strong>Ingresar</strong>.</p>
                        <img src="statics/bienvenida/ingresar_cuenta.PNG" width="474">
                        <p>Una vez ahì se solicitara los datos de acceso de nombre de usuario y contraseña, los cuales
                          fueron elegidos durante el registro.</p>
                        <p>Si no se recuerda la contraseña, hay que ingresar alguna contraseña que se recuerde, donde si
                          no es exactamente la contraseña, se mostrará un mensaje que indica que la contraseña es
                          incorrecta, y se mostrará también un botón para recuperar la contraseña.</p>
                        <img src="statics/bienvenida/iniciar_sesion_incorrecto.PNG" width="474">
                        <p>Para recuperar la contraseña hay que pulsar el botón "Restablecer contraseña", el cual
                          mostrará una ventana solicitado la dirección de correo que se utilizó para crear la cuenta. Se
                          debe introducir la dirección de correo y a continuación pulsar el botón "Enviar correo de
                          recuperación". Posteriormente hay que revisar el correo electronico, a donde llegará un enlace
                          para asignar una nueva contraseña. Despues de cambiarla ya se debe poder acceder con la nueva
                          contraseña.</p>
                        <img src="statics/bienvenida/recuperar_contra.PNG" width="474">
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="info"
                    label="Ver info de un reporte"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Para poder visualizar la info de un reporte en particular se debe tener seleccionara la
                          herramienta "info" de la barra de herramientas, en la parte superior izquierda.</p>
                        <img src="statics/bienvenida/info.PNG" width="474">
                        <br>
                        <p>Teniendo seleccionada la herramienta "info", se puede ir al mapa y dar click sobre cualquier
                          punto para obtener la ficha de los detalles de dicho reporte, los cuales se mostraran en una
                          ficha cuya esquina superior izquierda coincide con la ubicación del punto seleccionado</p>
                        <img src="statics/bienvenida/info_ficha.PNG" width="474">
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="mdi-playlist-plus"
                    label="Agregar reporte basado en domicilio"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Se pueden crear reportes a partir de conocer la ubicación de la calle y número del lugar o
                          calles y su calle de intersección.</p>
                        <p>Para crear un nuevo reporte en este modo hay que seleccionar la herramienta de "Agrear
                          reporte basado en domicilio" de la barra de herramientas.</p>
                        <img src="statics/bienvenida/nuevo_domicilio.PNG" width="474">
                        <p>A continuación hay que llenar el formulario con los datos correspondientes a cada campo,
                          dependiendo de las opciones seleccionadas se iran desplegando nuevos campos acorde a lo
                          previamente seleccionado.</p>
                        <p>En esta modalidad de registro, la ubicación espacial se logra a partir de los datos del
                          domicilio. Para una mejor precisión es importante escribir el nombre de la calle completo y
                          solo uno de estos dos: el número postal de la ubicación del caso, o una calle cercana que
                          intersecte.</p>
                        <p>Una vez se ha terminado de llenar los datos, se debe dar clic en el botón <strong>Guardar
                          reporte</strong> y si todo es correcto, se almacenará el registro correspondiente en la base
                          de datos.</p>
                        <p>Nota: Los reportes nuevos no se reflejan en el mapa inmediatamente, hay que esperar unos
                          segundos para su almacenamiento.</p>
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="mdi-map-marker-plus"
                    label="Agregar reporte a partir de un marcador en el mapa"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Se pueden crear reportes a partir de poner un marcador o pin directamente sobre el mapa, en
                          los casos donde resulte más facil ubicar directamente en el mapa esta es la mejor opción.</p>
                        <p>Para crear un nuevo reporte en este modo hay que seleccionar la herramienta de "Agrear
                          reporte ubicando en el mapa" de la barra de herramientas.</p>
                        <img src="statics/bienvenida/nuevo_marcador.PNG" width="474">
                        <p>A continuación hay que llenar el formulario con los datos correspondientes a cada campo,
                          dependiendo de las opciones seleccionadas se iran desplegando nuevos campos acorde a lo
                          previamente seleccionado.</p>
                        <p>En esta modalidad de registro, Los datos de la ubicación del domicilio se obtienen a partir
                          de una consulta espacial a partir de las coordenadas donde se haya hecho click sobre el mapa,
                          y los datos referentes al domicilio se llenan automaticamente.</p>
                        <p>Una vez se ha terminado de llenar los datos del reporte, se debe dar clic en el botón
                          <strong>Guardar reporte</strong> y si todo es correcto, se almacenará el registro
                          correspondiente en la base de datos.</p>
                        <p>Nota: Los reportes nuevos no se reflejan en el mapa inmediatamente, hay que esperar unos
                          segundos para su almacenamiento.</p>
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                </q-list>

              </div>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <q-btn @click="bienvenida_dialog = false" no-caps color="green"
                     label="Entendido" class="full-width"/>
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
import cookies from 'browser-cookies'

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
      homeData: "",
      agregarreportemarcador_dialog: false,
      reporte_agregado_dialog: false,
      bienvenida_dialog: false,
      fecha_reporte_marcador: "",
      hora_reporte_marcador: "",
      zoom: 15,
      center: [-103.38890075683594, 20.72561197927564],
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
    homeData() {
      if (this.homeData) {
        if (!this.auth_logged) {
          this.bienvenida_dialog = true
        }
      }
    },
    selectedFeatures() {
      if (this.selectedFeatures.length > 0 && this.herramientaActiva === 'info') {
        this.layers = [this.$refs.reportes[0]]
        this.position = transform(this.selectedFeatures[0].geometry.coordinates, 'EPSG:3857', 'EPSG:4326')
      } else {
        this.selectedFeatureInfo = {}
      }
    },
    'selectedFeatureInfo.estatus': function (newVal, oldVal) {
      if (oldVal && newVal) {
        this.token = cookies.get("access_token")
        console.log(oldVal);
        console.log(newVal);
        console.log(this.selectedFeatureInfo);
        axios.patch(`https://api-nosotras.inmujereszapopan.gob.mx/api/v1/reportes/${this.selectedFeatureInfo.id}/`,
          {estatus: newVal}, {headers: {'Authorization': `Bearer ${this.token}`}})
          .then(response => {
            console.log(response)
          })
          .catch(error => {
            //console.log(error)
          })
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
    'reporte_marcador_data.colonia': function (newVal, oldVal) {
      console.log(newVal)
      console.log(oldVal)
      console.log(this.reporte_marcador_data.colonia)
    },
    agregarreportemarcador_dialog() {
      if (this.agregarreportemarcador_dialog === false) {
        this.herramientaActiva = 'info'
        this.fecha_reporte_marcador = ""
        this.hora_reporte_marcador = ""
        this.reporte_marcador_data = {
          colonia: undefined, calle: undefined, numero: undefined, entre_interseccion: undefined,
          tipo: undefined, tipo_servicio: undefined, estado_servicio: undefined, estado_servicio_otro: undefined,
          situacion_peligrosa: undefined, situacion_peligrosa_otra: undefined, comentarios: undefined,
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
      'capasMapaGetter', 'getDrawerCapas', 'getMapkey', 'getUserGroups']),
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
    ...mapActions('geojitsu', ['capasMapaAction', 'setCapa', 'setCapaTicked', 'setHerramientaActiva', 'setMapkey',
      'setUserGroups']),
    getEntries(properties) {
      let limpio = [];
      limpio.push(["Fecha", properties.fecha]);
      limpio.push(["Hora", properties.hora]);
      let colonia = properties.colonia_display;
      if (properties.colonia_cp_display) colonia = colonia + " (" + properties.colonia_cp_display + ")";
      limpio.push(["Colonia", colonia]);
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
        axios.get(url).then(response => {
          if (response.data.numberReturned > 0) {
            this.selectedFeatures = response.data.features
            axios.get(`https://api-nosotras.inmujereszapopan.gob.mx/api/v1/reportes/${response.data.features[0].id.split(".")[1]}/`)
              .then(response => {
                this.selectedFeatureInfo = response.data
              })
          }
        }).catch(error => {
          //console.log(error)
        })
      }
      if (this.herramientaActiva === 'agregar_marcador') {
        const coord = transform(evt.coordinate, 'EPSG:4326', 'EPSG:3857')
        const viewResolution = this.$refs.olview.$view.values_.resolution;
        axios.get(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${evt.coordinate[1]},${evt.coordinate[0]}&key=AIzaSyAPJOFYKRav1z3IxoK-URalWtPY4KKTAb0`)
          .then(response => {
            console.log("response", response)
            if (response.data.results.length > 0) {
              this.reporte_marcador_data.ubicacion = `SRID=4326;POINT (${evt.coordinate[0]} ${evt.coordinate[1]})`
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
                if (response.data.features.length > 0) {
                  const col = response.data.features[0]
                  this.reporte_marcador_data.colonia = parseInt(col.id.split(".")[1])
                  this.agregarreportemarcador_dialog = true
                } else {
                  this.herramientaActiva = 'info'
                }
              }).catch(error => {
                //console.log(error))
              })
            }
          }).catch(error => {
          //console.log(error)
        })
      }
    },
    getColonias() {
      axios.get(`https://api-nosotras.inmujereszapopan.gob.mx/api/v1/colonias/?municipio=120`).then(response => {
        this.colonias = response.data
        console.log("colonias", this.colonias)
      }).catch(error => {
        //console.log(error)
      })
    },
    getTiposServicio() {
      axios.get(`https://api-nosotras.inmujereszapopan.gob.mx/api/v1/tipos-servicio/`).then(response => {
        this.tipos_servicio = response.data
        console.log("tipos_servicio", this.tipos_servicio)
      }).catch(error => {
        //console.log(error)
      })
    },
    getEstadosServicio(val) {
      if (val && val < 1000000) {
        axios.get(`https://api-nosotras.inmujereszapopan.gob.mx/api/v1/estados-servicio/?tipo=${val}`).then(response => {
          this.estados_servicio = response.data
          console.log("estados_servicio", this.estados_servicio)
        }).catch(error => {
          //console.log(error)
        })
      } else {
        this.estados_servicio = undefined
      }
    },
    getSituacionesPeligrosas() {
      axios.get(`https://api-nosotras.inmujereszapopan.gob.mx/api/v1/situaciones-peligro/`).then(response => {
        this.situaciones_peligro = response.data
        console.log("situaciones_peligrosas", this.situaciones_peligro)
      }).catch(error => {
        //console.log(error)
      })
    },
    saveReporteMarcador() {
      this.$refs.form_reporte_marcador.validate().then(valid => {
        if (valid) {
          this.token = cookies.get("access_token");
          this.reporte_marcador_data.reporta = this.auth_user.pk;
          axios.post(`https://api-nosotras.inmujereszapopan.gob.mx/api/v1/reportes/`, this.reporte_marcador_data,
            {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
            console.log(response.data)
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
          }).catch(error => {
            //console.log(error)
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      }).catch(error => {
      });
    },
    getPaginaHome() {
      // axios.get("https://api-nosotras.inmujereszapopan.gob.mx/api/v1/pages/?type=home.HomePage")
      axios.get("https://api-nosotras.inmujereszapopan.gob.mx/api/v1/pages/3/")
        .then(response => {
          console.log("response getPagina", response)
          this.homeData = response.data
        })
    },
  },
  mounted() {
    if (this.$q.screen.width < 768) {
      this.zoom = 13;
    }

    this.loadingBar = this.$refs.bar
    axios.get('statics/zapopan.geojson').then(res => {
      console.log(res.data.features)
      this.zapopan = res.data.features
    }).then(() => {
      this.getPaginaHome()
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
