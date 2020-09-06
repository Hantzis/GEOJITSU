<template>
  <div>
    <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd">
      <q-list padding>
        <q-item to="/" clickable v-ripple exact>
          <q-item-section avatar>
            <q-icon name="home"/>
          </q-item-section>

          <q-item-section>
            Inicio
          </q-item-section>

        </q-item>
        <q-item to="registros" clickable v-ripple>
          <q-item-section avatar>
            <q-icon name="mdi-file-edit"/>
          </q-item-section>

          <q-item-section>
            Registros
          </q-item-section>
        </q-item>

        <q-separator></q-separator>

        <q-item to="archivos" clickable v-ripple>
          <q-item-section avatar>
            <q-icon name="mdi-semantic-web"/>
          </q-item-section>
          <q-item-section>
            Archivos
          </q-item-section>
        </q-item>

        <q-item to="fondos" clickable v-ripple>
          <q-item-section avatar>
            <q-icon name="inbox"/>
          </q-item-section>

          <q-item-section>
            Fondos
          </q-item-section>
        </q-item>

        <q-item to="lugares" clickable v-ripple>
          <q-item-section avatar>
            <q-icon name="place"/>
          </q-item-section>

          <q-item-section>
            Lugares
          </q-item-section>
        </q-item>

        <q-item to="ramos" clickable v-ripple>
          <q-item-section avatar>
            <q-icon name="mdi-source-repository"/>
          </q-item-section>

          <q-item-section>
            Ramos
          </q-item-section>
        </q-item>
      </q-list>
    </q-scroll-area>
    <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
      <div class="absolute-bottom bg-transparent">
        <q-avatar size="56px" class="q-mb-sm">
          <img src="~assets/logo_unam.jpg" alt="UNAM">
        </q-avatar>
        <div class="text-weight-bold">Conflictos Socioambientales de México</div>
      </div>
    </q-img>
  </div>
</template>

<script>
export default {
  name: 'LeftMenu',
  props: ['left'],
  data() {
    return {
      leftMenu: false
    }
  }
}
</script>
