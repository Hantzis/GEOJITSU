<template>
  <q-page padding>
    <div class="row">
      <q-breadcrumbs>
        <q-breadcrumbs-el icon="home"/>
        <q-breadcrumbs-el label="Casos de éxito" icon="mdi-checkbox-marked-outline"/>
      </q-breadcrumbs>
    </div>
    <div class="row" style="padding-bottom: 10px;">
      <div class="col" :align="'right'">
        <q-btn color="primary" @click="getRamos()">
          <q-icon left dense size="2em" name="mdi-sync" style="margin-right: -10px; margin-left: -10px;"/>
        </q-btn>
        <q-btn no-caps v-if="!es_usuario" style="margin-left: 8px;" color="green" @click="addRamoDialog()">
          <q-icon left size="2em" name="mdi-plus"/>
          <div>Promover caso de éxito</div>
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
        <q-tab name="todos" label="Todos los casos"/>
        <q-tab name="dictaminados" label="Casos dictaminados por expertos"/>
        <q-tab name="pendientes" label="Casos pendientes de revisión"/>
        <q-tab name="mios" label="Casos promovidos por mí"/>
      </q-tabs>

      <q-separator/>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="todos">
          <div class="row">
            <div class="col">
              <q-table
                title="Todos los casos"
                :data.sync="datos_registros"
                :columns="columnas"
                :visible-columns="visible_columnas"
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
                    v-model="visible_columnas"
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
                      <q-btn dense round flat color="accent" @click="props.expand = !props.expand"
                             :icon="props.expand ? 'remove' : 'add'"></q-btn>
                      <q-btn v-if="es_usuario" dense round flat color="primary" @click="editRegistroDialog(props)"
                             icon="edit"></q-btn>
                      <q-btn v-if="es_usuario" dense round flat color="red" @click="deleteRegistroDialog(props)"
                             icon="delete"></q-btn>
                    </q-td>
                  </q-tr>
                  <q-tr v-show="props.expand" :props="props">
                    <q-td colspan="100%">
                      <div class="text-left">
                        <q-tr>
                          <q-td>Encabezado</q-td>
                          <q-td>
                            <q-tr>
                              <q-td style="height: initial; border-bottom-width: 0;">{{ props.row.encabezado }}</q-td>
                            </q-tr>
                          </q-td>
                        </q-tr>
                        <q-tr>
                          <q-td>Transcripción</q-td>
                          <q-td>
                            <q-tr>
                              <q-td style="height: initial; border-bottom-width: 0;">
                                <pre>{{ props.row.transcripcion }}</pre>
                              </q-td>
                            </q-tr>
                          </q-td>
                        </q-tr>
                        <q-tr>
                          <q-td>Observaciones</q-td>
                          <q-td>
                            <q-tr>
                              <q-td style="height: initial; border-bottom-width: 0;">
                                <pre>{{ props.row.observaciones }}</pre>
                              </q-td>
                            </q-tr>
                          </q-td>
                        </q-tr>
                        <q-tr v-if="es_usuario">
                          <q-td>Notas</q-td>
                          <q-td>
                            <q-tr>
                              <q-td style="height: initial; border-bottom-width: 0;">
                                <pre>{{ props.row.notas }}</pre>
                              </q-td>
                            </q-tr>
                          </q-td>
                        </q-tr>
                      </div>
                    </q-td>
                  </q-tr>
                </template>

              </q-table>
            </div>
          </div>


        </q-tab-panel>

        <q-tab-panel name="dictaminados">
          <div class="text-h6">Alarms</div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>

        <q-tab-panel name="pendientes">
          <div class="text-h6">Movies</div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
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
export default {
  name: 'casosExito',
  data() {
    return {
      tab: 'todos',
      columnas: [
        {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true},
        {name: 'archivo', align: 'left', label: 'Archivo', field: 'archivo', sortable: true},
        {name: 'fondo', align: 'left', label: 'Fondo', field: 'fondo', sortable: true},
        {name: 'tipo_documento', align: 'left', label: 'Tipo de documento', field: 'tipo_documento', sortable: true},
        {name: 'libro', align: 'left', label: 'Libro', field: 'libro', sortable: true},
        {name: 'foja', align: 'left', label: 'Foja', field: 'foja', sortable: true},
        {name: 'caja', align: 'left', label: 'Caja', field: 'caja', sortable: true},
        {name: 'expediente', align: 'left', label: 'Expediente', field: 'expediente', sortable: true},
        {name: 'años', align: 'left', label: 'Años', field: 'años', sortable: true},
        {name: 'lugar', align: 'left', label: 'Lugar', field: 'lugar', sortable: true},
        {name: 'ramo', align: 'left', label: 'Ramo', field: 'ramo', sortable: true},
        {name: 'encabezado', align: 'left', label: 'Encabezado', field: 'encabezado', sortable: true},
        {
          name: 'personas_involucradas',
          align: 'left',
          label: 'Personas involucradas',
          field: 'personas_involucradas',
          sortable: true
        },
        {name: 'transcripcion', align: 'left', label: 'Transcripcion', field: 'transcripcion', sortable: true},
        {name: 'observaciones', align: 'left', label: 'Observaciones', field: 'observaciones', sortable: true},
        {name: 'creacion', align: 'left', label: 'Creación', field: 'creacion', sortable: true},
        {name: 'crea', align: 'left', label: 'Crea', field: 'crea', sortable: true},
        {name: 'actualizacion', align: 'left', label: 'Actualización', field: 'actualizacion', sortable: true},
        {name: 'actualiza', align: 'left', label: 'Actualiza', field: 'actualiza', sortable: true},
      ],
      visible_columns: ['archivo', 'fondo', 'libro', 'foja', 'años', 'lugar', 'ramo', 'crea'],
    }
  }
}
</script>
