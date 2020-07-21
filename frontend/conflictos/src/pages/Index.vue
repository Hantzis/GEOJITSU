<template>
  <q-page style="background-color: green; height: 100px">
    <div class="full-map">
      <vl-map ref="map" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
              data-projection="EPSG:4326" style="min-height: inherit; width: 100%; background-color: #75CFF0;">
        <vl-view ref="map_view" :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

        <!-- <vl-geoloc @update:position="geolocPosition = $event">
          <template slot-scope="geoloc">
            <vl-feature v-if="geoloc.position" id="position-feature">
              <vl-geom-point :coordinates="geoloc.position"></vl-geom-point>
              <vl-style-box>
                <vl-style-icon src="_media/marker.png" :scale="0.4" :anchor="[0.5, 1]"></vl-style-icon>
              </vl-style-box>
            </vl-feature>
          </template>
        </vl-geoloc> -->

        <!-- <vl-layer-tile id="osm">
          <vl-source-osm></vl-source-osm>
        </vl-layer-tile> -->
        <vl-layer-tile>
          <vl-source-xyz url="https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZXhhbXBsZXMiLCJhIjoiY2p0MG01MXRqMW45cjQzb2R6b2ptc3J4MSJ9.zA2W0IkI0c6KaAhJfk9bWg" attributions="Mapbox Outdoors v11" />
        </vl-layer-tile>
        <vl-layer-vector>
          <vl-source-vector :url="conflictos_geojson_url" :features.sync="conflictos_features" attributions="IIES-UNAM, Conflictos Socio-ambientales de México"/>
          <vl-style-func :factory="pointsStyleFunc" />
        </vl-layer-vector>

        <vl-interaction-select :features.sync="conflictos_selectedFeatures"></vl-interaction-select>
      </vl-map>
    </div>
  </q-page>
</template>

<script>
  import Vue from 'vue'
  import VueLayers from 'vuelayers'
  import 'vuelayers/lib/style.css' // needs css-loader
  import axios from 'axios'
  import IconStyle from 'vuelayers'
  Vue.use(VueLayers)

  export default {
    name: 'PageIndex',
    data () {
      return {
        zoom: 6,
        center: [-101.3, 23.9],
        center3857: [-11268847.24, 2231060.47],
        rotation: 0,
        geolocPosition: [-101.22977709999999, 19.6453138],
        conflictos_features: [],
        conflictos_selectedFeatures: [],
        conflictos_geojson_url: "https://conflictossocioambientales.iies.unam.mx/conflictos/conflictos.geojson",

      }
    },
    mounted() {
      console.log("mounted")
      axios.get("https://conflictossocioambientales.iies.unam.mx/conflictos/conflictos.geojson").then(response => {
        console.log("aqui")
        console.log(response.data )
        this.conflictos = response.data ;
      })
    },
    methods: {
      pointsStyleFunc() {
        let cache = {}
        console.log("puntostyle")

        return (feature, resolution) => {
          console.log(feature)
          console.log(resolution)
          const conflictos_styles = {
            '1': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/agri.2e16d0ba.fill-40x40.png"}),
            '2': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/bio.2e16d0ba.fill-40x40.png"}),
            /*'3': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/carre.2e16d0ba.fill-40x40.png"}),
            '4': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/energy_SL4BInB.2e16d0ba.fill-40x40.png"}),
            '5': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/forest.2e16d0ba.fill-40x40.png"}),
            '6': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/agua.2e16d0ba.fill-40x40.png"}),
            '7': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/Mineria.2e16d0ba.fill-40x40.png"}),
            '8': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/fish.2e16d0ba.fill-40x40_9Lu86JZ.png"}),
            '9': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/relleno.2e16d0ba.fill-40x40.png"}),
            '10': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/turismo.2e16d0ba.fill-40x40.png"}),
            '11': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/urbano.2e16d0ba.fill-40x40.png"}),
            '12': new IconStyle({src: "https://conflictossocioambientales.iies.unam.mx/media/images/Politico.2e16d0ba.fill-40x40.jpg"})*/
          }
          console.log("return styles")
          console.log(conflictos_styles);
          return conflictos_styles
        }
      }
    },
    watch: {
      conflictos_selectedFeatures() {
        console.log(this.conflictos_selectedFeatures[0])
      }
    }
  }
</script>

<style lang="scss">
.full-map {
  min-height: inherit;
  height: 100%;
}
</style>
