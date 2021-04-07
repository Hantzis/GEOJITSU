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
      <q-tab name="datos" icon="mdi-table" label="Datos"/>
      <q-tab name="filtros" icon="mdi-filter" label="Filtros"/>
    </q-tabs>

    <q-tab-panels v-model="tab" class="shadow-2 rounded-borders">
      <q-tab-panel name="graficas">
        <div class="text-h6">Graficas</div>
        <div v-if="Object.entries(datosGraficas).length > 0" class="row justify-between content-center">
          <conflictos-pie-chart v-if="datosGraficas.tipos.length" :title="'Tipo'" :dataGrafica="datosGraficas.tipos"/>
          <conflictos-pie-chart v-if="datosGraficas.estados.length" :title="'Estados'" :dataGrafica="datosGraficas.estados"/>
          <conflictos-pie-chart v-if="datosGraficas.municipios.length"  :title="'Municipios'" :dataGrafica="datosGraficas.municipios"/>
          <conflictos-pie-chart v-if="datosGraficas.organizaciones.length"  :title="'Organizaciones'" :dataGrafica="datosGraficas.organizaciones"/>
          <conflictos-pie-chart v-if="datosGraficas.empresas.length"  :title="'Empresas'" :dataGrafica="datosGraficas.empresas"/>
          <conflictos-pie-chart v-if="datosGraficas.secretarias.length"  :title="'Secretarías'" :dataGrafica="datosGraficas.secretarias"/>
          <conflictos-pie-chart v-if="datosGraficas.pueblos.length"  :title="'Pueblos originarios'" :dataGrafica="datosGraficas.pueblos"/>
        </div>

        <div v-if="datosGraficas.length < 1" class="row justify-between content-center">
          <p>cargando info</p>
        </div>


      </q-tab-panel>

      <q-tab-panel name="datos">
        <div class="text-h6 q-pb-sm">Datos</div>
        <q-table
          title="Treats"
          :data="datosTabla"
          :columns="tablaColumnas"
          row-key="name"
          :visible-columns="visibleColumns"
          :rows-per-page-label="'Registros por página'"
          :filter="filterTabla"
        >
          <template v-slot:top>

            <q-space/>

            <q-input class="q-pr-md" outlined dense debounce="300" v-model="filterTabla" placeholder="Buscar">
              <template v-slot:append>
                <q-icon name="buscar"/>
              </template>
            </q-input>

            <q-select
              v-model="visibleColumns"
              multiple
              outlined
              dense
              options-dense
              :display-value="$q.lang.table.columns"
              emit-value
              map-options
              :options="tablaColumnas"
              option-value="name"
              options-cover
              style="min-width: 150px"
            />
          </template>

        </q-table>
      </q-tab-panel>

      <q-tab-panel name="filtros">
        <div class="text-h6">Filtros</div>

        <div class="row full-width">
          <div class="col-12 q-pa-sm">
            <q-select class="full-width" outlined name="tipo" emit-value map-options multiple clearable
                      use-chips use-input option-label="conflictotipo_nombre" option-value="id"
                      @filter="filterTipos" label="Tipos"
                      v-model="tiposOptionsSelected" :options="tiposOptionsFiltered"/>
          </div>
        </div>
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
          <q-btn label="Limpiar filtros" color="grey-6" style="margin-right: 12px;"
                 @click.stop="limpiarFiltros"></q-btn>
          <q-btn label="Filtrar" color="green" @click.stop="filtrarDatos"></q-btn>
        </div>

      </q-tab-panel>
    </q-tab-panels>

    <q-ajax-bar
      ref="bar"
      position="top"
      color="primary"
      size="4px"
      skip-hijack
    />
  </div>
</template>

<script>
import axios from 'axios'
import ConflictosPieChart from "components/ConflictosPieChart";

