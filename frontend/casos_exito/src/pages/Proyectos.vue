<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Proyectos" icon="mdi-chart-timeline"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" @click="getProyectos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn no-caps v-if="auth_logged" style="margin-left: 8px;" color="green" @click="add_proyecto_dialog = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div style="margin-top: 2px;">Agregar Proyecto</div>
        </q-btn>
      </div>
    </div>

    <q-card square>
      <q-tabs
        v-model="tab"
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="left"
        no-caps
      >
        <q-tab name="todos" label="Todos los proyectos"/>
        <q-tab v-if="auth_logged" name="mios" label="Proyectos registrados por mí"/>
      </q-tabs>

      <q-separator/>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="todos">
          <div class="row">
            <div class="col">
              <q-table
                title="Todos los proyectos"
                :data.sync="datos_proyectos"
                :columns="columnas"
                :visible-columns="visible_columns"
                row-key="id"
                :loading="tabla_loading"
                :filter="filter"
                square
              >
                <template v-slot:top-right>
                  <q-input borderless dense debounce="300" v-model="filter" placeholder="Buscar"
                           style="margin-right: 12px;">
                    <template v-slot:append>
                      <q-icon name="search"/>
                    </template>
                  </q-input>
                  <q-select
                    v-model="visible_columns"
                    multiple
                    outlined
                    dense
                    options-dense
                    :display-value1="$q.lang.table.columnas"
                    display-value="Mostrar columnas..."
                    emit-value
                    map-options
                    :options="columnas"
                    option-value="name"
                    options-cover
                    style="min-width: 150px"
                  />
                </template>

                <template v-slot:header="props">
                  <q-tr :props="props">
                    <q-th
                      v-for="col in props.cols"
                      :key="col.name"
                      :props="props"
                    >
                      {{ col.label }}
                    </q-th>
                    <q-th auto-width/>
                  </q-tr>
                </template>

                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td v-for="col in props.cols" :key="col.name" :props="props">{{ col.value }}</q-td>
                    <q-td auto-width>
                      <q-btn dense round flat color="primary"
                             icon="mdi-eye"></q-btn>
                      <q-btn v-if="auth_logged" dense round flat color="primary" @click="editRegistroDialog(props)"
                             icon="edit"></q-btn>
                      <q-btn v-if="auth_logged" dense round flat color="red" @click="deleteRegistroDialog(props)"
                             icon="delete"></q-btn>
                    </q-td>
                  </q-tr>
                </template>

              </q-table>
            </div>
          </div>
        </q-tab-panel>

        <q-tab-panel v-if="auth_logged" name="mios">
          <div class="row">
            <div class="col">
              <q-table
                title="Proyectos registrados por mí"
                :data.sync="datos_proyectos_mios"
                :columns="columnas"
                :visible-columns="visible_columns"
                row-key="id"
                :loading="tabla_loading"
                :filter="filter"
                square
              >
                <template v-slot:top-right>
                  <q-input borderless dense debounce="300" v-model="filter" placeholder="Buscar"
                           style="margin-right: 12px;">
                    <template v-slot:append>
                      <q-icon name="search"/>
                    </template>
                  </q-input>
                  <q-select
                    v-model="visible_columns"
                    multiple
                    outlined
                    dense
                    options-dense
                    :display-value1="$q.lang.table.columnas"
                    display-value="Mostrar columnas..."
                    emit-value
                    map-options
                    :options="columnas"
                    option-value="name"
                    options-cover
                    style="min-width: 150px"
                  />
                </template>

                <template v-slot:header="props">
                  <q-tr :props="props">
                    <q-th
                      v-for="col in props.cols"
                      :key="col.name"
                      :props="props"
                    >
                      {{ col.label }}
                    </q-th>
                    <q-th auto-width/>
                  </q-tr>
                </template>

                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td v-for="col in props.cols" :key="col.name" :props="props">{{ col.value }}</q-td>
                    <q-td auto-width>
                      <q-btn dense round disable flat color="accent"
                             :icon="props.expand ? 'edit' : 'add'"></q-btn>
                      <q-btn v-if="auth_logged" dense round flat color="primary" @click="editRegistroDialog(props)"
                             icon="edit"></q-btn>
                      <q-btn v-if="auth_logged" dense round flat color="red" @click="deleteRegistroDialog(props)"
                             icon="delete"></q-btn>
                    </q-td>
                  </q-tr>
                </template>

              </q-table>
            </div>
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>

    <q-dialog ref="add_proyecto_dialog" full-width full-height v-model="add_proyecto_dialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-user" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar proyecto</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 79vh" class="scroll">
          <div class="row q-py-xs">
            <q-input outlined class="full-width" name="username" v-model="proyecto_data.nombre_proyecto"
                     :rules="[val => !!val || 'Nombre del proyecto']"
                     label="Nombre del proyecto"/>
          </div>
          <div class="row q-py-xs">
            <div class="col-3 q-pr-md">
              <q-input outlined class="full-width" name="nombre_corto" v-model="proyecto_data.nombre_corto"
                       :rules="[val => !!val || 'Nombre corto obligatorio']"
                       label="Nombre corto (del proyecto)"/>
            </div>
            <div class="col-3 q-pr-md">
              <q-input outlined name="fecha_inicio" v-model="proyecto_data.fecha_inicio"
                       :rules="['date']"
                       label="Fecha de inicio">
                <template v-slot:default >
                    <q-popup-proxy  ref="fecha_inicio" transition-show="scale" mask="date" transition-hide="scale">
                      <q-date v-model="proyecto_data.fecha_inicio">
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Cerrar" color="primary" flat/>
                        </div>
                      </q-date>
                    </q-popup-proxy>
                </template>
                <template v-slot:append>
                  <q-icon name="event">
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-3 q-pr-md">
              <q-input outlined class="full-width" name="fecha_registro" v-model="proyecto_data.fecha_registro"
                       :rules="['date']"
                       label="Fecha de registro a ONSSES">
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy ref="qDateProxy" transition-show="scale" mask="date" transition-hide="scale">
                      <q-date v-model="proyecto_data.fecha_registro">
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Cerrar" color="primary" flat/>
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-3">
              <q-select
                name="etapa"
                label="Etapa"
                outlined
                v-model="proyecto_data.etapa"
                :options="['Inicial', 'Intermedio', 'Consolidado']"
                :rules="[val => !!val || 'Género obligatorio']"
              />
            </div>
          </div>


        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col-auto q-pr-xs">
              <q-btn @click="updateProfile()" color="grey-7"
                     label="Cancelar" no-caps class=""/>
            </div>
            <div class="col-auto q-pl-xs">
              <q-btn @click="updateProfile()" color="green"
                     label="Guardar" no-caps class=""/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script>
