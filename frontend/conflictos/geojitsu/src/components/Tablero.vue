<template>
  <div>

    <q-tabs
      v-model="tab"
      indicator-color="primary"
      align="left"
      :breakpoint="0"
      no-caps
      inline-label
    >
      <q-tab name="graficas" icon="mdi-chart-pie" label="Gráficas"/>
      <q-tab name="filtros" icon="mdi-filter" label="Filtros"/>
    </q-tabs>

    <q-tab-panels v-model="tab" class="shadow-2 rounded-borders">
      <q-tab-panel name="graficas">
        <div class="text-h6">Graficas</div>
        Lorem ipsum dolor sit amet consectetur adipisicing elit.
      </q-tab-panel>

      <q-tab-panel name="filtros">
        <div class="text-h6">Filtros</div>

        <div class="row full-width">
          <div class="col-sm-6 col-xs-12 q-pa-sm">
            <q-select class="full-width" outlined name="estados" emit-value map-options multiple clearable
                      use-chips use-input option-label="entidadfederativa_nombre" option-value="id"
                      @filter="filterEstados" label="Estados" @input="estadosChange"
                      v-model="estadosOptionsSelected" :options="estadosOptionsFiltered"/>
          </div>
          <div class="col-sm-6 col-xs-12 q-pa-sm">
            <q-select class="full-width" outlined name="municipios" emit-value map-options multiple clearable
                      use-chips use-input option-label="municipio_estado_nombre" option-value="id"
                      :readonly="!estadosOptionsSelected"
                      @filter="filterMunicipios" label="Municipios" @input="municipiosChange"
                      v-model="municipiosOptionsSelected" :options="municipiosOptionsFiltered"/>
          </div>
        </div>
        <div class="row full-width">
          <div class="col-sm-6 col-xs-12 q-pa-sm">
            <q-select class="full-width" outlined name="organizaciones" emit-value map-options multiple clearable
                      use-chips use-input option-label="organizacion_nombre" option-value="id"
                      @filter="filterOrganizaciones" label="Organizaciones"
                      v-model="organizacionesOptionsSelected" :options="organizacionesOptionsFiltered"/>
          </div>
          <div class="col-sm-6 col-xs-12 q-pa-sm">
            <q-select class="full-width" outlined name="empresas" emit-value map-options multiple clearable
                      use-chips use-input option-label="empresa_nombre" option-value="id"
                      @filter="filterEmpresas" label="Empresas"
                      v-model="empresasOptionsSelected" :options="empresasOptionsFiltered"/>
          </div>
        </div>
        <div class="row full-width">
          <div class="col-sm-6 col-xs-12 q-pa-sm">
            <q-select class="full-width" outlined name="secretarias" emit-value map-options multiple clearable
                      use-chips use-input option-label="secretaria_nombre" option-value="id"
                      @filter="filterSecretarias" label="Secretarías"
                      v-model="secretariasOptionsSelected" :options="secretariasOptionsFiltered"/>
          </div>
          <div class="col-sm-6 col-xs-12 q-pa-sm">
            <q-select class="full-width" outlined name="pueblos" emit-value map-options multiple clearable
                      use-chips use-input option-label="pueblo_nombre" option-value="id"
                      @filter="filterPueblos" label="Pueblos originarios"
                      v-model="pueblosOptionsSelected" :options="pueblosOptionsFiltered"/>
          </div>
        </div>

        <div class="row q-pa-sm">
          <q-space/>
          <q-btn label="Limpiar filtros" color="grey-6" style="margin-right: 12px;"></q-btn>
          <q-btn label="Filtrar" color="green"></q-btn>
        </div>

      </q-tab-panel>
    </q-tab-panels>


  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Tablero",
  components: {},
  data() {
    return {
      tab: 'graficas',
      estadosFilter: '',
      estadosOptions: [],
      estadosOptionsFiltered: [],
      estadosOptionsSelected: null,
      municipiosFilter: '',
      municipiosOptions: [],
      municipiosOptionsFiltered: [],
      municipiosOptionsSelected: null,
      organizacionesFilter: '',
      organizacionesOptions: [],
      organizacionesOptionsFiltered: [],
      organizacionesOptionsSelected: null,
      empresasFilter: '',
      empresasOptions: [],
      empresasOptionsFiltered: [],
      empresasOptionsSelected: null,
      secretariasFilter: '',
      secretariasOptions: [],
      secretariasOptionsFiltered: [],
      secretariasOptionsSelected: null,
      pueblosFilter: '',
      pueblosOptions: [],
      pueblosOptionsFiltered: [],
      pueblosOptionsSelected: null,
    }
  },
  methods: {
    estadosChange() {
      if (this.municipiosOptionsSelected && this.estadosOptionsSelected) {
        if (this.municipiosOptionsSelected.length && this.estadosOptionsSelected.length) {
          axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/municipio-estado/?municipio_entidadfederativa__in=${this.estadosOptionsSelected.toString()}`).then(response => {
            this.municipiosOptions = response.data
            this.municipiosOptionsFiltered = response.data
            this.municipiosOptionsSelected = this.municipiosOptions
              .filter(municipio => {
                return this.municipiosOptionsSelected.includes(municipio.id)
              }).map(mun => mun.id)
          })
        } else {
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
    filterOrganizaciones(val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.organizacionesOptionsFiltered = this.organizacionesOptions.filter(v => v.organizacion_nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase().indexOf(needle) > -1)
      })
    },
    filterEmpresas(val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.empresasOptionsFiltered = this.empresasOptions.filter(v => v.empresa_nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase().indexOf(needle) > -1)
      })
    },
    filterSecretarias(val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.secretariasOptionsFiltered = this.secretariasOptions.filter(v => v.secretaria_nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase().indexOf(needle) > -1)
      })
    },
    filterPueblos(val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.pueblosOptionsFiltered = this.pueblosOptions.filter(v => v.pueblo_nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase().indexOf(needle) > -1)
      })
    },
  },
  watch: {
    estadosOptionsSelected() {
      if (this.estadosOptionsSelected) {
        if (this.estadosOptionsSelected.length === 0) {
          this.estadosOptionsSelected = null
          this.municipiosOptions = null
          this.municipiosOptionsFiltered = null
          this.municipiosOptionsSelected = null
        }
      }
    }
  },
  created() {
    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/entidad-federativa/')
      .then(response => {
        this.estadosOptions = response.data
        this.estadosOptionsFiltered = response.data
      })
    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/organizacion/')
      .then(response => {
        this.organizacionesOptions = response.data
        this.organizacionesOptionsFiltered = response.data
      })
    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/empresa/')
      .then(response => {
        this.empresasOptions = response.data
        this.empresasOptionsFiltered = response.data
      })
    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/secretaria/')
      .then(response => {
        this.secretariasOptions = response.data
        this.secretariasOptionsFiltered = response.data
      })
    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/pueblo/')
      .then(response => {
        this.pueblosOptions = response.data
        this.pueblosOptionsFiltered = response.data
      })

  },
  mounted() {

  }
}
</script>

<style scoped>

</style>
