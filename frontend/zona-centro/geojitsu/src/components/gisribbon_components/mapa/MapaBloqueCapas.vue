<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs" style="padding-bottom: 12px;">
          <q-select outlined name="archivo" label="Capa seleccionada" :options="capasMapa" v-model="capaSeleccionada" emit-value
                    map-options>
            <template v-slot:prepend>
              <q-icon name="mdi-layers-triple"/>
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
        Capas
      </div>
      <div class="col-auto">
        <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right" @click="drawerCapas = !drawerCapas"
               style="border-radius: 0; margin-bottom: 0; margin-right: 1px;"/>
      </div>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: "MapaBloqueCapas",
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['capasMapaGetter', 'capaSeleccionadaGetter', 'getDrawerCapas']),
    capasMapa: {
      get() {
        return this.capasMapaGetter
      }
    },
    capaSeleccionada: {
      get() {
        return this.capaSeleccionadaGetter
      },
      set(value) {
        this.capaSeleccionadaAction(value)
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
    ...mapActions('geojitsu', ['capaSeleccionadaAction', 'setDrawerCapas']),
  },
}
</script>
