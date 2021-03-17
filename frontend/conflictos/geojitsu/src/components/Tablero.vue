<template>
  <div>
    <div class="row">
      <div class="col q-pr-md">
        <q-select style="width: 240px;" outlined name="estados" emit-value map-options multiple clearable
                  use-chips use-input option-label="entidadfederativa_nombre" option-value="id"
                  @filter="filterEstados" label="Estados" @input="estadosChange"
                  v-model="estadosOptionsSelected" :options="estadosOptionsFiltered"/>
      </div>
      <div class="col">
        <q-select style="width: 240px;" outlined name="municipios" emit-value map-options multiple clearable
                  use-chips use-input option-label="municipio_estado_nombre" option-value="id"
                  :readonly="!estadosOptionsSelected"
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
    estadosChange() {
      if (this.municipiosOptionsSelected) {
        if (this.municipiosOptionsSelected.length && this.estadosOptionsSelected) {
          axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/municipio-estado/?municipio_entidadfederativa__in=${this.estadosOptionsSelected.toString()}`).then(response => {
            this.municipiosOptions = response.data
            this.municipiosOptionsFiltered = response.data
            this.municipiosOptionsSelected = this.municipiosOptions
              .filter(municipio => {
                return this.municipiosOptionsSelected.includes(municipio.id)
              }).map(mun => mun.id)
          })
        } else {
          console.log("estados sin elementos")
          this.estadosOptionsSelected = null
          this.municipiosOptions = null
          this.municipiosOptionsFiltered = null
          this.municipiosOptionsSelected = null
        }
      }
      if (this.estadosOptionsSelected != null) {
        axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/municipio-estado/?municipio_entidadfederativa__in=${this.estadosOptionsSelected.toString()}`).then(response => {
          this.municipiosOptions = response.data
          this.municipiosOptionsFiltered = response.data
        })
      } else {
        this.estadosOptionsSelected = null
        this.municipiosOptionsSelected = null
        this.municipiosOptions = null
        this.municipiosOptionsFiltered = null
      }
    },
    municipiosChange() {
      console.log(this.municipiosOptionsSelected)
      if (this.municipiosOptionsSelected) {
        if (this.municipiosOptionsSelected.length === 0) {
          this.municipiosOptionsSelected = null
          console.log("null", this.municipiosOptionsSelected)
        }
      }
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
