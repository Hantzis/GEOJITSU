<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs" style="padding-bottom: 0px;">
          <q-select outlined name="base" label="Mapa base" :options="mapasBase" v-model="mapaBase"
                    emit-value map-options>
            <template v-slot:prepend>
              <q-icon name="mdi-layers-outline"/>
            </template>
          </q-select>
        </div>
      </div>
    </div>
    <div class="row justify-between items-end">
      <div class="col-auto">
        <div class="row q-px-sm"/>
      </div>
      <div class="col-auto" style="margin-bottom: 3px;">
        <span>&nbsp;&nbsp;</span>Capas y simbología
      </div>
      <div class="col-auto" >
        <q-btn dense size="md" flat icon="mdi-arrow-bottom-right" @click="drawerCapas = !drawerCapas"
               style="border-radius: 0; margin-bottom: 0; margin-right: 1px;"/>
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
  computed: {
    ...mapGetters('geojitsu', ['mapasBaseGetter', 'mapaBaseGetter', 'getDrawerCapas']),
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
    drawerCapas: {
      get() {
        return this.getDrawerCapas
      },
      set(value) {
        this.setDrawerCapas(value)
      }
    },
  },
  methods: {
    ...mapActions('geojitsu', ['mapaBaseAction', 'setDrawerCapas']),
  }
}
</script>
