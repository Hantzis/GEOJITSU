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
        <q-tab name="mias" label="Evaluaciones promovidas por mí"/>
        <q-tab name="todas" label="Todas las evaluaciones"/>
      </q-tabs>
      <q-separator/>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="mias">
          <div class="row">
            <div class="col">
              <q-table
                title="Evaluaciones promovidas por mí"
                :data.sync="datos_evaluaciones_mias"
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
      </q-tab-panels>
    </q-card>

    <q-dialog ref="add_evaluacion_dialog" full-width full-height v-model="add_evaluacion_dialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-chart-timeline" color="primary" text-color="white"/>
          <q-toolbar-title>Nueva evaluación</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="closeAddEvaluacionDialog"/>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 86vh" class="scroll">
          <q-form ref="form_add" autocomplete="off" greedy>
            <div class="row q-py-xs">
              <q-select
                style="width: 100%"
                name="proyecto"
                label="Proyecto"
                outlined
                v-model="evaluacion_data.proyecto"
                :options="datos_proyectos"
                emit-value
                map-options
                option-value="id"
                option-label="nombre_proyecto"
                :rules="[val => !!val || 'Estado obligatorio']"
              />
            </div>

            <div class="row q-py-xs">
              <div class="col-3 q-pr-md">

              </div>
              <div class="col-3 q-pr-md">

              </div>
              <div class="col-3 q-pr-md">

              </div>
              <div class="col-3">

              </div>
            </div>

            <div class="row q-py-xs">
              <q-list bordered class="rounded-borders" style="width: 100%;">
                <q-expansion-item
                  expand-separator
                  label="Generación de conocimiento"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <q-toggle v-model="evaluacion_data.generacion_conocimiento.aplica">
                            <span>{{ evaluacion_data.generacion_conocimiento.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section v-if="evaluacion_data.generacion_conocimiento.aplica" class="align-center">

                      <q-expansion-item
                        label="Formación de investigadores comunitarios"
                      >
                        <q-card>
                          <q-card-section>
                            <div class="row justify-center">
                              <q-rating
                                v-model="evaluacion_data.generacion_conocimiento.test"
                                size="3.5em"
                                color="grey"
                                :color-selected="ratingColors"
                              >
                                <template v-slot:tip-1>
                                  <q-tooltip>Not bad</q-tooltip>
                                </template>
                                <template v-slot:tip-2>
                                  <q-tooltip max-width="76%" anchor="top middle" self="bottom middle" :offset="[10, 10]"
                                             content-class="bg-black"
                                             content-style="font-size: 16px">
                                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                                    Asperiores cum debitis doloribus eius in perferendis quibusdam quis rem repellat
                                    saepe.
                                    Commodi corporis, harum magni nisi officia quidem reiciendis ullam voluptatum.
                                  </q-tooltip>

                                </template>
                                <template v-slot:tip-3>
                                  <q-tooltip>Very good!</q-tooltip>
                                </template>
                                <template v-slot:tip-4>
                                  <q-tooltip>Very good!</q-tooltip>
                                </template>
                                <template v-slot:tip-5>
                                  <q-tooltip>Very good!</q-tooltip>
                                </template>

                              </q-rating>
                            </div>
                          </q-card-section>
                        </q-card>
                      </q-expansion-item>


                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-separator/>

                <q-expansion-item
                  expand-separator
                  label="Certificaciones"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col" :align="'right'">
                          <q-btn no-caps color="green" @click="certificacionDialog = true">Agregar certificación</q-btn>
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <q-list bordered separator>

                        <q-item clickable v-ripple v-for="(item, idx) in nuevas_certificaciones" :key="idx">
                          <q-item-section>
                            <div class="row no-wrap justify-between">
                              <div class="col-11">
                                <span>{{ item.nombre }} ({{ item.fecha }}, {{ item.fuente }})</span>
                              </div>
                              <div class="col-1 " style="text-align: right;">
                                <div class="row no-wrap">
                                  <!-- <q-btn flat dense @click.stop="console.log(22)" icon="edit" color="primary"></q-btn> -->
                                  <q-btn flat dense @click.stop="deleteCertificacion(idx)" icon="delete"
                                         color="red"></q-btn>
                                </div>
                              </div>
                            </div>
                          </q-item-section>
                        </q-item>

                      </q-list>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-separator/>

                <q-expansion-item
                  expand-separator
                  label="Reconocimientos"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col" :align="'right'">
                          <q-btn no-caps color="green" @click="reconocimientoDialog = true">Agregar reconocimiento
                          </q-btn>
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <q-list bordered separator>

                        <q-item clickable v-ripple v-for="(item, idx) in nuevos_reconocimientos" :key="idx">
                          <q-item-section>
                            <div class="row no-wrap justify-between">
                              <div class="col-11">
                                <span>{{ item.nombre }} ({{ item.fecha }}, {{ item.fuente }})</span>
                              </div>
                              <div class="col-1 " style="text-align: right;">
                                <div class="row no-wrap">
                                  <!-- <q-btn flat dense @click.stop="console.log(22)" icon="edit" color="primary"></q-btn> -->
                                  <q-btn flat dense @click.stop="deleteReconocimiento(idx)" icon="delete"
                                         color="red"></q-btn>
                                </div>
                              </div>
                            </div>
                          </q-item-section>
                        </q-item>

                      </q-list>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-separator/>

                <q-expansion-item
                  expand-separator
                  label="Redes"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col" :align="'right'">
                          <q-btn no-caps color="green" @click="redDialog = true">Agregar red</q-btn>
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <q-list bordered separator>
                        <q-item clickable v-ripple v-for="(item, idx) in nuevas_redes" :key="idx">
                          <q-item-section>
                            <div class="row no-wrap justify-between">
                              <div class="col-11">
                                <span>{{ item.nombre }}</span>
                              </div>
                              <div class="col-1 " style="text-align: right;">
                                <div class="row no-wrap">
                                  <!-- <q-btn flat dense @click.stop="console.log(22)" icon="edit" color="primary"></q-btn> -->
                                  <q-btn flat dense @click.stop="deleteRed(idx)" icon="delete" color="red"></q-btn>
                                </div>
                              </div>
                            </div>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-separator/>

                <q-expansion-item
                  expand-separator
                  label="Financiamientos"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col" :align="'right'">
                          <q-btn no-caps color="green" @click="financiamientoDialog = true">Agregar financiamiento
                          </q-btn>
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <q-list bordered separator>
                        <q-item clickable v-ripple v-for="(item, idx) in nuevos_financiamientos" :key="idx">
                          <q-item-section>
                            <div class="row no-wrap justify-between">
                              <div class="col-11">
                                <span>{{ item.nombre }} ({{ item.fuente }})</span>
                              </div>
                              <div class="col-1 " style="text-align: right;">
                                <div class="row no-wrap">
                                  <!-- <q-btn flat dense @click.stop="console.log(22)" icon="edit" color="primary"></q-btn> -->
                                  <q-btn flat dense @click.stop="deleteFinanciamiento(idx)" icon="delete"
                                         color="red"></q-btn>
                                </div>
                              </div>
                            </div>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>

              </q-list>
            </div>

          </q-form>
          <div class="row justify-end q-py-md">
            <div class="col-auto q-pr-xs">
              <q-btn @click="closeAddEvaluacionDialog()" color="grey-7"
                     label="Cancelar" no-caps class=""/>
            </div>
            <div class="col-auto q-pl-xs">
              <q-btn @click="addEvaluacion()" color="green"
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
import {mapGetters} from "vuex";

export default {
  name: 'casosExito',
  data() {
    return {
      filter: '',
      token: "",
      add_evaluacion_dialog: false,
      tab: 'mias',
      ratingColors: ['light-green-3', 'light-green-6', 'green', 'green-9', 'green-10'],
      evaluacion_data_template: {generacion_conocimiento: {aplica: false, test: 0}},
      evaluacion_data: {generacion_conocimiento: {aplica: false, test: 0}},
      datos_proyectos: undefined,
      proyecto_data: undefined,
      nuevo_logro: {nombre: "", fecha: ""},
      nuevos_logros: [],
      nueva_certificacion: {nombre: "", fuente: "", fecha: ""},
      nuevas_certificaciones: [],
      nuevo_reconocimiento: {nombre: "", fuente: "", fecha: ""},
      nuevos_reconocimientos: [],
      nueva_red: {nombre: "", integrantes: ""},
      nuevas_redes: [],
      nuevo_financiamiento: {nombre: "", fuente: "", monto: ""},
      nuevos_financiamientos: [],
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
    addEvaluacion() {
      // aqui va todo el chisme que envia al api la evaluación
    },
    closeAddEvaluacionDialog() {
      this.add_evaluacion_dialog = false
      this.evaluacion_data = this.evaluacion_data_template
    },
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
    getMisProyectos() {
      this.token = cookies.get("access_token")
      axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/proyectos/?promovente=${this.auth_user.pk}`,
        {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
        this.datos_proyectos = response.data
        console.log(this.datos_proyectos)
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
        this.getMisProyectos()
      })
    } else {
      this.getEvaluaciones()
    }
  },
}
</script>
