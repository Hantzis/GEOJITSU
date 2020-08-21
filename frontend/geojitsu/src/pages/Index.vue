<template>
  <q-page>
    <div class="row">
      <div class="col">
        <GISRibbon/>
      </div>
    </div>
    <div class="row">
      <div class="col" :style="{'min-height': mapHeight}">
        <vl-map @click="clic" ref="olmap" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
                data-projection="EPSG:4326"
                :style="{'min-height': 'inherit', 'max-height': '1px', 'width': '100%', 'background-color': mapaBase.bgcolor}">
          <vl-view ref="map_view" :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>
          <vl-geoloc @update:position="geolocPosition = $event">
            <template slot-scope="geoloc">
              <vl-feature v-if="geoloc.position" id="position-feature">
                <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
                <vl-style-box>
                  <vl-style-icon src="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png"
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

          <div v-for="capa of capasMapa" :key="capa.value">
            <vl-layer-tile v-if="capa.type==='wms'" :opacity="capa.opacity" :visible="capa.visible">
              <vl-source-wms
                :url="capa.url"
                :format="capa.format"
                :serverType="capa.server_type"
                :layers="capa.layers"
                :attributions="capa.attribution"
                :ext-params="capa.params" />
            </vl-layer-tile>
            <vl-layer-vector v-if="capa.type==='vector'" :opacity="capa.opacity">
              <vl-source-vector :url="capa.url" :features.sync="conflictos_features"
                                :attributions="capa.attribution" />
              <vl-style-func :factory="pointsStyleFunc"/>
            </vl-layer-vector>

          </div>


          <vl-interaction-select :features.sync="conflictos_selectedFeatures"/>


        </vl-map>
      </div>
    </div>
  </q-page>
</template>

<script>
import {mapGetters} from 'vuex'
import turf from '@turf/turf'


import axios from 'axios'
import Vue from 'vue'
import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'
import GISRibbon from "components/GISRibbon"; // needs css-loader
import Style from 'ol/style/Style'
import Icon from 'ol/style/Icon'

Vue.use(VueLayers)

export default {
  name: 'PageIndex',
  components: {GISRibbon},
  data() {
    return {
      clickCoords: undefined,
      zoom: 5.7,
      center: [-101.22977709999999, 24.02],
      center3857: [-11268847.24, 2231060.47],
      rotation: 0,
      geolocPosition: [-101.22977709999999, 19.6453138],
      conflictos: [],
      loading: false,
      conflictos_geojson_url: "https://conflictossocioambientales.iies.unam.mx/conflictos/conflictos.geojson",
      conflictos_features: [],
      conflictos_selectedFeatures: [],
      conflictos_styles: {}
    }
  },
  watch: {
    mapHeight() {
      this.$refs["olmap"].remount()
    },
    mapaBase() {
      this.$refs["olmap"].remount()
    },
    conflictos_selectedFeatures() {
      if (this.conflictos_selectedFeatures.length > 0) {
        console.log("clic", this.conflictos_selectedFeatures)
        for (let feat of this.conflictos_selectedFeatures) {
          console.log("feat: ", feat)
          console.log("feat coordinates: ", feat.geometry.coordinates)
          console.log("this.clickCoords: ", this.clickCoords)
        }
        let collection = []
        for (let point of this.conflictos_selectedFeatures[0].geometry.coordinates) {
          console.log("point", point)
          collection.push(turf.point(point))
        }
        let featureCoords = turf.featureCollection(collection)
        let cercano = turf.nearestPoint(this.clickCoords, featureCoords)
        console.log("cercano: ", cercano)
      }
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'mapaBaseGetter', 'mapasBaseGetter', 'capasMapaGetter']),
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
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
    mapHeight() {
      let ribbon_height = 87
      if (this.showGISRibbon) ribbon_height = 180
      return this.$q.screen.height - ribbon_height + "px"
    }
  },
  methods: {
    clic(evt) {
      console.log("clic event", evt)
      this.clickCoords = evt.coordinate
    },
    pointsStyleFunc() {
      return (feature, resolution) => {
        let img_url = "https://conflictossocioambientales.iies.unam.mx" + feature.values_.tipo[2]
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
    for (let i of this.capasMapa) {
      console.log("capasMapa: ", i)
    }
  }
}
</script>

<style lang="scss">

</style>
