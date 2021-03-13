<template>
  <q-page>
    <q-layout view="lHh Lpr lff" container :style="{height: mainScreenHeight}">
      <q-header>
      </q-header>

      <q-page-container>
        <q-page>

          <q-tabs
            v-model="activeTab"
            dense
            class="bg-grey-4 text-grey-7"
            active-color="grey-9"
            indicator-color="primary"
            active-bg-color="grey-1"
            align="left">
            <q-route-tab no-caps v-for="tab of GISRibbonTabs.filter(val => val.is_enabled === true)" :key="tab.value"
                         :name="tab.value"
                         :label="tab.label" :to="tab.value === 'mapa' ? '/' : tab.value"/>
            <q-route-tab no-caps v-for="pagina of paginas.items" :key="pagina.meta.slug" :name="pagina.meta.slug"
                         :label="pagina.title" :to="pagina.meta.slug"/>
          </q-tabs>

          <q-tab-panels v-model="activeTab" class="bg-grey-1 text-grey-9">

            <q-tab-panel name="mapa" class="no-padding">
              <q-layout view="lHh Lpr lff" container :style="{height: viewScreenHeight}">
                <q-header>
                  <GISRibbon v-show="showGISRibbon"/>
                </q-header>

                <q-page-container>
                  <q-page>

                    <q-separator color="grey-5"/>

                    <div class="row">
                      <div class="col" :style="{'min-height': mapHeight}">
                        <vl-map @click="clic" ref="olmap" :load-tiles-while-animating="true"
                                :load-tiles-while-interacting="true"
                                data-projection="EPSG:4326"
                                :style="{'min-height': 'inherit', 'max-height': '1px', 'width': '100%', 'background-color': mapaBase.bgcolor}">
                          <vl-view ref="map_view" :zoom.sync="zoom" :center.sync="center"
                                   :rotation.sync="rotation"></vl-view>

                          <!--
                          <vl-geoloc @update:position="geolocPosition = $event">
                            <template slot-scope="geoloc">
                              <vl-feature v-if="geoloc.position" id="position-feature">
                                <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
                                <vl-style-box>
                                  <vl-style-icon
                                    src="/statics/icons/Map-Marker.png"
                                    :scale="0.2" :anchor="[0.5, 1]"></vl-style-icon>
                                </vl-style-box>
                              </vl-feature>
                            </template>
                          </vl-geoloc>
                          -->

                          <vl-layer-tile>
                            <vl-source-xyz
                              :url="mapaBase.url"
                              attributions="Mapbox, <a href='https://www.saeba.click' target='_blank'>Saeba</a>"/>
                          </vl-layer-tile>

                          <div :key="mapkey">
                            <div v-for="(capa) of capasMapa" :key="capa.value">
                              <vl-layer-tile v-if="capa.type==='wms'" :opacity="capa.opacity" :visible="capa.visible">
                                <vl-source-wms
                                  :url="capa.url"
                                  :format="capa.format"
                                  :server_type="capa.server_type"
                                  :layers="capa.layers"
                                  :attributions="capa.attribution"
                                  :ext-params="capa.params"
                                  :projection="capa.params.crs"
                                />
                              </vl-layer-tile>
                              <vl-layer-vector v-if="capa.type==='vector'" :opacity="capa.opacity"
                                               :visible="capa.visible">
                                <vl-source-vector :features="capa.features"
                                                  :attributions="capa.attribution"/>
                                <vl-style-func :factory="pointsStyleFunc"/>
                              </vl-layer-vector>
                            </div>
                          </div>

                          <vl-interaction-select :features.sync="conflictos_selectedFeatures">
                            <vl-overlay v-if="position && conflictos_selectedFeatures.length > 0" :position="position"
                                        :auto-pan="true"
                                        style="background: white; padding: 8px">
                              <div style="max-width: 300px; min-width: 300px;">
                                <q-table
                                  class="detalles"
                                  style="max-height: 400px; max-width: 300px"
                                  :title="conflictos_selectedFeatures[0].properties['tipo_conflicto'] + ' (id:' + conflictos_selectedFeatures[0].id + ')'"
                                  square
                                  wrap-cells
                                  dense
                                  :rows-per-page-options="[15]"
                                  virtual-scroll
                                  separator="cell"
                                  hide-bottom
                                  :data="getEntries(conflictos_selectedFeatures[0].properties)"
                                >
                                  <template v-slot:header>
                                    <q-tr align="left">
                                      <q-td v-if="!ver_mas" colspan="2">
                                        {{ conflictos_selectedFeatures[0].properties['resumen'].slice(0, 240) + '...' }}
                                        <span @click="ver_mas = true" style="cursor: pointer; font-weight: bold;"> Ver mas</span>
                                        <q-separator/>
                                      </q-td>
                                      <q-td v-if="ver_mas" colspan="2">
                                        {{ conflictos_selectedFeatures[0].properties['resumen'] }}
                                        <span @click="ver_mas = false" style="cursor: pointer; font-weight: bold;"> Ver menos</span>
                                        <q-separator/>
                                      </q-td>
                                    </q-tr>
                                  </template>
                                  <template v-slot:top-right>
                                    <q-btn flat dense size="sm" style="margin-right: -11px;">
                                      <q-icon name="close"
                                              @click="position = undefined; conflictos_selectedFeatures = []; ver_mas = false;"/>
                                    </q-btn>
                                  </template>
                                </q-table>
                              </div>
                            </vl-overlay>
                          </vl-interaction-select>
                        </vl-map>
                      </div>
                    </div>

                    <mapa-drawer-capas/>

                  </q-page>
                </q-page-container>
              </q-layout>
            </q-tab-panel>

            <q-tab-panel name="herramientas" class="no-padding">
              <div class="row q-pa-md">
                <div class="col">
                  <p>herramientas</p>
                </div>
              </div>
            </q-tab-panel>

            <q-tab-panel name="metodologia" class="no-padding">
              <q-layout view="lHh Lpr lff" container :style="{height: viewScreenHeight}">
                <q-header></q-header>
                <q-page-container>
                  <q-page>
                    <q-separator color="grey-5"/>
                    <div class="column fit justify-between">
                      <div class="col q-pa-md">
                        <p>metodología</p>
                      </div>
                    </div>
                  </q-page>
                </q-page-container>
              </q-layout>
            </q-tab-panel>

            <q-tab-panel name="agradecimiento" class="no-padding">
              <div class="row q-pa-md">
                <div class="col">
                  <p>agradecimiento</p>
                </div>
              </div>
            </q-tab-panel>
            <q-tab-panel name="tablero" class="no-padding">
              <div class="row q-pa-md">
                <div class="col">
                  <p>tablero</p>
                </div>
              </div>
            </q-tab-panel>


          </q-tab-panels>


        </q-page>
      </q-page-container>
    </q-layout>
    <q-ajax-bar
      ref="bar"
      position="top"
      color="primary"
      size="4px"
      skip-hijack
    />
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

