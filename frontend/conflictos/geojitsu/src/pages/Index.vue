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
            <q-tab v-for="(tab, index) in GISRibbonEnabledTabs" :key="index" :name="tab[0]" :label="tab[1].label"
                   class="q-tab--no-caps tabs-title" @click="showGISRibbon = true"/>
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
                            <div v-for="(capa, idx) of capasMapa" :key="capa.value">
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
                                <vl-source-vector :loaderFactory="loaderFactory(idx)" :url="capa.url"
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
                                  :title="conflictos_selectedFeatures[0].properties.tipo[1] + ' (id:' + conflictos_selectedFeatures[0].properties.pk + ')'"
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
                                    <q-th colspan="2" align="left">
                                      <q-td style="padding: 0">
                                        {{ conflictos_selectedFeatures[0]['properties']['resumen'] }}
                                      </q-td>
                                    </q-th>
                                  </template>
                                  <template v-slot:top-right>
                                    <q-btn flat dense size="sm" style="margin-right: -11px;">
                                      <q-icon name="close"
                                              @click="position = undefined; conflictos_selectedFeatures = []"/>
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
                  <p>fjdlksjfk</p>
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
      zoom: 5.7,
      center: [-102.02, 24.02],
      center3857: [-11268847.24, 2231060.47],
      rotation: 0,
      geolocPosition: [-101.22977709999999, 19.6453138],
      conflictos: [],
      loading: false,
      conflictos_geojson_url: "https://conflictossocioambientales.iies.unam.mx/conflictos/conflictos.geojson",
      conflictos_features: [],
      conflictos_selectedFeatures: [],
      conflictos_styles: {},
      drawer_capas: true,
      mapkey: 0,
      GISRibbonTabs: {
        proyecto: {label: "Proyecto", is_enabled: false},
        mapa: {label: "Mapa", is_enabled: true},
        herramientas: {label: "Herramientas", is_enabled: true},
      }
    }
  },
  watch: {
    capasMapa() {
      this.mapkey++
    },
    mapHeight() {
      this.$refs["olmap"].remount()
    },
    mapaBase() {
      this.$refs["olmap"].updateSize()
    },
    conflictos_selectedFeatures() {
      if (this.conflictos_selectedFeatures.length > 0) {
        //console.log("clic", this.conflictos_selectedFeatures)
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
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'mapaBaseGetter', 'mapasBaseGetter', 'capasMapaGetter', 'getDrawerCapas']),
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      },
      set(value) {
        this.GISRibbonIsOpenAction(value)
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
    ...mapActions('geojitsu', ['capasMapaAction', 'setCapaFeatures', 'setCapaTicked', 'GISRibbonIsOpenAction']),
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
      if (this.capasMapa[capa].features.length === 0) {
        axios.get(this.capasMapa[capa].url).then(response => {
          console.log("geojson", capa, response)
          this.setCapaFeatures({capa: capa, features: response.data.features})
        }).then(() => {
          this.loadingBar.stop()
          this.setCapaTicked({capa: this.capasMapa[capa], visible: true})
        }).catch(error => {
          console.log(error)
        })
      } else {
        if (this.loadingBar)
          this.loadingBar.stop()
      }
    },
    clic(evt) {
      console.log("clic event", evt)
      this.clickCoords = evt.coordinate
    },
    pointsStyleFunc() {
      return (feature) => {
        let img_url = "https://conflictossocioambientales.iies.unam.mx" + feature.values_.tipo_icon_url
        let style = new Style({image: new Icon({src: img_url})})
        /*let baseStyle = new Style({
          image: new Circle({
            radius: 10,
            fill: new Fill({
              color: '#fff',
            }),
            stroke: new Stroke({
              color: '#F44336',
            }),
          }),
          text: new Text({
            text: "yeet", // get feature property
          }),
        }) */
        return style
      }
    }
  },
  mounted() {
    this.loadingBar = this.$refs.bar
    this.loadingBar.start()
  }
}
</script>

<style lang="css" scoped>
.detalles >>> .q-table__top.relative-position.row.items-center {
  flex-wrap: nowrap;
  align-items: flex-start;
}
</style>