export default {
  name: "Tablero",
  components: {
    ConflictosPieChart
  },
  data() {
    return {

      tab: 'graficas',
      tiposFilter: '',
      tiposOptions: [],
      tiposOptionsFiltered: [],
      tiposOptionsSelected: null,
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
      datosTabla: [],
      datosTablaTodos: [],
      datosGraficas: {},
      datosGraficasTodos: [],
      filterTabla: '',
      visibleColumns: ['tipo_conflicto', 'estados_nombre_texto',
        'secretarias_nombre_texto',
        'pueblos_originarios_nombre_texto'],
      tablaColumnas: [
        {name: 'tipo_conflicto', align: 'left', label: 'Típo de conflicto', field: 'tipo_conflicto', sortable: true},
        {name: 'estados_nombre_texto', align: 'left', label: 'Estados', field: 'estados_nombre_texto', sortable: true},
        {
          name: 'municipios_estado_nombre_texto',
          align: 'left',
          label: 'Municipios',
          field: 'municipios_estado_nombre_texto',
          sortable: true
        },
        {
          name: 'organizaciones_nombre_texto',
          align: 'left',
          label: 'Organizaciones',
          field: 'organizaciones_nombre_texto',
          sortable: true
        },
        {
          name: 'empresas_nombre_texto',
          align: 'left',
          label: 'Empresas',
          field: 'empresas_nombre_texto',
          sortable: true
        },
        {
          name: 'secretarias_nombre_texto',
          align: 'left',
          label: 'Secretarías',
          field: 'secretarias_nombre_texto',
          sortable: true
        },
        {
          name: 'pueblos_originarios_nombre_texto',
          align: 'left',
          label: 'Pueblos originarios',
          field: 'pueblos_originarios_nombre_texto',
          sortable: true
        },
        {
          name: 'publicaciones_lista',
          align: 'left',
          label: 'Publicaciones',
          field: row => row.publicaciones_lista.url,
          sortable: true
        },
      ],
      loadingBar: undefined,
      source: undefined,
      CancelToken: undefined,
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
      if (this.municipiosOptionsSelected) {
        if (this.municipiosOptionsSelected.length === 0) {
          this.municipiosOptionsSelected = null
        }
      }
    },
    limpiarFiltros() {
      this.tiposOptionsSelected = null
      this.estadosOptionsSelected = null
      this.municipiosOptionsSelected = null
      this.organizacionesOptionsSelected = null
      this.empresasOptionsSelected = null
      this.secretariasOptionsSelected = null
      this.pueblosOptionsSelected = null
    },
    filtrarDatos() {
      const filtros = []
      if (Array.isArray(this.tiposOptionsSelected)) {
        if (this.tiposOptionsSelected.length > 0)
          filtros.push("tipo__in=" + this.tiposOptionsSelected)
      }
      if (Array.isArray(this.estadosOptionsSelected)) {
        if (this.estadosOptionsSelected.length > 0)
          filtros.push("estados__in=" + this.estadosOptionsSelected)
      }
      if (Array.isArray(this.municipiosOptionsSelected)) {
        if (this.municipiosOptionsSelected.length > 0)
          filtros.push("municipios__in=" + this.municipiosOptionsSelected)
      }
      if (Array.isArray(this.organizacionesOptionsSelected)) {
        if (this.organizacionesOptionsSelected.length > 0)
          filtros.push("organizaciones__in=" + this.organizacionesOptionsSelected)
      }
      if (Array.isArray(this.empresasOptionsSelected)) {
        if (this.empresasOptionsSelected.length > 0)
          filtros.push("empresas__in=" + this.empresasOptionsSelected)
      }
      if (Array.isArray(this.secretariasOptionsSelected)) {
        if (this.secretariasOptionsSelected.length > 0)
          filtros.push("secretarias__in=" + this.secretariasOptionsSelected)
      }
      if (Array.isArray(this.pueblosOptionsSelected)) {
        if (this.pueblosOptionsSelected.length > 0)
          filtros.push("pueblos__in=" + this.pueblosOptionsSelected)
      }
      this.datosGraficas = {}
      let query = "?" + filtros.join("&")
      if (query === "?" || query === "") {
        this.loadingBar.start()
        this.datosGraficas = this.datosGraficasTodos
        this.datosTabla = this.datosTablaTodos
        this.loadingBar.stop()
      } else {
        this.loadingBar.start()
        this.CancelToken.cancel("Nuevo filtro");
        axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/datos-graficas/${query}`,
        ).then(response => {
          this.datosGraficas = response.data
        }).then(() => {
        }).catch(error => {
          this.loadingBar.stop()
        })
        axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/datos-tabla/${query}`,
        ).then(response => {
          this.datosTabla = response.data
          this.tab = 'graficas'
          this.loadingBar.stop()
        }).catch(error => {
          this.loadingBar.stop()
        })
      }
    },
    filterTipos(val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.tiposOptionsFiltered = this.tiposOptions.filter(v => v.conflictotipo_nombre.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase().indexOf(needle) > -1)
      })
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
    },
  },
  mounted() {
    this.loadingBar = this.$refs.bar
    this.loadingBar.start()
    this.CancelToken = axios.CancelToken.source();
    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/datos-tabla/',
      {cancelToken: this.CancelToken.token}).then(response => {
      this.datosTabla = response.data
      this.datosTablaTodos = response.data
    }).then(() => {
      axios.get(`https://conflictossocioambientales.iies.unam.mx/back/api/v1/datos-graficas/`,
        {cancelToken: this.CancelToken.token}).then(response => {
        this.datosGraficas = response.data
        this.datosGraficasTodos = response.data
      })
    }).then(() => {
      this.loadingBar.stop()
    }).catch(() => {
      this.loadingBar.stop()
    })


    axios.get('https://conflictossocioambientales.iies.unam.mx/back/api/v1/conflicto-tipo/')
      .then(response => {
        this.tiposOptions = response.data
        this.tiposOptionsFiltered = response.data
      })
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
}
</script>

<style scoped>
</style>
