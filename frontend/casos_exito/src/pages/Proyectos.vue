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
          <q-avatar icon="mdi-chart-timeline" color="primary" text-color="white"/>
          <q-toolbar-title>Agregar proyecto</q-toolbar-title>
          <q-btn icon="close" flat round dense @click="closeAddProyectoDialog"/>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 86vh" class="scroll">
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
                          <q-btn color="green">Agregar logro</q-btn>
                        </div>
                      </div>
                    </q-card-section>
                    <q-card-section>
                      <q-list bordered separator>
                        <q-item clickable v-ripple>
                          <q-item-section>Single line item</q-item-section>
                        </q-item>

                        <q-item clickable v-ripple>
                          <q-item-section>
                            <q-item-label>Item with caption</q-item-label>
                            <q-item-label caption>Caption</q-item-label>
                          </q-item-section>
                        </q-item>

                        <q-item clickable v-ripple>
                          <q-item-section>
                            <q-item-label overline>OVERLINE</q-item-label>
                            <q-item-label>Item with caption</q-item-label>
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
                      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
                      commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
                      eveniet doloribus ullam aliquid.
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
                      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
                      commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
                      eveniet doloribus ullam aliquid.
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
                      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
                      commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
                      eveniet doloribus ullam aliquid.
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
                      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
                      commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
                      eveniet doloribus ullam aliquid.
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
      proyecto_data: {inclusion_genero: false},
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
      this.proyecto_data = {inclusion_genero: false}
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
      const token = cookies.get("access_token")
      this.proyecto_data.promovente = this.auth_user.pk
      this.$refs.form_add.validate().then(valid => {
        if (valid) {
          axios.post(`https://onsses45.maptitude.xyz/api/v1/ce/proyectos/`, this.proyecto_data,
            {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
            console.log(response.data)
            this.add_proyecto_dialog = false
          }).catch(error => {
            console.log(error)
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
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
    const token = cookies.get("access_token")
    if (token) {
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
    }
  }
}
</script>

<style lang="css" scoped>
proyectos >>> .q-menu.q-position-engine.scroll {
  min-width: 0 !important;
}
</style>