import axios from 'axios'
import cookies from 'browser-cookies'
import {mapGetters, mapActions} from 'vuex'

export default {
  name: 'casosExito',
  data() {
    return {
      filter: '',
      add_proyecto_dialog: false,
      proyecto_data: {},
      datos_proyectos: undefined,
      datos_proyectos_mios: undefined,
      tabla_loading: true,
      tab: 'todos',
      columnas: [
        {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true},
        {name: 'nombre_proyecto', align: 'left', label: 'Nombre de proyecto', field: 'nombre_proyecto', sortable: true},
        {name: 'nombre_corto', align: 'left', label: 'Nombre corto', field: 'nombre_corto', sortable: true},
        {name: 'fecha_inicio', align: 'left', label: 'Fecha de inicio', field: 'fecha_inicio', sortable: true},
        {name: 'fecha_registro', align: 'left', label: 'Fecha de registro', field: 'fecha_registro', sortable: true},
        {name: 'etapa_display', align: 'left', label: 'Etapa', field: 'etapa_display', sortable: true},
        {name: 'escala_display', align: 'left', label: 'Escala', field: 'escala_display', sortable: true},
        {name: 'domicilio_display', align: 'left', label: 'Domicilio', field: 'domicilio_display', sortable: true},
        {name: 'municipio_display', align: 'left', label: 'Municipio', field: 'municipio_display', sortable: true},
        {name: 'estado_display', align: 'left', label: 'Estado', field: 'estado_display', sortable: true},
        {name: 'telefono', align: 'left', label: 'Teléfono', field: 'telefono', sortable: true},
        {name: 'email', align: 'left', label: 'e-mail', field: 'email', sortable: true},
        {name: 'representante', align: 'left', label: 'Representante', field: 'representante', sortable: true},
        {name: 'url', align: 'left', label: 'URL', field: 'url', sortable: true},
        {
          name: 'tipo_organizacion_display',
          align: 'left',
          label: 'Tipo de organizacion',
          field: 'tipo_organizacion_display',
          sortable: true
        },
        {
          name: 'grupo_etnico_display',
          align: 'left',
          label: 'Grupo étnico',
          field: 'grupo_etnico_display',
          sortable: true
        },
        {name: 'numero_hombres', align: 'left', label: 'Número de hombres', field: 'numero_hombres', sortable: true},
        {name: 'numero_mujeres', align: 'left', label: 'Número de mujeres', field: 'numero_mujeres', sortable: true},
        {
          name: 'inclusion_genero_display',
          align: 'left',
          label: 'Inclusión de género',
          field: 'inclusion_genero_display',
          sortable: true
        },
        {
          name: 'actividad_principal_display',
          align: 'left',
          label: 'Actividad económica principal',
          field: 'actividad_principal_display',
          sortable: true
        },
        {
          name: 'actividad_secundaria_display',
          align: 'left',
          label: 'Actividad económica secundaria',
          field: 'actividad_secundaria_display',
          sortable: true
        },
        {
          name: 'actividad_otra_display',
          align: 'left',
          label: 'Otra actividad económica',
          field: 'actividad_otra_display',
          sortable: true
        },
        {name: 'promovente_display', align: 'left', label: 'Promovente', field: 'promovente_display', sortable: true},

      ],
      visible_columns: ['id', 'nombre_proyecto', 'fecha_inicio', 'etapa_display', 'escala_display', 'actividad_principal_display', 'representante'],
    }
  },
  computed: {
    ...mapGetters('base', ['getUserData']),
    ...mapGetters('auth', ['logged', 'user']),
    auth_user: {
      get() {

        return this.user
      }
    },
    auth_logged: {
      get() {
        console.log("auth_user", this.user)
        return this.logged
      }
    }
  },
  methods: {
    getProyectos() {
      const token = cookies.get("access_token")
      axios.get("https://onsses45.maptitude.xyz/api/v1/ce/proyectos/").then(response => {
        console.log("response: ", response.data)
        this.datos_proyectos = response.data
      }).then(() => {

        if (token) {
          axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/proyectos/?promovente=${this.auth_user.pk}`,
            {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
            this.datos_proyectos_mios = response.data
          }).catch(error => {
            console.log(error)
          })
        }
      }).catch(error => {
        console.log(error)
      }).finally(() => {
        this.tabla_loading = false
      })
    }
  },
  mounted() {
    const token = cookies.get("access_token")
    if (token) {
      this.$auth.refreshToken().then(response => {
        console.log("refreshToken", response)
        this.getProyectos()
      })
    } else {
      this.getProyectos()
    }
  }
}
</script>

<style lang="scss" scoped>
.q-menu.q-position-engine.scroll {
  min-width: initial;
}
</style>
