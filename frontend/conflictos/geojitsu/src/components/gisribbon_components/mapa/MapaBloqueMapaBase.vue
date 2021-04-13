<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs">
          <q-select style="min-width: 255px;" outlined name="base" label="Mapa base" :options="mapasBase" v-model="mapaBase"
                    emit-value map-options>
            <template v-slot:prepend>
              <q-icon name="mdi-layers-outline"/>
            </template>
          </q-select>
        </div>
      </div>
    </div>
    <div class="row justify-between">
      <div class="col-auto">
        <div class="row q-px-sm"/>
      </div>
      <div class="col-auto">
        Mapa base
      </div>
      <div class="col-auto">
        <div class="col-auto">
          <div class="row q-px-sm"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

export default {
  name: "MapaBloqueCapas",
  data() {
    return {
      bloqueIsEnabled: false,
    }
  },
  watch: {
    mapaBase() {
      console.log(this.mapaBase)
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['mapasBaseGetter', 'mapaBaseGetter']),
    mapasBase: {
      get() {
        return this.mapasBaseGetter
      }
    },
    mapaBase: {
      get() {
        return this.mapaBaseGetter
      },
      set(value) {
        this.mapaBaseAction(value)
      }
    },
  },
  methods: {
    ...mapActions('geojitsu', ['mapaBaseAction']),
  }
}
</script>
