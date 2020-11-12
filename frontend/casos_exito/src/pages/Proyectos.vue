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
                      <!-- <q-btn v-if="auth_logged" dense round flat color="primary" @click="editRegistroDialog(props)"
                             icon="edit"></q-btn>
                      <q-btn v-if="auth_logged" dense round flat color="red" @click="deleteRegistroDialog(props)"
                             icon="delete"></q-btn> -->
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
                      <!-- <q-btn dense round disable flat color="accent"
                             :icon="props.expand ? 'edit' : 'add'"></q-btn>
                      <q-btn v-if="auth_logged" dense round flat color="primary" @click="editRegistroDialog(props)"
                             icon="edit"></q-btn> -->
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
          <q-avatar icon="mdi-chart-timeline" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar proyecto</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="closeAddProyectoDialog"/>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 86vh" class="scroll">
          <div class="q-py-xs">
            <p></p>
            <p>El proyecto o caso exitoso es aquel proceso de intervención que tiene claramente definidos sus
              <strong>objetivos, alcances, logros y metodologías de trabajo para la protección, conservación,
                restauración o usos sustentable de la naturaleza</strong>.</p>
            <p>Una organización podrá dar de alta un proyecto que abarque varias acciones o en su caso, varios
              proyectos si se considera pertinente. (ver instructivo para detalles)</p>
            <p></p>
          </div>
          <q-form ref="form_add" autocomplete="off" greedy>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="nombre_proyecto" v-model="proyecto_data.nombre_proyecto"
                       :rules="[val => !!val || 'Nombre del proyecto obligatorio']"
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
                         label="Fecha de inicio">
                  <template v-slot:default>
                    <q-popup-proxy ref="fecha_inicio" transition-show="scale" transition-hide="scale">
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
                         label="Fecha de registro a ONSSES">
                  <template v-slot:default>
                    <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                      <q-date v-model="proyecto_data.fecha_registro">
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
              <div class="col-3">
                <q-select
                  name="etapa"
                  label="Etapa"
                  outlined
                  v-model="proyecto_data.etapa"
                  :options="['Inicial', 'Intermedio', 'Consolidado']"
                  :rules="[val => !!val || 'Etapa obligatoria']"
                />
              </div>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="descripcion_proyecto"
                       v-model="proyecto_data.descripcion_proyecto"
                       :rules="[val => !!val || 'Descripción proyecto del proyecto obligatoria']"
                       type="textarea" rows="1" autogrow label="Descripción del proyecto"/>
            </div>
            <div class="row q-py-xs">
              <div class="col-3 q-pr-md">
                <q-select
                  name="escala"
                  label="Escala del proyecto"
                  outlined
                  v-model="proyecto_data.escala"
                  :options="['Nacional', 'Estatal', 'Municipal', 'Intermunicipal', 'Comunitaria/Local']"
                  :rules="[val => !!val || 'Género obligatorio']"
                />
              </div>
              <div class="col-3 q-pr-md">
                <q-select
                  name="estado"
                  label="Estado"
                  outlined
                  v-model="proyecto_data.estado"
                  :options="datos_estados"
                  emit-value
                  map-options
                  option-value="id"
                  option-label="nombre"
                  :rules="[val => !!val || 'Estado obligatorio']"
                />
              </div>
              <div class="col-3 q-pr-md">
                <q-select
                  name="municipio"
                  label="Municipio"
                  outlined
                  v-model="proyecto_data.municipio"
                  :options="datos_municipios"
                  emit-value
                  map-options
                  option-value="id"
                  option-label="nombre"
                  :rules="[val => !!val || 'Municipio obligatorio']"
                />
              </div>
              <div class="col-3">
                <q-input outlined class="full-width" name="localidad" v-model="proyecto_data.localidad"
                         :rules="[val => !!val || 'Localidad obligatoria']"
                         label="Localidad"/>
              </div>
            </div>
            <div class="row q-py-xs">
              <div class="col-6 q-pr-md">
                <q-input outlined name="domicilio_calle" v-model="proyecto_data.domicilio_calle"
                         :rules="[val => !!val || 'Domicilio obligatorio']"
                         label="Domicilio del proyecto (calle y número)"/>
              </div>
              <div class="col-4 q-pr-md">
                <q-input outlined name="domicilio_colonia" v-model="proyecto_data.domicilio_colonia"
                         :rules="[val => !!val || 'Colonia obligatoria']"
                         label="Colonia"/>
              </div>
              <div class="col-2">
                <q-input outlined name="codigo_postal" v-model="proyecto_data.codigo_postal"
                         :rules="[val => !!val || 'C. P. obligatorio']"
                         label="Código postal"/>
              </div>
            </div>
            <div class="row q-py-xs">
              <div class="col-4 q-pr-md">
                <q-input outlined class="full-width" name="telefono" v-model="proyecto_data.telefono"
                         :rules="[val => !!val || 'Teléfono obligatorio, 10 dígitos, solo números ']"
                         label="Teléfono (solo dígitos (10), sin espacios ni guiones)"/>
              </div>
              <div class="col-8">
                <q-input outlined class="full-width" name="email" v-model="proyecto_data.email"
                         :rules="[isValidEmail]"
                         label="Correo electrónico"/>
              </div>
            </div>
            <div class="row q-py-xs">
              <div class="col-6 q-pr-md">
                <q-input outlined class="full-width" name="representante" v-model="proyecto_data.representante"
                         :rules="[val => !!val || 'Representante obligatorio']"
                         label="Representante"/>
              </div>
              <div class="col-6 q-pr-md">
                <q-input outlined class="full-width" name="url" v-model="proyecto_data.url"
                         label="URL"/>
              </div>
            </div>
            <div class="row q-py-xs">
              <div class="col-6 q-pr-md">
                <q-select
                  name="tipo_organizacion"
                  label="Tipo de organización"
                  outlined
                  v-model="proyecto_data.tipo_organizacion"
                  :options="['Gubernamental federal', 'Gubernamental estatal', 'Gubernamental municipal',
                              'Organismo descentalizado', 'Organizaciones sociales (Comunitaria/Ejidal)',
                              'Organización productiva', 'Organización de la sociedad civil', 'Otra']"
                  :rules="[val => !!val || 'Tipo de organización obligatorio']"
                />
              </div>
              <div class="col-6 q-pr-md">
                <q-select
                  name="grupos_etnicos"
                  label="Grupos étnicos"
                  outlined
                  v-model="proyecto_data.grupos_etnicos"
                  :options="datos_grupos_etnicos"
                  emit-value
                  map-options
                  use-chips
                  multiple
                  option-value="id"
                  option-label="nombre"
                />
              </div>
            </div>
            <div class="row q-py-xs">
              <div class="col-2 q-pr-md items-center">
                <q-toggle
                  v-model="proyecto_data.inclusion_genero"
                  :label="proyecto_data.inclusion_genero ? 'Con inclusión de género' : 'Sin inclusión de género'"
                />
              </div>
              <div class="col-2 q-pr-md">
                <q-input
                  v-model.number="proyecto_data.numero_hombres" :min="0"
                  type="number" outlined label="Número de hombres en el proyecto"
                  :rules="[val => !!val || val === 0 || 'Número obligatorio, 0 si no hay']"
                />
              </div>
              <div class="col-2 q-pr-md">
                <q-input
                  v-model.number="proyecto_data.numero_mujeres" :min="0"
                  type="number" outlined label="Número de mujeres en el proyecto"
                  :rules="[val => !!val || val === 0 || 'Número obligatorio, 0 si no hay']"
                />
              </div>
              <div class="col-6 q-pr-md">
                <q-input
                  v-model="proyecto_data.estructura_gobierno"
                  outlined label="Estructura de gobierno"
                  :rules="[val => !!val || 'Estructura de gobierno obligatoria']"
                />
              </div>
            </div>
            <div class="row q-py-xs">
              <q-select
                class="full-width"
                name="rama_actividad_principal"
                label="Actividad económica principal"
                outlined
                v-model="proyecto_data.rama_actividad_principal"
                :options="datos_actividades_economicas"
                emit-value
                map-options
                option-value="id"
                option-label="nombre"
                :rules="[val => !!val || 'Actividad económica principal obligatorio']"
              />
            </div>
            <div class="row q-py-xs" style="margin-bottom: 10px">
              <q-select
                class="full-width"
                name="rama_actividad_secundaria"
                label="Actividad económica secundaria"
                outlined
                v-model="proyecto_data.rama_actividad_secundaria"
                :options="datos_actividades_economicas"
                emit-value
                map-options
                option-value="id"
                option-label="nombre"
              />
            </div>
            <div class="row q-py-md">
              <q-input outlined class="full-width" name="actividad_otra" v-model="proyecto_data.actividad_otra"
                       label="Otra actividad económica"/>
            </div>
            <div class="row q-py-xs">
              <div class="col-2">
                <q-btn label="Territorio" size="lg" icon="mdi-vector-polygon" no-caps color="grey-9"
                       @click="openTerritorioDialog()"/>
              </div>
              <div class="col-4 q-pr-md items-baseline">
                <q-input disable outlined v-model="proyecto_data.territorio" label="Coordenadas territorio"/>
              </div>
              <div class="col-2 q-pr-md items-baseline">
                <q-btn label="Ubicación" size="lg" class="full-width" icon="mdi-map-marker" no-caps color="grey-9"
                       @click="openUbicacionDialog()"/>
              </div>
              <div class="col-4 q-pr-md items-baseline">
                <q-input disable outlined v-model="proyecto_data.ubicacion" label="Coordenadas ubicación"/>
              </div>
            </div>
            <div class="row q-py-md">
              <q-input outlined class="full-width" name="area_influencia" v-model="proyecto_data.area_influencia"
                       label="Área de influencia" :rules="[val => !!val || 'Área de influencia obligatorio']"/>
            </div>
            <div class="row q-py-xs">
              <q-list bordered class="rounded-borders" style="width: 100%;">
                <q-expansion-item
                  expand-separator
                  label="Logros"
                >
                  <q-card>
                    <q-card-section>
                      <div class="row">
                        <div class="col" :align="'right'">
                          <q-btn no-caps color="green" @click="logroDialog = true">Agregar logro</q-btn>
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <q-list bordered separator>

                        <q-item clickable v-ripple v-for="(item, idx) in nuevos_logros" :key="idx">
                          <q-item-section>
                            <div class="row no-wrap justify-between">
                              <div class="col-11">
                                <span>{{ item.nombre }} ({{ item.fecha }})</span>
                              </div>
                              <div class="col-1 " style="text-align: right;">
                                <div class="row no-wrap">
                                  <!-- <q-btn flat dense @click.stop="console.log(22)" icon="edit" color="primary"></q-btn> -->
                                  <q-btn flat dense @click.stop="deleteLogro(idx)" icon="delete" color="red"></q-btn>
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
              <q-btn @click="closeAddProyectoDialog()" color="grey-7"
                     label="Cancelar" no-caps class=""/>
            </div>
            <div class="col-auto q-pl-xs">
              <q-btn @click="addProyecto()" color="green"
                     label="Guardar" no-caps class=""/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="territorioDialog" persistent>
      <q-card style="width: 600px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-vector-polygon" color="primary" text-color="white"/>
          <q-toolbar-title>Territorio</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="territorioDialog = false"/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <p>Suba un archivo de tipo GeoJSON.</p>
          <q-uploader
            style="width: 100%"
            url="https://onsses45.maptitude.xyz/api/v1/ce/subir-geojson/"
            label="Sólo archivo en formato GeoJSON"
            :headers="[{name: 'Authorization', value: `Bearer ${this.token}`}]"
            @uploaded="onUploaded"
            auto-upload
            :max-files="1"
            accept=".geojson, application/vnd.geo+json"
            @rejected="onRejectedGeoJSON"
          />
        </q-card-section>

        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="Cerrar" v-close-popup/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="ubicacionDialog" persistent>
      <q-card style="width: 600px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-map-marker" color="primary" text-color="white"/>
          <q-toolbar-title>Ubicación</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="closeUbicacionDialog()"/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div :key="mapkey">
            <vl-map ref="olmap" :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
                    data-projection="EPSG:4326" :style="{'min-height': 'inherit', 'width': '526px', 'height': '400px'}">
              <vl-view ref="olview" :zoom="5" :center="[-102, 20]"></vl-view>
              <vl-layer-tile id="osm">
                <vl-source-osm></vl-source-osm>
              </vl-layer-tile>


              <vl-layer-vector ref="vl-ubicacion">
                <vl-source-vector :features.sync="ubicacion" :ident="mapkey.toString()"></vl-source-vector>


                <vl-interaction-draw type="Point" :source="mapkey.toString()">
                  <vl-style-box>
                    <vl-style-stroke color="red"></vl-style-stroke>
                    <vl-style-fill color="rgba(255,255,255,0.9)"></vl-style-fill>
                  </vl-style-box>
                </vl-interaction-draw>

              </vl-layer-vector>

            </vl-map>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="Cerrar" @click="closeUbicacionDialog()"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="logroDialog" persistent>
      <q-card style="width: 600px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar logro</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="logroDialog = false"/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="nombre_logro" v-model="nuevo_logro.nombre"
                         :rules="[val => !!val || 'Nombre obligatorio']"
                         label="Nombre del logro"/>
              </div>
              <div class="row q-py-xs">
                <q-input outlined name="fecha_logro" v-model="nuevo_logro.fecha" class="full-width"
                         label="Fecha">
                  <template v-slot:default>
                    <q-popup-proxy ref="fecha_logro" transition-show="scale" transition-hide="scale">
                      <q-date v-model="nuevo_logro.fecha">
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
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="Cancelar" color="grey-8" @click="cancelarLogro()"/>
          <q-btn flat label="Agregar" @click="addLogro()"
                 :disable="nuevo_logro.nombre ==='' || nuevo_logro.fecha === ''"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="certificacionDialog" persistent>
      <q-card style="width: 600px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar certificación</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="certificacionDialog = false"/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="nombre_certificacion" v-model="nueva_certificacion.nombre"
                         :rules="[val => !!val || 'Nombre obligatorio']"
                         label="Nombre de la certificación"/>
              </div>
              <div class="row q-py-xs">
                <q-input outlined name="fecha_certificacion" v-model="nueva_certificacion.fecha" class="full-width"
                         label="Fecha">
                  <template v-slot:default>
                    <q-popup-proxy ref="fecha_certificacion" transition-show="scale" transition-hide="scale">
                      <q-date v-model="nueva_certificacion.fecha">
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
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="fuente_certificacion" v-model="nueva_certificacion.fuente"
                         :rules="[val => !!val || 'Fuente obligatoria']"
                         label="Fuente que certifica"/>
              </div>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="Cancelar" color="grey-8" @click="cancelarCertificacion()"/>
          <q-btn flat label="Agregar" @click="addCertificacion()"
                 :disable="nueva_certificacion.nombre ==='' || nueva_certificacion.fecha === '' || nueva_certificacion.fuente === ''"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="reconocimientoDialog" persistent>
      <q-card style="width: 600px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar reconocimiento</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="reconocimientoDialog = false"/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="nombre_reconocimiento" v-model="nuevo_reconocimiento.nombre"
                         :rules="[val => !!val || 'Nombre obligatorio']"
                         label="Nombre del reconocimiento"/>
              </div>
              <div class="row q-py-xs">
                <q-input outlined name="fecha_reconocimiento" v-model="nuevo_reconocimiento.fecha" class="full-width"
                         label="Fecha">
                  <template v-slot:default>
                    <q-popup-proxy ref="fecha_reconocimiento" transition-show="scale" transition-hide="scale">
                      <q-date v-model="nuevo_reconocimiento.fecha">
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
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="fuente_reconocimiento" v-model="nuevo_reconocimiento.fuente"
                         :rules="[val => !!val || 'Fuente obligatoria']"
                         label="Fuente que da el reconocimiento"/>
              </div>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="Cancelar" color="grey-8" @click="cancelarReconocimiento()"/>
          <q-btn flat label="Agregar" @click="addReconocimiento()"
                 :disable="nuevo_reconocimiento.nombre ==='' || nuevo_reconocimiento.fecha === '' || nuevo_reconocimiento.fuente === ''"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="redDialog" persistent>
      <q-card style="width: 600px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar red</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="redDialog = false"/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="nombre_red" v-model="nueva_red.nombre"
                         :rules="[val => !!val || 'Nombre obligatorio']"
                         label="Nombre de la red"/>
              </div>
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="integrantes_red" v-model="nueva_red.integrantes"
                         :rules="[val => !!val || 'Integrandes obligatorio']"
                         label="Integrantes de la red"/>
              </div>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="Cancelar" color="grey-8" @click="cancelarRed()"/>
          <q-btn flat label="Agregar" @click="addRed()"
                 :disable="nueva_red.nombre ==='' || nueva_red.integrantes === ''"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="financiamientoDialog" persistent>
      <q-card style="width: 600px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-plus" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar financiamiento</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="financiamientoDialog = false"/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="nombre_financiamiento" v-model="nuevo_financiamiento.nombre"
                         :rules="[val => !!val || 'Nombre obligatorio']"
                         label="Nombre del financiamiento"/>
              </div>
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="monto_financiamiento" v-model="nuevo_financiamiento.monto"
                         :rules="[val => !!val || 'Monto obligatorio']"
                         label="Monto del financiamiento"/>
              </div>
              <div class="row q-py-xs">
                <q-input outlined class="full-width" name="fuente_financiamiento" v-model="nuevo_financiamiento.fuente"
                         :rules="[val => !!val || 'Fuente obligatoria']"
                         label="Fuente del financiamiento"/>
              </div>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-teal">
          <q-btn flat label="Cancelar" color="grey-8" @click="cancelarFinanciamiento()"/>
          <q-btn flat label="Agregar" @click="addFinanciamiento()"
                 :disable="nuevo_financiamiento.nombre ==='' || nuevo_financiamiento.monto === '' || nuevo_financiamiento.fuente === ''"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script>