Vue.use(VueLayers)

export default {
  name: 'PageIndex',
  components: {MapaDrawerCapas, GISRibbon},
  data() {
    return {
      activeTab: 'mapa',
      loadingBar: undefined,
      clickCoords: undefined,
      position: undefined,
      ver_mas: false,
      paginaInicioID: 0,
      paginas: [],
      zoom: 5.7,
      center: [-102.02, 24.02],
      center3857: [-11268847.24, 2231060.47],
      rotation: 0,
      geolocPosition: [-101.22977709999999, 19.6453138],

      loading: false,
      simbologias: ['Tipos', 'Organizaciones', 'Secretarías', 'Empresas'],
      simbologiasDict: {
        'tipo_icon_url': 'Tipos',
        'organizacion_icon_url': 'Organizaciones',
        'secretaria_icon_url': 'Secretarías',
        'empresa_icon_url': 'Empresas'
      },
      conflictos_selectedFeatures: [],
      vectorLayersStyles: {},
      drawer_capas: true,
      mapkey: 0,
      GISRibbonTabs: [
        {value: 'mapa', label: "Mapa", is_enabled: true},
        {value: 'herramientas', label: "Herramientas", is_enabled: false},
      ]
    }
  },
  watch: {
    capasMapa() {
      this.mapkey++
    },
    simbologiaTipo() {
      this.mapkey++
    },
    mapHeight() {
      this.$refs["olmap"].remount()
    },
    mapaBase() {
      this.$refs["olmap"].updateSize()
    },
    conflictos_selectedFeatures() {
      this.ver_mas = false
      if (this.conflictos_selectedFeatures.length > 0) {
        console.log("clic", this.conflictos_selectedFeatures)
        for (let feat of this.conflictos_selectedFeatures) {
          /*console.log("feat: ", feat)
          console.log("feat coordinates: ", feat.geometry.coordinates)
          console.log("this.clickCoords: ", this.clickCoords)*/
        }
        let collection = []
        for (let point of this.conflictos_selectedFeatures[0].geometry.coordinates) {
          let a = turf.point(point)
          collection.push(a)
        }
        let featureCoords = turf.featureCollection(collection)
        let cercano = turf.nearestPoint(this.clickCoords, featureCoords)
        this.position = cercano.geometry.coordinates
      }
    },
    /* drawerCapas() {
      setTimeout(() => {
        this.$refs["olmap"].remount()
      }, 400);
    }, */
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'mapaBaseGetter', 'mapasBaseGetter', 'capasMapaGetter', 'getDrawerCapas', 'getSimbologiaTipo']),
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      },
      set(value) {
        this.GISRibbonIsOpenAction(value)
      }
    },
    simbologiaTipo: {
      get() {
        return this.getSimbologiaTipo
      },
      set(value) {
        this.setSimbologiaTipo(value)
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
      let ribbon_height = 87
      if (this.showGISRibbon) ribbon_height = 172
      return this.$q.screen.height - ribbon_height + "px"
    },
    viewScreenHeight() {
      return this.$q.screen.height - 86 + "px"
    },

    mainScreenHeight() {
      return this.$q.screen.height - 50 + "px"
    },
    GISRibbonEnabledTabs() {
      let enabled_tabs = [];
      for (let tab of Object.entries(this.GISRibbonTabs)) {
        if (tab[1].is_enabled) {
          enabled_tabs.push(tab)
        }
      }
      return enabled_tabs
    }
  },
  methods: {
    ...mapActions('geojitsu', ['capasMapaAction', 'setCapaFeatures', 'setCapaTicked', 'GISRibbonIsOpenAction', 'setSimbologiaTipo']),
    getEntries(properties) {
      let limpio = []
      Object.entries(properties).forEach((row) => {
        const esconder = ['pk', 'resumen', 'tipo', 'publicaciones_texto', 'publicaciones', 'bibliografia',
          'estados', 'municipios', 'secretarias', 'organizaciones', 'empresas', 'pueblos_originarios']
        if (row[1] && row[1].length && !esconder.includes(row[0])
          && !row[0].endsWith('icon_url') && !row[0].endsWith('nombre_texto')) {
          if (row[0] === 'estados_nombre_lista') row[0] = 'Estados'
          if (row[0] === 'municipios_nombre_lista') row[0] = 'Municipios'
          if (row[0] === 'empresas_nombre_lista') row[0] = 'Empresas'
          if (row[0] === 'organizaciones_nombre_lista') row[0] = 'Organizaciones'
          if (row[0] === 'secretarias_nombre_lista') row[0] = 'Secretarías'
          if (row[0] === 'publicaciones_lista') row[0] = 'Publicaciones'
          if (row[0] === 'fecha_registro') {
            row[0] = 'Fecha de registro'
            const ds = row[1].split('-')
            const d = new Date(ds[0], ds[1], ds[2]);
            const ye = new Intl.DateTimeFormat('es', {year: 'numeric'}).format(d);
            const mo = new Intl.DateTimeFormat('es', {month: 'short'}).format(d);
            const da = new Intl.DateTimeFormat('es', {day: '2-digit'}).format(d);
            row[1] = `${da} de ${mo} de ${ye}`
          }
          if (row[0] === 'fecha_inicio') row[0] = 'Fecha de inicio'
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
    clic(evt) {
      console.log("clic event", evt)
      this.clickCoords = evt.coordinate
    },
    pointsStyleFunc() {
      return (feature) => {
        if (!this.simbologiaTipo) {
          this.simbologiaTipo = 'Tipos'
        }
        return this.vectorLayersStyles['conflictos'][this.simbologiaTipo][feature.id_]
      }
    },
    preloadGeoJSONLayers() {
      this.capasMapa.forEach((capa, index) => {
        if (capa.server_type === 'geojson') {
          axios.get(capa.url).then(response => {
            this.vectorLayersStyles[capa.value] = {}
            this.vectorLayersStyles[capa.value]['Tipos'] = {}
            this.vectorLayersStyles[capa.value]['Organizaciones'] = {}
            this.vectorLayersStyles[capa.value]['Secretarías'] = {}
            this.vectorLayersStyles[capa.value]['Empresas'] = {}
            this.setCapaFeatures({capa: index, features: response.data.features})
            if (response.data.features) {
              if (response.data.features.length) {
                response.data.features.forEach(feature => {
                  // console.log("feature.properties", feature.id, feature.properties)
                  Object.entries(feature.properties).forEach(property => {
                    if (property[0].endsWith('icon_url')) {
                      // console.log("property", property[0])
                      // console.log("capa.value", capa.value)
                      this.vectorLayersStyles[capa.value]['Tipos'][feature.id] = new Style({image: new Icon({src: 'https://conflictossocioambientales.iies.unam.mx' + feature.properties.tipo_icon_url})})
                      this.vectorLayersStyles[capa.value]['Organizaciones'][feature.id] = new Style({image: new Icon({src: 'https://conflictossocioambientales.iies.unam.mx' + feature.properties.organizacion_icon_url})})
                      this.vectorLayersStyles[capa.value]['Secretarías'][feature.id] = new Style({image: new Icon({src: 'https://conflictossocioambientales.iies.unam.mx' + feature.properties.secretaria_icon_url})})
                      this.vectorLayersStyles[capa.value]['Empresas'][feature.id] = new Style({image: new Icon({src: 'https://conflictossocioambientales.iies.unam.mx' + feature.properties.empresa_icon_url})})
                    }
                  })
                })
              }
            }
            console.log("styles", this.vectorLayersStyles)
          }).then(() => {
            this.setCapaTicked({capa: this.capasMapa[index], visible: true})
          }).catch(error => {
            console.log(error)
          })
        }
      })
    },
    getPaginas() {
      axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/wagtail/pages/?type=conflictos.Inicio`).then(response => {
        if (response.data.meta.total_count === 1) {
          console.log("Si", response.data.items[0]['id'])
          const inicioID = Promise.resolve(response.data.items[0]['id'])
          inicioID.then(id => {
            axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/wagtail/pages/?child_of=${id}`).then(response => {
              this.paginas = response.data
              console.log("paginas", this.paginas)
              console.log("this.GISRibbonTabs", this.GISRibbonTabs)
            })
          })
        } else {
          Promise.reject("No hay página de inicio")
        }
      }).catch(error => {
        console.log(error)
      })
    },
  },
  beforeMount() {
    this.getPaginas()
  },
  mounted() {
    this.loadingBar = this.$refs.bar
    this.loadingBar.start()

    this.preloadGeoJSONLayers()
    console.log("fin preload")
    console.log("fin get paginas")
    this.loadingBar.stop()
  }
}
</script>

<style lang="css" scoped>
.detalles >>> .q-table__top.relative-position.row.items-center {
  flex-wrap: nowrap;
  align-items: flex-start;
}
</style>
