<template>
  <q-page style="background-color: #90caea;">
    <div class="full-map">
      <vl-map ref="map" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
              data-projection="EPSG:4326" style="min-height: inherit; width: 100%;">
        <vl-view ref="map_view" :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

        <vl-geoloc @update:position="geolocPosition = $event">
          <template slot-scope="geoloc">
            <vl-feature v-if="geoloc.position" id="position-feature">
              <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
              <vl-style-box>
                <vl-style-icon src="_media/marker.png" :scale="0.4" :anchor="[0.5, 1]"></vl-style-icon>
              </vl-style-box>
            </vl-feature>
          </template>
        </vl-geoloc>

        <vl-layer-tile id="osm">
          <vl-source-osm></vl-source-osm>
        </vl-layer-tile>
        <vl-layer-tile>
          <vl-source-xyz url="https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZXhhbXBsZXMiLCJhIjoiY2p0MG01MXRqMW45cjQzb2R6b2ptc3J4MSJ9.zA2W0IkI0c6KaAhJfk9bWg" attributions="string or array" />
        </vl-layer-tile>
      </vl-map>
    </div>
  </q-page>
</template>

<script>
  import Vue from 'vue'
  import VueLayers from 'vuelayers'
  import 'vuelayers/lib/style.css' // needs css-loader
  Vue.use(VueLayers)


  export default {
    name: 'PageIndex',
    data () {
      return {
        zoom: 12,
        center: [-101.22977709999999, 19.6453138],
        rotation: 0,
        geolocPosition: [-101.22977709999999, 19.6453138],
      }
    }
  }
</script>

<style lang="scss">
.full-map {
  min-height: inherit;
  /* background-color: green; */
  margin-bottom: -6px;
}
.ol-attribution.ol-uncollapsible {
  bottom: 6px;
  height: initial;
}
</style>