import axios from 'axios'
import cookies from 'browser-cookies'
import {mapGetters, mapActions} from 'vuex'
import Vue from 'vue'
import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css'
import {DrawInteraction} from 'vuelayers'


Vue.use(VueLayers)
Vue.use(DrawInteraction)


export default {
  name: 'casosExito',
  data() {
    return {
      filter: '',
      token: "",
      ubicacion: [],
      mapkey: 0,
      add_proyecto_dialog: false,
      territorioDialog: false,
      ubicacionDialog: false,
      logroDialog: false,
      certificacionDialog: false,
      reconocimientoDialog: false,
      redDialog: false,
      financiamientoDialog: false,
      proyecto_data: {inclusion_genero: false, fecha_inicio: "", fecha_registro: ""},
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
      datos_proyectos: undefined,
      datos_proyectos_mios: undefined,
      datos_estados: undefined,
      datos_municipios: undefined,
      datos_grupos_etnicos: undefined,
      datos_actividades_economicas: undefined,

      tabla_loading: true,
      tab: 'todos',
      estado_options: [],
      columnas: [
        {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true},
        {
          name: 'nombre_proyecto',
          align: 'left',
          label: 'Nombre de proyecto',
          field: 'nombre_proyecto',
          sortable: true
        },
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
          name: 'grupos_etnicos_display',
          align: 'left',
          label: 'Grupos étnicos',
          field: 'grupos_etnicos_display',
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
          name: 'rama_actividad_principal_display',
          align: 'left',
          label: 'Actividad económica principal',
          field: 'rama_actividad_principal_display',
          sortable: true
        },
        {
          name: 'rama_actividad_secundaria_display',
          align: 'left',
          label: 'Actividad económica secundaria',
          field: 'rama_actividad_secundaria_display',
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
      visible_columns: ['id', 'nombre_proyecto', 'fecha_inicio', 'etapa_display', 'escala_display', 'rama_actividad_principal_display', 'representante'],
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
    deleteLogro(val) {
      console.log(val)
      this.nuevos_logros.splice(val, 1)
    },
    deleteCertificacion(val) {
      console.log(val)
      this.nuevas_certificaciones.splice(val, 1)
    },
    deleteReconocimiento(val) {
      console.log(val)
      this.nuevos_reconocimientos.splice(val, 1)
    },
    deleteRed(val) {
      console.log(val)
      this.nuevas_redes.splice(val, 1)
    },
    deleteFinanciamiento(val) {
      console.log(val)
      this.nuevos_financiamientos.splice(val, 1)
    },
    onUploaded(evt) {
      console.log("uploaded", evt)
      console.log("response", evt.xhr.response)
      this.proyecto_data.territorio = evt.xhr.response
    },
    factoryGeoJSON(file) {
      this.token = cookies.get("access_token")
      console.log("file", file)

      let meh = new Promise((resolve, reject) => {
        // simulating a delay of 2 seconds
        resolve({url: 'https://onsses45.maptitude.xyz/api/v1/ce/subir-geojson/'})
      })
      meh.then(response => {
        console.log("aqui", response)
      })
      return meh
    },
    onRejectedGeoJSON(rejectedEntries) {
      // Notify plugin needs to be installed
      // https://quasar.dev/quasar-plugins/notify#Installation
      this.$q.notify({
        type: 'negative',
        message: `El archivo no es válido`
      })
    },
    closeAddProyectoDialog() {
      this.add_proyecto_dialog = false
      this.proyecto_data = {inclusion_genero: false, fecha_inicio: "", fecha_registro: ""}
    },
    isValidEmail(val) {
      if (val) {
        const emailPattern = /^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
        return emailPattern.test(val) || 'La dirección email no tiene formato correcto.';
      } else {
        return "Correo electrónico obligatorio"
      }
    },
    addProyecto() {
      this.token = cookies.get("access_token")
      this.proyecto_data.promovente = this.auth_user.pk
      this.$refs.form_add.validate().then(valid => {
        if (valid) {
          axios.post(`https://onsses45.maptitude.xyz/api/v1/ce/proyectos/`, this.proyecto_data,
            {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
            console.log(response.data)
            this.token = cookies.get("access_token")
            let proyecto_id = response.data.id
            if (this.nuevos_logros.length > 0) {
              this.nuevos_logros.forEach(item => {
                item.proyecto = proyecto_id
                axios.post(`https://onsses45.maptitude.xyz/api/v1/ce/logros/`, item,
                  {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
                  console.log(response.data)
                }).catch(error => console.log(error))
              })
            }
            if (this.nuevas_certificaciones.length > 0) {
              this.nuevas_certificaciones.forEach(item => {
                item.proyecto = proyecto_id
                axios.post(`https://onsses45.maptitude.xyz/api/v1/ce/certificaciones/`, item,
                  {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
                  console.log(response.data)
                }).catch(error => console.log(error))
              })
            }
            if (this.nuevos_reconocimientos.length > 0) {
              this.nuevos_reconocimientos.forEach(item => {
                item.proyecto = proyecto_id
                axios.post(`https://onsses45.maptitude.xyz/api/v1/ce/reconocimientos/`, item,
                  {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
                  console.log(response.data)
                }).catch(error => console.log(error))
              })
            }
            if (this.nuevas_redes.length > 0) {
              this.nuevas_redes.forEach(item => {
                item.proyecto = proyecto_id
                axios.post(`https://onsses45.maptitude.xyz/api/v1/ce/redes/`, item,
                  {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
                  console.log(response.data)
                }).catch(error => console.log(error))
              })
            }
            if (this.nuevos_financiamientos.length > 0) {
              this.nuevos_financiamientos.forEach(item => {
                item.proyecto = proyecto_id
                axios.post(`https://onsses45.maptitude.xyz/api/v1/ce/financiamientos/`, item,
                  {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
                  console.log(response.data)
                }).catch(error => console.log(error))
              })
            }
          }).catch(error => {
            console.log(error)
          }).finally(() => {
            this.add_proyecto_dialog = false
            this.proyecto_data = {inclusion_genero: false, fecha_inicio: "", fecha_registro: ""}
            this.nuevo_logro = {nombre: "", fecha: ""}
            this.nueva_certificacion = {nombre: "", fuente: "", fecha: ""}
            this.nuevo_reconocimiento = {nombre: "", fuente: "", fecha: ""}
            this.nueva_red = {nombre: "", integrantes: ""}
            this.nuevo_financiamiento = {nombre: "", fuente: "", monto: ""}
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    addLogro() {
      this.nuevos_logros.push(this.nuevo_logro)
      this.logroDialog = false
      this.nuevo_logro = {nombre: "", fecha: ""}
      console.log(this.nuevos_logros)
    },
    cancelarLogro() {
      this.logroDialog = false
      this.nuevo_logro = {nombre: "", fecha: ""}
    },
    addCertificacion() {
      this.nuevas_certificaciones.push(this.nueva_certificacion)
      this.certificacionDialog = false
      this.nueva_certificacion = {nombre: "", fuente: "", fecha: ""}
      console.log(this.nuevas_certificaciones)
    },
    cancelarCertificacion() {
      this.certificacionDialog = false
      this.nueva_certificacion = {nombre: "", fuente: "", fecha: ""}
    },
    addReconocimiento() {
      this.nuevos_reconocimientos.push(this.nuevo_reconocimiento)
      this.reconocimientoDialog = false
      this.nuevo_reconocimiento = {nombre: "", fuente: "", fecha: ""}
      console.log(this.nuevos_reconocimientos)
    },
    cancelarReconocimiento() {
      this.reconocimientoDialog = false
      this.nuevo_reconocimiento = {nombre: "", fuente: "", fecha: ""}
    },
    addRed() {
      this.nuevas_redes.push(this.nueva_red)
      this.redDialog = false
      this.nueva_red = {nombre: "", integrantes: ""}
      console.log(this.nuevas_redes)
    },
    cancelarRed() {
      this.redDialog = false
      this.nueva_red = {nombre: "", integrantes: ""}
    },
    addFinanciamiento() {
      this.nuevos_financiamientos.push(this.nuevo_financiamiento)
      this.financiamientoDialog = false
      this.nuevo_financiamiento = {nombre: "", fuente: "", monto: ""}
      console.log(this.nuevos_financiamientos)
    },
    cancelarFinanciamiento() {
      this.financiamientoDialog = false
      this.nuevo_financiamiento = {nombre: "", fuente: "", monto: ""}
    },
    closeUbicacionDialog() {
      this.ubicacionDialog = false
      console.log(this.ubicacion)
    },
    openTerritorioDialog() {
      this.token = cookies.get("access_token")
      this.territorioDialog = true
    },
    openUbicacionDialog() {
      this.ubicacion = []
      //this.ubicacion.splice(0,this.ubicacion.length)
      this.mapkey++
      console.log(this.mapkey)
      this.token = cookies.get("access_token")
      this.ubicacionDialog = true
    },
    getProyectos() {
      this.token = cookies.get("access_token")
      axios.get("https://onsses45.maptitude.xyz/api/v1/ce/proyectos/").then(response => {
        console.log("response proyectos: ", response.data)
        this.datos_proyectos = response.data
      }).then(() => {
        if (this.token) {
          axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/proyectos/?promovente=${this.auth_user.pk}`,
            {headers: {'Authorization': `Bearer ${this.token}`}}).then(response => {
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
    },
    getEstados() {
      axios.get("https://onsses45.maptitude.xyz/api/v1/ce/estados/").then(response => {
        console.log("estados: ", response.data)
        this.datos_estados = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    getMunicipios(estado) {
      if (estado) {
        axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/municipios/?estado=${estado}`).then(response => {
          console.log("datos_municipios: ", response.data)
          this.datos_municipios = response.data
        }).catch(error => {
          console.log(error)
        })
      }
    },
    getGruposEtnicos() {
      if (!this.datos_grupos_etnicos) {
        axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/grupos-etnicos/`).then(response => {
          console.log("datos_grupos_etnicos: ", response.data)
          this.datos_grupos_etnicos = response.data
        }).catch(error => {
          console.log(error)
        })
      }
    },
    getActividadesEconomicas() {
      if (!this.datos_actividades_economicas) {
        axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/ramas-actividades-economicas/`).then(response => {
          console.log("datos_actividades_economicas: ", response.data)
          this.datos_actividades_economicas = response.data
        }).catch(error => {
          console.log(error)
        })
      }
    }
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
        this.getProyectos()
        this.getEstados()
      })
    } else {
      this.getProyectos()
      this.getEstados()
    }
    this.getGruposEtnicos()
    this.getActividadesEconomicas()
  },
  watch: {
    ubicacion() {
      if (this.ubicacion.length > 1) {
        this.ubicacion.shift()
        const punto = "SRID=4326;POINT (" + this.ubicacion[0].geometry.coordinates[0] + " " + this.ubicacion[0].geometry.coordinates[1] + ")"
        console.log(punto)
        this.proyecto_data.ubicacion = punto
      }
    },
    'proyecto_data.estado': function (newVal, oldVal) {
      console.log(newVal)
      console.log(oldVal)
      this.getMunicipios(newVal)
    },
    'proyecto_data.fecha_inicio': function (newVal, oldVal) {
      this.proyecto_data.fecha_inicio = this.proyecto_data.fecha_inicio.split("/").join("-")
    },
    'proyecto_data.fecha_registro': function (newVal, oldVal) {
      this.proyecto_data.fecha_registro = this.proyecto_data.fecha_registro.split("/").join("-")
    },
    'nuevo_logro.fecha': function (newVal, oldVal) {
      this.nuevo_logro.fecha = this.nuevo_logro.fecha.split("/").join("-")
    },
    'nueva_certificacion.fecha': function (newVal, oldVal) {
      this.nueva_certificacion.fecha = this.nueva_certificacion.fecha.split("/").join("-")
    },
    'nuevo_reconocimiento.fecha': function (newVal, oldVal) {
      this.nuevo_reconocimiento.fecha = this.nuevo_reconocimiento.fecha.split("/").join("-")
    },
    'nueva_red.fecha': function (newVal, oldVal) {
      this.nueva_red.fecha = this.nueva_red.fecha.split("/").join("-")
    },
    'nuevo_financiamiento.fecha': function (newVal, oldVal) {
      this.nuevo_financiamiento.fecha = this.nuevo_financiamiento.fecha.split("/").join("-")
    },
  }
}
</script>

<style lang="css" scoped>
proyectos >>> .q-menu.q-position-engine.scroll {
  min-width: 0 !important;
}
</style>
