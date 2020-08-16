<template>
  <q-page>
        <div class="row">
          <div class="col">
            <GISRibbon />
          </div>
        </div>
        <div class="row">
            <div class="col" :style="{'min-height': mapHeight}">
              <vl-map ref="olmap" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
                      data-projection="EPSG:4326" style="min-height: inherit; max-height: 1px; width: 100%; background-color: #75CFF0;">
                <vl-view ref="map_view" :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

                <vl-geoloc @update:position="geolocPosition = $event">
                  <template slot-scope="geoloc">
                    <vl-feature v-if="geoloc.position" id="position-feature">
                      <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
                      <vl-style-box>
                        <vl-style-icon src="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png" :scale="0.1" :anchor="[0.5, 1]"></vl-style-icon>
                      </vl-style-box>
                    </vl-feature>
                  </template>
                </vl-geoloc>
                <vl-layer-tile>
                  <vl-source-xyz
                    url="https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibml6aGlzYWViYSIsImEiOiJjanZwZXNpeWYwZDcxNDlwOXVhejg1Yno3In0.kqEaQSkVaFMpKKtx0FyNRA"
                    attributions="Mapbox"/>
                </vl-layer-tile>
              </vl-map>
            </div>
          </div>

  </q-page>

</template>

<script>
import {mapGetters} from 'vuex'

import Vue from 'vue'
import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'
import GISRibbon from "components/GISRibbon"; // needs css-loader
Vue.use(VueLayers)

export default {
  name: 'PageIndex',
  components: {GISRibbon},
  data() {
    return {
      zoom: 12,
      center: [-101.22977709999999, 19.6453138],
      center3857: [-11268847.24, 2231060.47],
      rotation: 0,
      geolocPosition: [-101.22977709999999, 19.6453138],
    }
  },
  watch: {
    mapHeight() {
      this.$refs["olmap"].remount()
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter']),
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      }
    },
    mapHeight() {
      let ribbon_height = 87
      if (this.showGISRibbon) ribbon_height = 180
      return this.$q.screen.height - ribbon_height + "px"
    }
  },
}
</script>

<style lang="scss">

</style>
