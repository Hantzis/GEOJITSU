<template>
  <div class="col-auto">
    <div class="row">
      <div class="col">
        <div class="row q-pa-xs" style="padding-bottom: 12px;">
          <q-select outlined name="archivo" label="Capa activa" :options="capas" v-model="capa_activa">
            <template v-slot:prepend>
              <q-icon name="mdi-layers"/>
            </template>
          </q-select>

        </div>
      </div>
    </div>
    <div class="row justify-between">
      <div class="col-auto">
        <div class="row q-px-sm"/>
      </div>
      <div class="col-auto">
        Capas
      </div>
      <div class="col-auto">
        <q-btn dense size="xs" flat icon="mdi-arrow-bottom-right"
                 style="border-radius: 0; margin-bottom: -3px; margin-right: -1px;"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MapaBloqueCapas",
  data() {
    return {
      bloqueIsEnabled: false,
      capa_activa: '',
      capas: ["Estados", "Municipios", "Localidades", "Ejidos"]
    }
  },
  watch: {
    capa_activa() {
      console.log(this.capa_activa)
    }
  }
}
</script>

<style lang="css" scoped>

.bloque >>> .disabled,
.bloque >>> .disabled *,
.bloque >>> [disabled],
.bloque >>> [disabled] * {
  cursor: initial !important;
}

</style>
