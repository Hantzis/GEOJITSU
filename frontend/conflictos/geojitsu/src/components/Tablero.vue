<template>
  <div>
    <div class="row">
      <div class="col q-pr-md">
        <q-select style="width: 240px;" outlined name="estados" emit-value map-options multiple clearable
                  use-chips use-input option-label="entidadfederativa_nombre" option-value="id"
                  @filter="filterEstados" label="Estados" @input="estadosChange($event)"
                  v-model="estadosOptionsSelected" :options="estadosOptionsFiltered"/>
      </div>
      <div class="col">
        <q-select style="width: 240px;" outlined name="municipios" emit-value map-options multiple clearable
                  use-chips use-input option-label="municipio_estado_nombre" option-value="id" :readonly="!estadosOptionsSelected"
                  @filter="filterMunicipios" label="Municipios" @input="municipiosChange"
                  v-model="municipiosOptionsSelected" :options="municipiosOptionsFiltered"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Tablero",
  components: {},
  data() {
    return {
      estadosFilter: '',
      estadosOptions: [],
      estadosOptionsFiltered: [],
      estadosOptionsSelected: null,
      municipiosFilter: '',
      municipiosOptions: [],
      municipiosOptionsFiltered: [],
      municipiosOptionsSelected: null,
    }
  },
  methods: {
    estadosChange(evt) {
      console.log(evt)
      console.log(this.estadosOptionsSelected)
      axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/municipio-estado/').then(response => {
      console.log("municipios", response)
      this.municipiosOptions = response.data
      this.municipiosOptionsFiltered = response.data
    })
    },
    municipiosChange() {
      console.log(this.municipiosOptionsSelected)
    },
    filterEstados(val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.estadosOptionsFiltered = this.estadosOptions.filter(v => v.entidadfederativa_nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase().indexOf(needle) > -1)
      })
    },
    filterMunicipios(val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.municipiosOptionsFiltered = this.municipiosOptions.filter(v => v.municipio_estado_nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase().indexOf(needle) > -1)
      })
    },
  },
  created() {
    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/entidad-federativa/').then(response => {
      console.log("estados", response)
      this.estadosOptions = response.data
      this.estadosOptionsFiltered = response.data
    })
  },
  mounted() {

  }
}
</script>

<style scoped>

</style>
