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

                <q-expansion-item expand-separator label="Integridad territorial">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Incorporado a una estrategia de ordenamiento del territorio, local, y/o regional que considere un plan de vida o proyecto de resiliencia, y es reconocido en el territorio.</p>
                          <q-toggle v-model="eval_integridad_territorial.aplica">
                            <span>{{ eval_integridad_territorial.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_integridad_territorial.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_integridad_territorial.alineado_programas_ordenamiento.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_integridad_territorial.alineado_programas_ordenamiento.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_integridad_territorial.alineado_programas_ordenamiento.options[eval_integridad_territorial.alineado_programas_ordenamiento.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-separator/>
                        <q-expansion-item
                          :label="eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{ eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.options[1] }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.options[eval_integridad_territorial.alineado_programas_ordenamiento_comunitario.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-separator/>
                        <q-expansion-item
                          :label="eval_integridad_territorial.aporta_beneficios_comunidad.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_integridad_territorial.aporta_beneficios_comunidad.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.aporta_beneficios_comunidad.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.aporta_beneficios_comunidad.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.aporta_beneficios_comunidad.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.aporta_beneficios_comunidad.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_integridad_territorial.aporta_beneficios_comunidad.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_integridad_territorial.aporta_beneficios_comunidad.options[eval_integridad_territorial.aporta_beneficios_comunidad.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-expansion-item expand-separator label="Identidad biocultural">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>El proyecto respeta los usos y costumbres locales.</p>
                          <q-toggle v-model="eval_identidad_biocultural.aplica">
                            <span>{{ eval_identidad_biocultural.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_identidad_biocultural.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_identidad_biocultural.fomenta_lengua_local.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_identidad_biocultural.fomenta_lengua_local.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.fomenta_lengua_local.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.fomenta_lengua_local.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.fomenta_lengua_local.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.fomenta_lengua_local.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.fomenta_lengua_local.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_identidad_biocultural.fomenta_lengua_local.options[eval_identidad_biocultural.fomenta_lengua_local.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_identidad_biocultural.participacion_celebraciones_locales.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_identidad_biocultural.participacion_celebraciones_locales.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_celebraciones_locales.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_celebraciones_locales.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_celebraciones_locales.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_celebraciones_locales.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_celebraciones_locales.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_identidad_biocultural.participacion_celebraciones_locales.options[eval_identidad_biocultural.participacion_celebraciones_locales.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_identidad_biocultural.participacion_intercambio_saberes_locales.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_identidad_biocultural.participacion_intercambio_saberes_locales.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_intercambio_saberes_locales.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_intercambio_saberes_locales.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_intercambio_saberes_locales.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_intercambio_saberes_locales.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.participacion_intercambio_saberes_locales.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_identidad_biocultural.participacion_intercambio_saberes_locales.options[eval_identidad_biocultural.participacion_intercambio_saberes_locales.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_identidad_biocultural.conservacion_patrimonio_biocultural.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_identidad_biocultural.conservacion_patrimonio_biocultural.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.conservacion_patrimonio_biocultural.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.conservacion_patrimonio_biocultural.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.conservacion_patrimonio_biocultural.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.conservacion_patrimonio_biocultural.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.conservacion_patrimonio_biocultural.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_identidad_biocultural.conservacion_patrimonio_biocultural.options[eval_identidad_biocultural.conservacion_patrimonio_biocultural.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_identidad_biocultural.promocion_practicas_tradicionales.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_identidad_biocultural.promocion_practicas_tradicionales.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.promocion_practicas_tradicionales.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.promocion_practicas_tradicionales.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.promocion_practicas_tradicionales.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.promocion_practicas_tradicionales.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_identidad_biocultural.promocion_practicas_tradicionales.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_identidad_biocultural.promocion_practicas_tradicionales.options[eval_identidad_biocultural.promocion_practicas_tradicionales.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-expansion-item expand-separator label="Gestión ambiental">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Manejo sustentable de flora y fauna silvestre, residuos sólidos, gestión del agua tanto para uso doméstico como tratamiento y disposición de aguas servidas y estrategias de conservación de suelo.</p>
                          <q-toggle v-model="eval_gestion_ambiental.aplica">
                            <span>{{ eval_gestion_ambiental.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_gestion_ambiental.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_gestion_ambiental.gestion_agua.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.gestion_agua.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_agua.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_agua.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_agua.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_agua.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_agua.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.gestion_agua.options[eval_gestion_ambiental.gestion_agua.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.gestion_residuos_solidos.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.gestion_residuos_solidos.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_solidos.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_solidos.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_solidos.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_solidos.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_solidos.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.gestion_residuos_solidos.options[eval_gestion_ambiental.gestion_residuos_solidos.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.gestion_residuos_peligrosos.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.gestion_residuos_peligrosos.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_peligrosos.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_peligrosos.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_peligrosos.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_peligrosos.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.gestion_residuos_peligrosos.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.gestion_residuos_peligrosos.options[eval_gestion_ambiental.gestion_residuos_peligrosos.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.materiales_regionales.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.materiales_regionales.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_regionales.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_regionales.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_regionales.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_regionales.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_regionales.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.materiales_regionales.options[eval_gestion_ambiental.materiales_regionales.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.materiales_amigables_ambiente.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.materiales_amigables_ambiente.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_amigables_ambiente.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_amigables_ambiente.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_amigables_ambiente.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_amigables_ambiente.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.materiales_amigables_ambiente.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.materiales_amigables_ambiente.options[eval_gestion_ambiental.materiales_amigables_ambiente.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.certificacion_manejo_ambiental.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.certificacion_manejo_ambiental.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.certificacion_manejo_ambiental.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.certificacion_manejo_ambiental.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.certificacion_manejo_ambiental.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.certificacion_manejo_ambiental.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.certificacion_manejo_ambiental.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.certificacion_manejo_ambiental.options[eval_gestion_ambiental.certificacion_manejo_ambiental.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.programa_manejo_flora.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.programa_manejo_flora.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_flora.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_flora.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_flora.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_flora.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_flora.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.programa_manejo_flora.options[eval_gestion_ambiental.programa_manejo_flora.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.programa_manejo_ambiental_avalado.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.programa_manejo_ambiental_avalado.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_ambiental_avalado.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_ambiental_avalado.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_ambiental_avalado.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_ambiental_avalado.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.programa_manejo_ambiental_avalado.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.programa_manejo_ambiental_avalado.options[eval_gestion_ambiental.programa_manejo_ambiental_avalado.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.estrategia_trafico_especies_riesgo.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.estrategia_trafico_especies_riesgo.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.estrategia_trafico_especies_riesgo.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.estrategia_trafico_especies_riesgo.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.estrategia_trafico_especies_riesgo.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.estrategia_trafico_especies_riesgo.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.estrategia_trafico_especies_riesgo.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.estrategia_trafico_especies_riesgo.options[eval_gestion_ambiental.estrategia_trafico_especies_riesgo.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_gestion_ambiental.monitoreo_gestion_ambiental.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_gestion_ambiental.monitoreo_gestion_ambiental.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.monitoreo_gestion_ambiental.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.monitoreo_gestion_ambiental.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.monitoreo_gestion_ambiental.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.monitoreo_gestion_ambiental.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_gestion_ambiental.monitoreo_gestion_ambiental.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_gestion_ambiental.monitoreo_gestion_ambiental.options[eval_gestion_ambiental.monitoreo_gestion_ambiental.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>

                <q-expansion-item expand-separator label="Procesos de gobernanza del proyecto en la organización o el proyecto">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Gobernanza para la mejora del buen gobierno en la toma de decisiones internas.</p>
                          <q-toggle v-model="eval_buen_gobierno_interno.aplica">
                            <span>{{ eval_buen_gobierno_interno.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_buen_gobierno_interno.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_buen_gobierno_interno.regulacion_actores_externos.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_interno.regulacion_actores_externos.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.regulacion_actores_externos.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.regulacion_actores_externos.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.regulacion_actores_externos.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.regulacion_actores_externos.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.regulacion_actores_externos.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_interno.regulacion_actores_externos.options[eval_buen_gobierno_interno.regulacion_actores_externos.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_interno.decisiones_internas_colectivas.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_interno.decisiones_internas_colectivas.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.decisiones_internas_colectivas.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.decisiones_internas_colectivas.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.decisiones_internas_colectivas.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.decisiones_internas_colectivas.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.decisiones_internas_colectivas.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_interno.decisiones_internas_colectivas.options[eval_buen_gobierno_interno.decisiones_internas_colectivas.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.options[eval_buen_gobierno_interno.acuerdos_comunes_resolucion_conflictos.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_interno.espacios_participacion.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_interno.espacios_participacion.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.espacios_participacion.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.espacios_participacion.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.espacios_participacion.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.espacios_participacion.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.espacios_participacion.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_interno.espacios_participacion.options[eval_buen_gobierno_interno.espacios_participacion.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_interno.incorpora_cosmovision_local.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_interno.incorpora_cosmovision_local.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.incorpora_cosmovision_local.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.incorpora_cosmovision_local.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.incorpora_cosmovision_local.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.incorpora_cosmovision_local.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.incorpora_cosmovision_local.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_interno.incorpora_cosmovision_local.options[eval_buen_gobierno_interno.incorpora_cosmovision_local.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.options[eval_buen_gobierno_interno.mecanismos_rendicion_cuentas.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.options[eval_buen_gobierno_interno.monitoreo_gestion_gobernanza.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>



                <q-expansion-item expand-separator label="eval_buen_gobierno_externo">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Estrategias para el diálogo de saberes y sistematización del conocimiento generado.</p>
                          <q-toggle v-model="eval_buen_gobierno_externo.aplica">
                            <span>{{ eval_buen_gobierno_externo.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_buen_gobierno_externo.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_buen_gobierno_externo.participacion_activa_reglamentos.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_externo.participacion_activa_reglamentos.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_activa_reglamentos.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_activa_reglamentos.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_activa_reglamentos.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_activa_reglamentos.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_activa_reglamentos.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_externo.participacion_activa_reglamentos.options[eval_buen_gobierno_externo.participacion_activa_reglamentos.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_externo.participacion_equitativa_reglamentos.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_externo.participacion_equitativa_reglamentos.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_equitativa_reglamentos.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_equitativa_reglamentos.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_equitativa_reglamentos.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_equitativa_reglamentos.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_equitativa_reglamentos.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_externo.participacion_equitativa_reglamentos.options[eval_buen_gobierno_externo.participacion_equitativa_reglamentos.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_externo.participacion_previa_libre_informada.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_externo.participacion_previa_libre_informada.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_previa_libre_informada.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_previa_libre_informada.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_previa_libre_informada.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_previa_libre_informada.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_previa_libre_informada.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_externo.participacion_previa_libre_informada.options[eval_buen_gobierno_externo.participacion_previa_libre_informada.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_externo.participacion_otros_actores.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_externo.participacion_otros_actores.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_otros_actores.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_otros_actores.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_otros_actores.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_otros_actores.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.participacion_otros_actores.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_externo.participacion_otros_actores.options[eval_buen_gobierno_externo.participacion_otros_actores.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.label"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.options[eval_buen_gobierno_externo.monitoreo_gestion_gobernanza.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>



                <q-expansion-item expand-separator label="Generación de conocimiento">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Estrategias para el diálogo de saberes y sistematización del conocimiento generado.</p>
                          <q-toggle v-model="eval_generacion_conocimiento.aplica">
                            <span>{{ eval_generacion_conocimiento.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_generacion_conocimiento.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          label="Formación de investigadores comunitarios"
                        >
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_generacion_conocimiento.formacion_investigadores_comunitarios.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.formacion_investigadores_comunitarios.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.formacion_investigadores_comunitarios.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.formacion_investigadores_comunitarios.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.formacion_investigadores_comunitarios.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.formacion_investigadores_comunitarios.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_generacion_conocimiento.formacion_investigadores_comunitarios.options[eval_generacion_conocimiento.formacion_investigadores_comunitarios.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-separator/>
                        <q-expansion-item
                          :label="eval_generacion_conocimiento.inovacion_saberes_locales.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_generacion_conocimiento.inovacion_saberes_locales.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{ eval_generacion_conocimiento.inovacion_saberes_locales.options[1] }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.inovacion_saberes_locales.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.inovacion_saberes_locales.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.inovacion_saberes_locales.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.inovacion_saberes_locales.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_generacion_conocimiento.inovacion_saberes_locales.options[eval_generacion_conocimiento.inovacion_saberes_locales.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-separator/>
                        <q-expansion-item
                          :label="eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.options[eval_generacion_conocimiento.gestion_documental_generacion_conocimiento.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>

                        <q-separator/>
                        <q-expansion-item
                          :label="eval_generacion_conocimiento.eventos_intercambio_saberes.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_generacion_conocimiento.eventos_intercambio_saberes.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{ eval_generacion_conocimiento.eventos_intercambio_saberes.options[1] }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.eventos_intercambio_saberes.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.eventos_intercambio_saberes.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.eventos_intercambio_saberes.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.eventos_intercambio_saberes.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_generacion_conocimiento.eventos_intercambio_saberes.options[eval_generacion_conocimiento.eventos_intercambio_saberes.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>

                        <q-separator/>
                        <q-expansion-item
                          :label="eval_generacion_conocimiento.monitoreo_generacion_conocimiento.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_generacion_conocimiento.monitoreo_generacion_conocimiento.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColorsGreens"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{ eval_generacion_conocimiento.monitoreo_generacion_conocimiento.options[1] }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.monitoreo_generacion_conocimiento.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.monitoreo_generacion_conocimiento.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.monitoreo_generacion_conocimiento.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_generacion_conocimiento.monitoreo_generacion_conocimiento.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_generacion_conocimiento.monitoreo_generacion_conocimiento.options[eval_generacion_conocimiento.monitoreo_generacion_conocimiento.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>



                <q-expansion-item expand-separator label="eval_manejo_riesgo">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Estrategias para el diálogo de saberes y sistematización del conocimiento generado.</p>
                          <q-toggle v-model="eval_manejo_riesgo.aplica">
                            <span>{{ eval_manejo_riesgo.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_manejo_riesgo.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_manejo_riesgo.alineado_diagnostico_riesgo.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_manejo_riesgo.alineado_diagnostico_riesgo.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.alineado_diagnostico_riesgo.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.alineado_diagnostico_riesgo.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.alineado_diagnostico_riesgo.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.alineado_diagnostico_riesgo.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.alineado_diagnostico_riesgo.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_manejo_riesgo.alineado_diagnostico_riesgo.options[eval_manejo_riesgo.alineado_diagnostico_riesgo.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_manejo_riesgo.programa_contingencia_riesgo.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_manejo_riesgo.programa_contingencia_riesgo.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programa_contingencia_riesgo.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programa_contingencia_riesgo.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programa_contingencia_riesgo.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programa_contingencia_riesgo.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programa_contingencia_riesgo.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_manejo_riesgo.programa_contingencia_riesgo.options[eval_manejo_riesgo.programa_contingencia_riesgo.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_manejo_riesgo.participa_comites_proteccion_civil.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_manejo_riesgo.participa_comites_proteccion_civil.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.participa_comites_proteccion_civil.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.participa_comites_proteccion_civil.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.participa_comites_proteccion_civil.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.participa_comites_proteccion_civil.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.participa_comites_proteccion_civil.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_manejo_riesgo.participa_comites_proteccion_civil.options[eval_manejo_riesgo.participa_comites_proteccion_civil.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_manejo_riesgo.fondo_ahorro_contingencia.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_manejo_riesgo.fondo_ahorro_contingencia.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.fondo_ahorro_contingencia.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.fondo_ahorro_contingencia.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.fondo_ahorro_contingencia.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.fondo_ahorro_contingencia.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.fondo_ahorro_contingencia.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_manejo_riesgo.fondo_ahorro_contingencia.options[eval_manejo_riesgo.fondo_ahorro_contingencia.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_manejo_riesgo.programas_capacitacion_riesgo.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_manejo_riesgo.programas_capacitacion_riesgo.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programas_capacitacion_riesgo.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programas_capacitacion_riesgo.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programas_capacitacion_riesgo.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programas_capacitacion_riesgo.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.programas_capacitacion_riesgo.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_manejo_riesgo.programas_capacitacion_riesgo.options[eval_manejo_riesgo.programas_capacitacion_riesgo.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_manejo_riesgo.monitoreo_gestion_riesgo.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_manejo_riesgo.monitoreo_gestion_riesgo.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.monitoreo_gestion_riesgo.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.monitoreo_gestion_riesgo.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.monitoreo_gestion_riesgo.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.monitoreo_gestion_riesgo.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_manejo_riesgo.monitoreo_gestion_riesgo.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_manejo_riesgo.monitoreo_gestion_riesgo.options[eval_manejo_riesgo.monitoreo_gestion_riesgo.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>



                <q-expansion-item expand-separator label="eval_produccion_social_ambiental_amigable">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Estrategias para el diálogo de saberes y sistematización del conocimiento generado.</p>
                          <q-toggle v-model="eval_produccion_social_ambiental_amigable.aplica">
                            <span>{{ eval_produccion_social_ambiental_amigable.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_produccion_social_ambiental_amigable.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.options[eval_produccion_social_ambiental_amigable.insumos_bajo_impacto_ambiental.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.options[eval_produccion_social_ambiental_amigable.tecnologia_respetuosa_naturaleza.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_produccion_social_ambiental_amigable.respeta_saberes_locales.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_produccion_social_ambiental_amigable.respeta_saberes_locales.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.respeta_saberes_locales.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.respeta_saberes_locales.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.respeta_saberes_locales.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.respeta_saberes_locales.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.respeta_saberes_locales.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_produccion_social_ambiental_amigable.respeta_saberes_locales.options[eval_produccion_social_ambiental_amigable.respeta_saberes_locales.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.options[eval_produccion_social_ambiental_amigable.privilegia_trabajo_local.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.options[eval_produccion_social_ambiental_amigable.monitoreo_estrategias_produccion.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                      </q-list>

                    </q-card-section>
                  </q-card>
                </q-expansion-item>



                <q-expansion-item expand-separator label="Economía social y solidaria">
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col">
                          <p>Estrategias para el diálogo de saberes y sistematización del conocimiento generado.</p>
                          <q-toggle v-model="eval_economia_social_solidaria.aplica">
                            <span>{{ eval_economia_social_solidaria.aplica ? 'Aplica' : 'No aplica' }}</span>
                          </q-toggle>
                        </div>
                      </div>
                    </q-card-section>

                    <q-card-section v-if="eval_economia_social_solidaria.aplica" class="align-center">
                      <q-list bordered class="rounded-borders">
                        <q-expansion-item
                          :label="eval_economia_social_solidaria.cooperacion_colaboracion.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_economia_social_solidaria.cooperacion_colaboracion.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.cooperacion_colaboracion.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.cooperacion_colaboracion.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.cooperacion_colaboracion.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.cooperacion_colaboracion.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.cooperacion_colaboracion.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_economia_social_solidaria.cooperacion_colaboracion.options[eval_economia_social_solidaria.cooperacion_colaboracion.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_economia_social_solidaria.intercambio_organizaciones.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_economia_social_solidaria.intercambio_organizaciones.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_organizaciones.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_organizaciones.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_organizaciones.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_organizaciones.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_organizaciones.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_economia_social_solidaria.intercambio_organizaciones.options[eval_economia_social_solidaria.intercambio_organizaciones.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_economia_social_solidaria.intercambio_local.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_economia_social_solidaria.intercambio_local.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_local.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_local.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_local.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_local.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.intercambio_local.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_economia_social_solidaria.intercambio_local.options[eval_economia_social_solidaria.intercambio_local.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_economia_social_solidaria.insumos_locales.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_economia_social_solidaria.insumos_locales.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.insumos_locales.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.insumos_locales.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.insumos_locales.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.insumos_locales.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.insumos_locales.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_economia_social_solidaria.insumos_locales.options[eval_economia_social_solidaria.insumos_locales.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_economia_social_solidaria.autonomia_financiera.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_economia_social_solidaria.autonomia_financiera.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.autonomia_financiera.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.autonomia_financiera.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.autonomia_financiera.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.autonomia_financiera.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.autonomia_financiera.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_economia_social_solidaria.autonomia_financiera.options[eval_economia_social_solidaria.autonomia_financiera.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_economia_social_solidaria.economia_circular.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_economia_social_solidaria.economia_circular.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.economia_circular.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.economia_circular.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.economia_circular.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.economia_circular.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.economia_circular.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_economia_social_solidaria.economia_circular.options[eval_economia_social_solidaria.economia_circular.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
                        <q-expansion-item
                          :label="eval_economia_social_solidaria.monitoreo_emprendimientos.label">
                          <q-card>
                            <q-card-section>
                              <div class="row justify-center">
                                <q-rating
                                  v-model="eval_economia_social_solidaria.monitoreo_emprendimientos.value"
                                  size="3.5em"
                                  color="grey"
                                  :color-selected="ratingColors"
                                >
                                  <template v-slot:tip-1>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.monitoreo_emprendimientos.options[1]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-2>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.monitoreo_emprendimientos.options[2]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-3>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.monitoreo_emprendimientos.options[3]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-4>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.monitoreo_emprendimientos.options[4]
                                      }}
                                    </q-tooltip>
                                  </template>
                                  <template v-slot:tip-5>
                                    <q-tooltip max-width="76%" anchor="top middle" self="bottom middle"
                                               :offset="[10, 10]"
                                               content-class="bg-black" content-style="font-size: 16px">
                                      {{
                                        eval_economia_social_solidaria.monitoreo_emprendimientos.options[5]
                                      }}
                                    </q-tooltip>
                                  </template>
                                </q-rating>
                              </div>
                              <div class="row justify-center">
                                <div class="col">
                                  {{
                                    eval_economia_social_solidaria.monitoreo_emprendimientos.options[eval_economia_social_solidaria.monitoreo_emprendimientos.value]
                                  }}
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </q-expansion-item>
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
      ratingColorsGreens: ['light-green-3', 'light-green-6', 'green', 'green-9', 'green-10'],
      ratingColors: ['red', 'orange', 'yellow', 'green', 'blue'],
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
      eval_integridad_territorial: {
        aplica: false,
        alineado_programas_ordenamiento: {
          label: "El proyecto está alineado a algún programa de ordenamiento (federal, estatal, regional, municipal, local, comunitario y/o plan de vida)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de alinear el proyecto con un programa de ordenamiento",
            "Se reconoce la importancia de los programas de ordenamiento territorial pero el proyecto no está alineado a alguno",
            "Se ha identificado como alinear el proyecto a algún programa de ordenamiento territorial",
            "Se está construyendo una alineación a los programas de ordenamiento (federal, estatal y regional)",
            "El proyecto está alineado a los programas de ordenamiento",
          ]
        },
        alineado_programas_ordenamiento_comunitario: {
          label: "El proyecto participa en algún otro comité comunitario o vecinal relacionado con los planes para el desarrollo local y/o el plan de vida",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de participar en algún comité comunitario o vecinal relacionado con los planes para el desarrollo local y/o el plan de vida",
            "Se reconoce la importancia de participar en algún comité comunitario o vecinal relacionado con los planes para el desarrollo local y/o plan de vida, pero no se participa",
            "Ocasionalmente se participa en algún comité comunitario y/o vecinal relacionado con los planes para el desarrollo local y/o plan de vida",
            "Frecuentemente se participa en algún comité comunitario y/o vecinal relacionado con los planes para el desarrollo local y/o plan de vida",
            "Siempre se participa en los comités comunitarios o vecinales relacionados con los planes para el desarrollo local y/o el plan de vida",
          ]
        },
        aporta_beneficios_comunidad: {
          label: "El proyecto aporta algún beneficio para la comunidad en los siguientes rubros:  político, social, económico y/o ambiental. Por ejemplo, genera información para la toma de decisiones y procesos reflexivos sobre la integridad territorial",
          value: 0, options: [
            "No aplica",
            "No se reconoce si se ha generado algún beneficio para la comunidad",
            "Se reconoce que se han generado beneficios para la comunidad, pero no se ha identificado en qué ámbitos",
            "Se reconoce que se han generado beneficios para la comunidad, pero sólo en alguno de los rubros mencionados",
            "Se reconoce que se han generado beneficios para la comunidad, en la mayoría de los rubros mencionados",
            "Se reconoce que se han generado beneficios para la comunidad en todos los rubros",
          ]
        },
      },
      eval_identidad_biocultural: {
        aplica: false,
        fomenta_lengua_local: {
          label: "El proyecto fomenta y promueve la lengua local",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de la lengua local en el proyecto",
            "Se reconoce la importancia de la lengua local en el proyecto, pero no existen acciones de fomento",
            "Se fomenta la lengua local en acciones aisladas",
            "Se fomenta la lengua local en acciones frecuentes",
            "Existe un programa de promoción o de fomento de la lengua local desde el proyecto",
          ]
        },
        participacion_celebraciones_locales: {
          label: "Los integrantes del proyecto participan en trabajos o comités para las celebraciones locales",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de participar en las celebraciones locales",
            "El proyecto no participa de ninguna forma en las celebraciones locales a pesar de conocerlas",
            "Los integrantes del proyecto participan de forma eventual en la organización de celebraciones locales",
            "El proyecto participa frecuentemente en la organización de celebraciones locales",
            "El proyecto participa y hace propias las celebraciones locales",
          ]
        },
        participacion_intercambio_saberes_locales: {
          label: "El proyecto realiza (organiza) y participa en eventos de intercambio de saberes locales",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia para realizar o participar en eventos para el intercambio de los saberes locales",
            "Se reconoce la importancia para realizar o participar en eventos para el intercambio de saberes locales, pero no se efectúan como parte del proyecto",
            "Se realizan y participa en eventos para el intercambio de saberes locales de forma esporádica",
            "Se realizan y participa en eventos para el intercambio de saberes locales de forma frecuente",
            "Siempre se realizan y se participa en eventos para el intercambio de saberes locales y además están incorporados como parte del programa del proyecto",
          ]
        },
        conservacion_patrimonio_biocultural: {
          label: "El proyecto realiza estrategias encaminadas a la conservación del patrimonio biocultural (conocimiento, usos y manejo de la flora)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia del patrimonio biocultural",
            "Se reconoce el patrimonio biocultural pero no es considerado para el proyecto",
            "El proyecto realiza ocasionalmente estrategias encaminadas a la conservación del patrimonio biocultural",
            "El proyecto frecuentemente realiza estrategias encaminadas a la conservación del patrimonio biocultural",
            "En el proyecto siempre se realizan estrategias que incorporan la conservación del patrimonio biocultural",
          ]
        },
        promocion_practicas_tradicionales: {
          label: "El proyecto promociona y promueve el mejoramiento de prácticas tradicionales en los procesos productivos y uso de la naturaleza",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de las prácticas tradicionales en los procesos productivos y uso de la naturaleza",
            "Se reconocen las prácticas tradicionales en los procesos productivos y uso de la naturaleza, pero no son considerados por el proyecto",
            "El proyecto reconoce las prácticas tradicionales en los procesos productivos y uso de la naturaleza y los incorpora ocasionalmente",
            "El proyecto reconoce las prácticas tradicionales en procesos productivos y uso de la naturaleza y los incorpora constantemente",
            "El proyecto promueve y mejora las prácticas tradicionales en los procesos productivos y uso de la naturaleza"
          ]
        },
      },
      eval_gestion_ambiental: {
        aplica: false,
        gestion_agua: {
          label: "El proyecto cuenta con  un programa para gestión del agua (ahorro, reciclaje, tratamiento, reúso)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un programa para gestión del agua",
            "Se reconoce la importancia de un programa integral para la gestión del agua, pero no se cuenta con uno",
            "Se cuenta con un programa de gestión del agua y se lleva a cabo de forma parcial",
            "Se cuenta con un programa de gestión del agua y se lleva a cabo frecuentemente",
            "Siempre se llevan a cabo acciones estipuladas en el programa de gestión del agua"
          ]
        },
        gestion_residuos_solidos: {
          label: "El proyecto cuenta con un programa de gestión de residuos sólidos (separación primaria y secundaria)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un programa de gestión de residuos sólidos",
            "Se reconoce la importancia de los programas de gestión de residuos sólidos, pero no se cuenta con uno",
            "Se cuenta con un programa de gestión de residuos sólidos y se lleva a cabo de forma parcial",
            "Se cuenta con un programa de gestión de residuos sólidos y se lleva a cabo frecuentemente",
            "Siempre se cumplen las disposiciones y procedimientos del plan de gestión de residuos sólidos"
          ]
        },
        gestion_residuos_peligrosos: {
          label: "El proyecto cuenta con un programa de manejo de residuos peligrosos",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un programa de manejo de residuos peligrosos",
            "Se reconoce la importancia de los programas de manejo de residuos peligrosos, pero no se cuenta con uno",
            "Se cuenta con un programa de manejo de residuos peligrosos y se lleva a cabo ocasionalmente",
            "Se cuenta con un programa de gestión de residuos peligrosos Y se lleva a cabo frecuentemente",
            "Siempre se cumple con las disposiciones y procedimientos del plan de gestión de residuos peligrosos"
          ]
        },
        materiales_regionales: {
          label: "El proyecto para su operación y desarrollo de su infraestructura, utiliza preferentemente materiales propios de la región respetando el paisaje local",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia del uso de materiales locales para la construcción de infraestructura",
            "Se reconoce la importancia del uso de materiales de la región, pero los insumos no son adquiridos en la región",
            "De forma ocasional se adquieren insumos adquiridos en la región y se desconoce su impacto ambiental",
            "De forma frecuente se adquieren insumos de la región y se conoce el impacto que se ocasiona",
            "Existe un plan para que la mayoría de insumos y servicios sean adquiridos con proveedores locales evitando su impacto ambiental en la región"
          ]
        },
        materiales_amigables_ambiente: {
          label: "El proyecto evita el uso de agroquímicos, transgénicos y otro elemento no amigable al ambiente, como plásticos de un solo uso, entre otros",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia si las sustancias que se utilizan dañan al ambiente (agroquímicos, transgénicos, plásticos de un solo uso etc.)",
            "Se reconoce el impacto negativo de estos materiales, pero aun así se emplean en los procesos",
            "De forma ocasional se evita el uso de agroquímicos, transgénicos y otros elementos no amigables al ambiente",
            "De forma frecuente se evita el uso de agroquímicos, transgénicos y otros elementos no amigables al ambiente",
            "El proyecto siempre evita el uso de agroquímicos, transgénicos y otros elementos no amigables al ambiente"
          ]
        },
        certificacion_manejo_ambiental: {
          label: "El proyecto cuenta con algún certificado o reconocimiento de pares sobre el manejo ambiental",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con certificaciones sobre manejo ambiental",
            "Se reconoce la importancia de contar con certificados o reconocimientos sobre el manejo ambiental pero no se cuenta con alguno",
            "Se cuenta con un certificado o reconocimiento del manejo ambiental ocasionalmente, pero se desconoce el impacto del mismo sobre el proyecto",
            "Se cuenta con al menos un certificado o reconocimiento del buen desempeño ambiental y se conoce los impactos al proyecto",
            "Se cuenta con certificados y/o reconocimientos de manejo ambiental y se realiza un seguimiento de los impactos al proyecto"
          ]
        },
        programa_manejo_flora: {
          label: "El proyecto cuenta con una estrategia o programa para el manejo y/o conservación de flora silvestre",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con programas para el manejo y/o conservación de la flora silvestre",
            "Se reconoce la importancia del cuidado de la flora silvestre pero no se cuenta con un programa para su manejo y/o conservación",
            "El proyecto cuenta con una estrategia o programa de manejo y/o conservación de flora silvestre y se lleva a cabo ocasionalmente",
            "El proyecto cuenta con una estrategia o programa de manejo y/o conservación de flora silvestre y se lleva a cabo frecuentemente",
            "Siempre se realizan las acciones del programa de manejo y/o conservación de flora silvestre"
          ]
        },
        programa_manejo_ambiental_avalado: {
          label: "El proyecto cuenta con un programa de manejo ambiental (silvícola y/o vida silvestre) avalado por alguna dependencia local o federal",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de que el proyecto cuente con un programa de manejo ambiental (silvícola y/o vida silvestre)",
            "Se reconoce la importancia de los planes de manejo ambiental (silvícola y/o vida silvestre), pero no se cuenta con estos en el proyecto",
            "Se cuenta con alguno de estos planes de manejo ambiental (silvícola y/o vida silvestre), pero se lleva a cabo parcialmente",
            "Se cuentan con estos planes de manejo, se ejecutan estrategias para manejo ambiental (silvícola y/o vida silvestre) de manera frecuente",
            "Se cuentan y ejecutan de manera permanente planes de manejo ambiental (silvícola y/o vida silvestre). Estos se encuentran avalados por dependencias locales y/o federales"
          ]
        },
        estrategia_trafico_especies_riesgo: {
          label: "Existe un plan o estrategia para el control del aprovechamiento y en su caso la comercialización de especies con alguna categoría de riesgo (flora y fauna) y/o sus derivados (tierra de hoja y PFNM, etc.)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de un plan o estrategia para el control del aprovechamiento y en su caso la comercialización de especies con alguna categoría de riesgo (flora y fauna) y/o sus derivados (tierra de hoja y PFNM, etc.)",
            "Se reconoce la importancia de la aplicación de un plan o estrategias para el control del aprovechamiento y en su caso la comercialización de especies con alguna categoría de riesgo (flora y fauna) y/o sus derivados (tierra de hoja y PFNM, etc.), pero no se cuenta con acciones encaminadas a atenderlo",
            "Se cuenta con estrategias para el control del aprovechamiento y en su caso la comercialización de especies con alguna categoría de riesgo (flora y fauna) y/o sus derivados (tierra de hoja y PFNM, etc.), y ocasionalmente se ejecutan",
            "Se cuenta con estrategias para el control del aprovechamiento y en su caso la comercialización de especies con alguna categoría de riesgo (flora y fauna) y/o sus derivados (tierra de hoja y PFNM, etc.), y se ejecutan frecuentemente",
            "Siempre se implementan las acciones del plan para para el control del aprovechamiento y en su caso la comercialización de especies con alguna categoría de riesgo (flora y fauna) y/o sus derivados (tierra de hoja y PFNM, etc.)"
          ]
        },
        monitoreo_gestion_ambiental: {
          label: "Se cuenta con un plan de evaluación y monitoreo del programa de gestión ambiental",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un plan de evaluación y monitoreo del programa de gestión ambiental",
            "Se reconoce la importancia de contar con un plan de evaluación y monitoreo del programa de gestión ambiental, pero no se ha generado",
            "El proyecto cuenta con un plan de evaluación y monitoreo del programa de gestión ambiental y se lleva a cabo ocasionalmente",
            "El proyecto cuenta con un plan de evaluación y monitoreo del programa de gestión ambiental y se lleva a cabo frecuentemente",
            "Siempre se realizan las acciones del plan de evaluación y monitoreo del programa de gestión ambiental"
          ]
        },
      },
      eval_buen_gobierno_interno: {
        aplica: false,
        regulacion_actores_externos: {
          label: "En el proyecto se cuenta con un programa para regular la participación de actores externos (ONG, instituciones de gobierno, técnicos) en la mejora de la gobernanza interna (toma de decisiones internas)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un programa que regule la participación de actores externos en la mejora de la gobernanza interna",
            "Se reconoce la importancia de contar con un programa que regule la participación de agentes externos para la mejora de la gobernanza interna pero no se lleva a cabo",
            "Se cuenta con un programa para regular la participación de actores externos en la mejora de la gobernanza interna, pero se toma en cuenta ocasionalmente",
            "Se cuenta con un programa para regular la participación de actores externos en la mejora de la gobernanza interna, pero se toma en cuenta frecuentemente",
            "Siempre se realizan las acciones del programa para regular la participación de actores externos en la mejora de la gobernanza interna",
          ]
        },
        decisiones_internas_colectivas: {
          label: "En el proyecto las decisiones internas se realizan colectivamente",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de realizar colectivamente decisiones internas",
            "Se reconoce la importancia de realizar colectivamente decisiones internas, pero no se lleva a cabo",
            "En ocasiones se realizan colectivamente decisiones internas",
            "De forma frecuente se realizan colectivamente decisiones internas",
            "Siempre se realizan colectivamente las decisiones internas",
          ]
        },
        acuerdos_comunes_resolucion_conflictos: {
          label: "En el proyecto se realizan acuerdos comunes entre sus integrantes para la resolución de conflictos existentes",
          value: 0, options: [
            "No aplica",
            "No se reconoce la necesidad de realizar acuerdos comunes entre los integrantes del proyecto para resolver conflictos existentes",
            "Se reconoce la necesidad de realizar acuerdos comunes entre los integrantes del proyecto para resolver conflictos, pero no se realizan estos acuerdos",
            "Ocasionalmente existen acuerdos comunes entre los integrantes del proyecto para resolver conflictos",
            "Frecuentemente se tienen acuerdos comunes entre los integrantes del proyecto para resolver conflictos",
            "Siempre se tienen acuerdos comunes entre los integrantes del proyecto para resolver conflictos existentes",
          ]
        },
        espacios_participacion: {
          label: "No se reconoce la importancia de disponer de espacios deliberativos para llevar a cabo la toma de decisiones",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de disponer de espacios deliberativos para llevar a cabo la toma de decisiones",
            "Se reconoce la importancia de disponer espacios deliberativos para llevar a cabo la toma de decisiones, pero aún no se utilizan",
            "La toma de decisiones se realiza de forma ocasional en espacios deliberativos de participación",
            "La toma de decisiones se realiza de forma frecuente en espacios deliberativos de participación",
            "Siempre se realiza la toma de decisiones en espacios deliberativos de participación",
          ]
        },
        incorpora_cosmovision_local: {
          label: "El proyecto cuenta con un programa de buen gobierno que incorpora la cosmovisión local (prácticas, tradiciones y valores referentes al respeto a la naturaleza, el ser humano y la cultura local)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un programa de buen gobierno que incorpora en la cosmovisión local",
            "Se reconoce la importancia de contar con un programa de buen gobierno que incorpora la cosmovisión local pero no se lleva a cabo",
            "Se cuenta con un programa de buen gobierno que incorpora la cosmovisión local y ocasionalmente se lleva a cabo",
            "Se cuenta con un programa de buen gobierno que incorpora la cosmovisión local y frecuentemente se lleva a cabo",
            "Se cuenta con un programa de buen gobierno que incorpora la cosmovisión local y siempre se lleva a cabo",
          ]
        },
        mecanismos_rendicion_cuentas: {
          label: "Se cuenta con mecanismos claros para la  rendicion de cuentas de la organización y/o proyecto",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar mecanismos claros para la  rendicion de cuentas de la organización y/o proyecto",
            "Se reconoce la importancia de contar mecanismos claros para la  rendicion de cuentas de la organización y/o proyecto, pero no se han elaborado",
            "El proyecto cuenta mecanismos claros para la  rendicion de cuentas de la organización y/o proyecto y se lleva a cabo ocasionalmente",
            "El proyecto cuenta mecanismos claros para la  rendicion de cuentas de la organización y/o proyecto y se lleva a cabo frecuentemente",
            "Siempre se ejecutan los mecanismos claros para la  rendicion de cuentas de la organización y/o proyecto",
          ]
        },
        monitoreo_gestion_gobernanza: {
          label: "Se cuenta con un plan de evaluación y monitoreo de las estrategias de gobernanza al interior de la organización y/o proyecto",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un plan de evaluación y monitoreo de las estrategias de gobernanza al interior de la organización y/o proyecto",
            "Se reconoce la importancia de contar con un plan de evaluación y monitoreo de las estrategias de gobernanza al interior de la organización y/o proyecto, pero no se ha elaborado",
            "El proyecto cuenta con un plan de evaluación y monitoreo de las estrategias de gobernanza al interior de la organización y/o proyecto y se lleva a cabo ocasionalmente",
            "El proyecto cuenta con un plan de evaluación y monitoreo de las estrategias de gobernanza al interior de la organización y/o proyecto y se lleva a cabo frecuentemente",
            "Siempre se realizan las acciones del plan de evaluación y monitoreo de las estrategias de gobernanza al interior de la organización y/o proyecto",
          ]
        },
      },
      eval_buen_gobierno_externo: {
        aplica: false,
        participacion_activa_reglamentos: {
          label: "En el proyecto existe participación activa en procesos y elaboración de reglamentos (normas, reglamentos, disposiciones de gobierno a nivel nacional, estatal, municipal o local)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de la participación activa en la elaboración de reglamentos",
            "Se reconoce la importancia de la participación activa en la elaboración de reglamentos, pero no se lleva a cabo",
            "Ocasionalmente se participa de manera activa en el proceso y elaboración de reglamentos",
            "Frecuentemente se participa de manera activa en el proceso y elaboración de reglamentos",
            "Siempre se participa de manera activa en el proceso y elaboración de reglamentos",
          ]
        },
        participacion_equitativa_reglamentos: {
          label: "En el proyecto existe participación equitativa en la elaboración de reglamentos y/o en la toma de decisiones",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de la participación equitativa en la elaboración de reglamentos y/o en la toma de decisiones",
            "Se reconoce la importancia de la participación equitativa en la elaboración de reglamentos y/o en la toma de decisiones, pero no se lleva a cabo",
            "Ocasionalmente se participa de manera equitativa en el proceso y elaboración de reglamentos y/o en la toma de decisiones",
            "Frecuentemente se participa de manera equitativa en el proceso y elaboración de reglamentos y/o en la toma de decisiones",
            "Siempre se participa de manera equitativa en el proceso y elaboración de reglamentos y/o en la toma de decisiones"
          ]
        },
        participacion_previa_libre_informada: {
          label: "Existe la participación previa, libre e informada en las acciones llevadas a cabo por entidades de gobierno, privadas o sociales",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de la participación previa, libre e informada en las acciones de entidades mencionadas",
            "Se reconoce la importancia, pero no se participa de manera previa, libre e informada",
            "Ocasionalmente hay participación previa, libre e informada en las acciones de las entidades antes mencionadas",
            "Frecuentemente hay participación previa, libre e informada en las acciones de las entidades antes mencionadas",
            "Siempre existe la participación previa, libre e informada en las acciones de las entidades antes mencionadas"
          ]
        },
        participacion_otros_actores: {
          label: "En el proyecto existe la participación de otros actores (asesores, comité administrativo, la comunidad) en la gobernanza local",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de la participación de otros actores (asesores, comité administrativo, la comunidad) en la gobernanza local",
            "Se reconoce la participación de otros actores (asesores, comité administrativo, la comunidad) en la gobernanza localpero no se fomenta",
            "Ocasionalmente existe la participación de otros actores (asesores, comité administrativo, la comunidad) en la gobernanza local",
            "Regularmente existe la participación de otros actores (asesores, comité administrativo, la comunidad) en la gobernanza local",
            "Siempre existe participación de otros actores (asesores, comité administrativo, la comunidad) en la gobernanza local"
          ]
        },
        monitoreo_gestion_gobernanza: {
          label: "Se cuenta con un plan de evaluación y monitoreo de la gobernanza para el acceso al bien común",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un plan de evaluación y monitoreo de la gobernanza para el acceso al bien común",
            "Se reconoce la importancia de contar con un plan de evaluación y monitoreo de la gobernanza para el acceso al bien común, pero no se ha elaborado",
            "El proyecto cuenta con un plan de evaluación y monitoreo de la gobernanza para el acceso al bien común y se lleva a cabo ocasionalmente",
            "El proyecto cuenta con un plan de evaluación y monitoreo de la gobernanza para el acceso al bien común y se lleva a cabo frecuentemente",
            "Siempre se realizan las acciones del plan de evaluación y monitoreo de la gobernanza para el acceso al bien común"
          ]
        },
      },
      eval_generacion_conocimiento: {
        aplica: false,
        formacion_investigadores_comunitarios: {
          label: "Formación de investigadores comunitarios",
          value: 0, options: [
            "No aplica",
            "No se reconoce la necesidad de la  formación de investigadores comunitarios",
            "Se reconoce la necesidad formación de investigadores comunitarios, sin embargo no hay estrategias ni un plan",
            "Existe la formación de investigadores comunitarios pero sin estrategias ni planes concretos",
            "Existe la  formación de investigadores comunitarios a través de la propuesta de una estrategia y un plan, pero aún en elaboración",
            "Existen procesos de formación de investigadores comunitarios con un plan y una estrategia implementada y en funcionamiento"
          ]
        },
        inovacion_saberes_locales: {
          label: "Procesos de innovación a partir de los saberes locales",
          value: 0, options: [
            "No aplica",
            "No se reconoce la necesidad de innovar",
            "Se reconoce la necesidad innovar, sin embargo no hay iniciativas al respecto",
            "Existen algunas iniciativas de innovación sustentadas en saberes locales, pero sin estrategias ni planes concretos",
            "Existen procesos de innovación a partir de los saberes locales y a través de la propuesta de una estrategia y un plan, pero aún en elaboración",
            "Existen procesos de innovación a partir de los saberes locales y con un plan y una estrategia implementada y en funcionamiento",
          ]
        },
        gestion_documental_generacion_conocimiento: {
          label: "Gestión documental de los procesos de generación conocimiento o saberes locales",
          value: 0, options: [
            "No aplica",
            "No se reconoce la necesidad de documentar o registrar el conocimiento o saberes locales",
            "Se reconoce la necesidad de documentar el conocimiento o saberes locales, sin embargo, no hay inicativas al respecto",
            "Existen algunas iniciativas encaminadas a la documentación de saberes locales, pero sin alguna estrategia o plan",
            "Existen procesos de gestión documental sobre la generación del conocimientro o saberes locales, pero aún sin algun resultado",
            "Existen procesos de gestión documental sobre la generación del conocimientro o saberes locales, con un plan y una estrategia implementada y con resultados",
          ]
        },
        eventos_intercambio_saberes: {
          label: "Se realizan periódicamente eventos o reuniones de intercambio de saberes con otros grupos u organizaciones locales, regionales o nacionales",
          value: 0, options: [
            "No aplica",
            "No se reconoce la necesidad de realizar eventos o reuniones de intercambio de saberes con otros grupos u organizaciones locales, regionales o nacionales",
            "Se reconoce la necesidad de realizar eventos o reuniones de intercambio de saberes con otros grupos u organizaciones locales, regionales o nacionales, sin embargo, no hay inicativas al respecto",
            "Ocacionalmente se realizan eventos o reuniones de intercambio de saberes con otros grupos u organizaciones locales, regionales o nacionales, pero sin alguna estrategia o plan",
            "Se realizan de manera frecuente eventos y/o reuniones de intercambio de saberes con otros grupos u organizaciones locales, regionales o nacionales, aunque no se cuenta con un plan",
            "Existe un plan para la realización de eventos y/o reuniones de intercambio de saberes con otros grupos u organizaciones locales, regionales o nacionales y se llevan a cabo permanentemente",
          ]
        },
        monitoreo_generacion_conocimiento: {
          label: "Se cuenta con un plan de evaluación y monitoreo de la estrategia de generación del conocimiento",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un plan de evaluación y monitoreo de la estrategia de generación del conocimiento",
            "Se reconoce la importancia de contar con un plan de evaluación y monitoreo del programa de la estrategia de generación del conocimiento, pero no se ha generado",
            "El proyecto cuenta con un plan de evaluación y monitoreo de la estrategia de generación del conocimiento y se lleva a cabo ocasionalmente",
            "El proyecto cuenta con un plan de evaluación y monitoreo de la estrategia de generación del conocimiento y se lleva a cabo frecuentemente",
            "Siempre se realizan las acciones del plan de evaluación y monitoreo de la estrategia de generación del conocimiento",
          ]
        },
      },
      eval_manejo_riesgo: {
        aplica: false,
        alineado_diagnostico_riesgo: {
          label: "El proyecto se encuentra alineado con un diagnóstico integral de riesgo y vulnerabilidades del territorio",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un diagnóstico integral de riesgos, amenazas y vulnerabilidades del territorio",
            "Se reconoce la importancia de estar alineado a un diagnóstico integral de riesgos, amenazas y vulnerabilidades del territorio, pero no se encuentra alineado",
            "Se han empezado a identificar riesgos, amenazas y vulnerabilidades, pero no se está alineado a un diagnóstico integral de riesgos, amenazas y vulnerabilidad territorial",
            "Está alineado de forma parcial con el diagnóstico integral de riesgos, amenazas y vulnerabilidad territorial",
            "El proyecto se encuentra totalmente alineado con el diagnóstico integral de riesgos y cuentan con un plan de prevención de riesgos y amenazas;  y está operando"
          ]
        },
        programa_contingencia_riesgo: {
          label: "b)\tSe tiene un programa de contingencia de riesgo detectado para el proyecto",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un programa de contingencia de riesgo",
            "Se reconoce la importancia de contar con un programa de contingencia de riesgo, pero no se realiza",
            "El proyecto cuenta con un programa de contingencia de riesgo, pero no se ejecuta regularmente (O: pero se ejecuta ocacionalmente)",
            "El proyecto cuenta con un programa de contingencia de riesgo, mismo que se ejecuta frecuentemente",
            "En caso de contingencia siempre se realizan las acciones del programa de contingencia"
          ]
        },
        participa_comites_proteccion_civil: {
          label: "Se participa de forma activa en los comités de protección civil",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de participar en los comités de protección civil",
            "Se reconoce la importancia de colaborar en los comités de protección civil pero no se participa",
            "El proyecto participa parcialmente en los comités de protección civil",
            "El proyecto participa frecuentemente en los comités de protección civil",
            "El proyecto siempre participa en los comités de protección civil"
          ]
        },
        fondo_ahorro_contingencia: {
          label: "Se cuenta con un fondo de ahorro para el uso exclusivo en caso de contingencia",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un fondo de ahorro exclusivo para contingencias",
            "Se reconoce la importancia de contar con un fondo de ahorro para el uso exclusivo ante alguna contingencia, pero no se implementa",
            "Existe un fondo de ahorro, pero no es exclusivo para contingencias",
            "Existe un fondo de ahorro exclusivo para la contingencia, pero se ha usado para otros fines",
            "Existe un fondo de ahorro exclusivo para la contingencia y siempre se usa para este fin"
          ]
        },
        programas_capacitacion_riesgo: {
          label: "El proyecto cuenta con programas de capacitación para minimizar los riesgos y vulnerabilidades",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con programas de capacitación para minimizar riesgos y vulnerabilidades",
            "Se reconoce la importancia de contar con programas de capacitación para minimizar riesgos y vulnerabilidades, pero no se cuenta con ellos",
            "Se cuenta con un programa de capacitación para minimizar riesgos y vulnerabilidades, que se realiza ocasionalmente",
            "Se cuenta con un programa de capacitación para minimizar riesgos y vulnerabilidades y se realiza frecuentemente",
            "Siempre se llevan a cabo las acciones del programa de capacitación que minimizan riesgos y vulnerabilidades"
          ]
        },
        monitoreo_gestion_riesgo: {
          label: "Se cuenta con un plan de evaluación y monitoreo del programa integral de riesgos y vulnerabilidades del territorio",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un plan de evaluación y monitoreo del programa integral de riesgos y vulnerabilidades del territorio",
            "Se reconoce la importancia de contar con un plan de evaluación y monitoreo del programa integral de riesgos y vulnerabilidades del territorio, pero no se ha generado",
            "El proyecto cuenta con un plan de evaluación y monitoreo del programa integral de riesgos y vulnerabilidades del territorio y se lleva a cabo ocasionalmente",
            "El proyecto cuenta con un plan de evaluación y monitoreo del programa de integral de riesgos y vulnerabilidades del territorio y se lleva a cabo frecuentemente",
            "Siempre se realizan las acciones del plan de evaluación y monitoreo del programa de integral de riesgos y vulnerabilidades del territorio"
          ]
        },
      },
      eval_produccion_social_ambiental_amigable: {
        aplica: false,
        insumos_bajo_impacto_ambiental: {
          label: "Para procesos productivos, se utilizan insumos de bajo impacto ambiental (orgánicos y locales)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de utilizar insumos de bajo impacto ambiental en los procesos productivos",
            "Se reconoce la importancia de manejar insumos de bajo impacto ambiental en los procesos productivos, pero no se llevan a cabo",
            "En ocasiones se utilizan insumos de bajo impacto ambiental para realizar procesos productivos",
            "Frecuentemente se utilizan insumos de bajo impacto ambiental para realizar procesos productivos",
            "Siempre se realizan acciones para el uso de insumos de bajo impacto ambiental en procesos productivos"
          ]
        },
        tecnologia_respetuosa_naturaleza: {
          label: "Las prácticas y tecnología empleada para la producción son respetuosas de la naturaleza y el ser humano (reciclaje de agua, conservación de suelos, etc.…)",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de utilizar tecnología respetuosa de la naturaleza y el ser humano.en los procesos productivos",
            "Se reconoce la importancia de prácticas y tecnología que sean respetuosas con la naturaleza y el ser humano, pero no utiliza este tipo de tecnología",
            "Ocasionalmente las prácticas y tecnología empleada para la producción son respetuosa de la naturaleza y el ser humano",
            "Frecuentemente las prácticas y tecnología empleada para la producción son respetuosa de la naturaleza y el ser humano",
            "Siempre se realizan acciones para que las prácticas y tecnología empleada para la producción sean respetuosas de la naturaleza y el ser humano"
          ]
        },
        respeta_saberes_locales: {
          label: "Los procesos de producción respetan los saberes locales incorporando tecnologías apropiadas",
          value: 0, options: [
            "No aplica",
            "En el proyecto no se reconoce la importancia de los saberes locales por lo tanto no incorpora tecnologías apropiadas",
            "Se reconoce la importancia de respetar los saberes locales incorporando tecnologías apropiadas para ello",
            "En ocasiones se incorporan tecnologías apropiadas que respetan los saberes locales",
            "Frecuentemente se incorporan tecnologías apropiadas que respetan los saberes locales",
            "Siempre se incorporan tecnologías apropiadas que respetan los saberes locales  "
          ]
        },
        privilegia_trabajo_local: {
          label: "Los procesos de producción y servicios privilegian el trabajo local",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de privilegiar el trabajo local",
            "El proyecto reconoce la importancia del trabajo local pero no lo incorpora",
            "El proyecto incorpora en algunos de sus procesos de producción el trabajo local",
            "El proyecto incorpora en la mayoría de sus procesos de producción el trabajo local",
            "El proyecto incorpora y privilegia en todos sus procesos de producción el trabajo local y está respaldado por un acuerdo entre los miembros del proyecto"
          ]
        },
        monitoreo_estrategias_produccion: {
          label: "Se cuenta con un plan de evaluación y monitoreo de las estrategias de producción para que sean social y ambientalmente amigables",
          value: 0, options: [
            "No aplica",
            "No se reconoce la importancia de contar con un plan de evaluación y monitoreo de las estrategias de producción para que sean social y ambientalmente amigables",
            "Se reconoce la importancia de contar con un plan de evaluación y monitoreo de las estrategias de producción para que sean social y ambientalmente amigables, pero no se ha elaborado",
            "El proyecto cuenta con un plan de evaluación y monitoreo de las estrategias de producción para que sean social y ambientalmente amigables y se lleva a cabo ocasionalmente",
            "El proyecto cuenta con un plan de evaluación y monitoreo de las estrategias de producción para que sean social y ambientalmente amigables y se lleva a cabo frecuentemente",
            "Siempre se realizan las acciones del plan de evaluación y monitoreo de las estrategias de producción para que sean social y ambientalmente amigables"
          ]
        },
      },
      eval_economia_social_solidaria: {
          aplica: false,
          cooperacion_colaboracion: {
            label: "En el proyecto los procesos de organización están basados en la cooperación y trabajo colaborativo",
            value: 0, options: [
              "No aplica",
              "No se reconoce la importancia de fomentar que los procesos de organización se base en la cooperación y trabajo colaborativo",
              "Se reconoce la importancia de procesos de organización basados en la cooperación y trabajo colaborativo, pero no se llevan a cabo",
              "Ocasionalmente los procesos de organización se basan en la cooperación y trabajo colaborativo",
              "Frecuentemente los procesos de organización se basan en la cooperación y trabajo colaborativo",
              "Los procesos siempre están basados en la cooperación y trabajo colaborativo",
            ]
          },
          intercambio_organizaciones: {
            label: "El proyecto privilegia intercambios entre organizaciones que practican los principios y valores de la economía social y solidaria",
            value: 0, options: [
              "No aplica",
              "No se reconoce la importancia de intercambios entre organizaciones que practican los principios y valores de la economía social y solidaria",
              "Se reconoce la importancia del intercambios entre organizaciones que practican los principios y valores de la economía social y solidaria, pero no se privilegian",
              "De forma ocasional se realiza el intercambio entre organizaciones que practican los principios y valores de la economía social y solidaria",
              "De forma frecuente se realiza el intercambio entre organizaciones que practican los principios y valores de la economía social y solidaria",
              "La organización siempre privilegia el intercambio entre organizaciones que practican los principios y valores de la economía social y solidaria",
            ]
          },
          intercambio_local: {
            label: "En el proyecto se privilegian los procesos de intercambio con los mercados locales (productores locales, artesanos locales)",
            value: 0, options: [
              "No aplica",
              "No se reconoce la importancia de privilegiar los procesos de intercambio con los mercados locales",
              "Se reconoce la importancia de privilegiar el intercambio con los mercados locales, pero no se realizan",
              "De forma ocasional se privilegia el intercambio con mercados locales",
              "De forma frecuente se privilegia el intercambio con mercados locales",
              "Siempre se privilegian procesos de intercambio con los mercados locales",
            ]
          },
          insumos_locales: {
            label: "En el proyecto los insumos y servicios son adquiridos con proveedores locales",
            value: 0, options: [
              "No aplica",
              "No se reconoce la importancia de adquirir insumos y servicios con proveedores locales",
              "Se reconoce la importancia pero los insumos no son adquiridos con proveedores locales",
              "De forma ocasional se adquieren insumos con proveedores locales",
              "De forma frecuente se adquieren insumos con proveedores locales",
              "Los  insumos y servicios siempre  son adquiridos con proveedores locales",
            ]
          },
          autonomia_financiera: {
            label: "Se cuenta con mecanismos que transiten hacia la autonomía financiera (cajas de ahorro, instituciones de ahorro y préstamo, etc. (Por ejemplo: tandas, préstamos, etc.)",
            value: 0, options: [
              "No aplica",
              "No se reconoce  la importancia de contar con mecanismos que transiten hacia la autonomía financiera",
              "Se reconoce la importancia de contar con mecanismos para transitar hacia una autonomía financiera, pero no se realizan",
              "Se cuenta con mecanismos no formales de autonomía financiera (tandas, préstamos familiares, etc)",
              "Están en proceso de planeación los mecanismos formales de transición hacia una autonomía financiera",
              "Se cuenta con un programa de mecanismos formales para una autonomía financiera",
            ]
          },
          economia_circular: {
            label: "Se fomenta la economía circular para aumentar el ciclo de vida de los desechos (emisiones de gases de efecto invernadero, materias primas, etc.)",
            value: 0, options: [
              "No aplica",
              "No se reconoce la importancia de fomentar la economía circular para aumentar el ciclo de vida de los desechos",
              "Se reconoce la importancia de fomentar la economía circular para reducir el ciclo de vida de los desechos, pero no se llevan a cabo acciones",
              "Se fomenta la economía circular, pero ocasionalmente se realizan acciones para aumentar el ciclo de vida de los desechos",
              "Se fomenta la economía circular y frecuentemente se realizan acciones para aumentar el ciclo de vida de los desechos",
              "Se tiene un programa para fomentar la economía circular para aumentar el ciclo de vida de los desechos,  se realiza su monitoreo y evaluación",
            ]
          },
          monitoreo_emprendimientos: {
            label: "Se cuenta con un plan de evaluación y monitoreo de los emprendimientos de economía social y solidaria",
            value: 0, options: [
              "No aplica",
              "No se reconoce la importancia de contar con un plan de evaluación y monitoreo de los emprendimientos de economía social y solidaria",
              "Se reconoce la importancia de contar con un plan de evaluación y monitoreo de los emprendimientos de economía social y solidaria, pero no se ha generado",
              "El proyecto cuenta con un plan de evaluación y monitoreo de los emprendimientos de economía social y solidaria y se lleva a cabo ocasionalmente",
              "El proyecto cuenta con un plan de evaluación y monitoreo de los emprendimientos de economía social y solidaria y se lleva a cabo frecuentemente",
              "Siempre se realizan las acciones del plan de evaluación y monitoreo de los emprendimientos de economía social y solidaria",
            ]
          },
        },
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
