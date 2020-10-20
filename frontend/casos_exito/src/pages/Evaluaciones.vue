<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Casos de éxito" icon="mdi-format-list-checks"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" @click="getEvaluaciones()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn no-caps v-if="auth_logged" style="margin-left: 8px;" color="green" @click="add_evaluacion_dialog = true">
          <q-icon left size="2em" name="mdi-plus"/>
          <div style="margin-top: 2px;">Nueva evaluación</div>
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
        <q-tab name="todas" label="Todas las evaluaciones"/>
        <q-tab name="mios" label="Casos promovidos por mí"/>
      </q-tabs>

      <q-separator/>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="todas">
          <div class="row">
            <div class="col">
              <q-table
                title="Todas las evaluaciones"
                :data.sync="datos_evaluaciones"
                :columns="columnas"
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
                      <!-- <q-btn dense round flat color="accent" @click="props.expand = !props.expand"
                             :icon="props.expand ? 'remove' : 'add'"></q-btn>
                      <q-btn v-if="es_usuario" dense round flat color="primary" @click="editRegistroDialog(props)"
                             icon="edit"></q-btn>
                      <q-btn v-if="es_usuario" dense round flat color="red" @click="deleteRegistroDialog(props)"
                             icon="delete"></q-btn> -->
                    </q-td>
                  </q-tr>
                </template>

              </q-table>
            </div>
          </div>


        </q-tab-panel>

        <q-tab-panel name="mios">
          <div class="text-h6">Movies</div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>
      </q-tab-panels>
    </q-card>


  </q-page>
</template>

<script>
import axios from 'axios'
import cookies from 'browser-cookies'
import {mapGetters} from "vuex";

export default {
  name: 'casosExito',
  data() {
    return {
      filter: '',
      token: "",
      add_evaluacion_dialog: false,
      tab: 'todas',
      datos_evaluaciones_mias: undefined,
      datos_evaluaciones: undefined,
      columnas: [
        {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true},
        {
          name: 'proyecto_display',
          align: 'left',
          label: 'Nombre de proyecto',
          field: 'proyecto_display',
          sortable: true
        },
        {name: 'fecha', align: 'left', label: 'Fecha de evaluación', field: 'fecha', sortable: true},
      ],
      tabla_loading: true,

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
    getEvaluaciones() {
      this.token = cookies.get("access_token")
      axios.get("https://onsses45.maptitude.xyz/api/v1/ce/evaluaciones/").then(response => {
        console.log("response evaluaciones: ", response.data)
        this.datos_evaluaciones = response.data
      }).then(() => {
        if (this.token) {
          axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/evaluaciones/?promovente=${this.auth_user.pk}`,
            {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
            this.datos_evaluaciones_mias = response.data
          }).catch(error => {
            console.log(error)
          })
        }
      }).catch(error => {
        console.log(error)
      }).finally(() => {
        this.tabla_loading = false
      })
    },
  },
  mounted() {
    try {
      this.token = cookies.get("access_token")
    } catch (error) {
      console.log(error)
    }
    if (this.token) {
      this.$auth.refreshToken().then(response => {
        console.log("refreshToken", response)
        this.getEvaluaciones()
      })
    } else {
      this.getEvaluaciones()
    }
  },
}
</script>
