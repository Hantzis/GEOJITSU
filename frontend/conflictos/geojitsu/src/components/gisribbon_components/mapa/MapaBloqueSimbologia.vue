<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs">
          <q-select outlined name="simbologia" label="Simbología" :options="simbologias" v-model="simbologiaTipo">
            <template v-slot:prepend>
              <q-icon name="mdi-map-marker"/>
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
        Simbología
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
  name: "MapaBloqueSimbologia",
  data() {
    return {
      simbologias: ['Tipo', 'Organizaciones', 'Empresas'],
    }
  },
  computed: {
    ...mapGetters('geojitsu', ['getSimbologiaTipo']),
    simbologiaTipo: {
      get() {
        return this.getSimbologiaTipo
      },
      set(value) {
        this.setSimbologiaTipo(value)
      }
    },
  },
  methods: {
    ...mapActions('geojitsu', ['setSimbologiaTipo']),
  }
}
</script>
