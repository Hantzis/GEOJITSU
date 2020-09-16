<template>
  <q-layout view="lHh lpR fff">

    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left" />

        <q-toolbar-title>
          Casos de éxito ONSSES
        </q-toolbar-title>

        <q-btn dense flat round icon="mdi-cube" @click2="right = !right" />
      </q-toolbar>

      <q-tabs align="right" no-caps>
        <q-route-tab to="/" label="Inicio" />
        <q-route-tab to="/casos-exito" label="Casos de éxito" />
        <q-route-tab to="/acerca-de" label="Acerca de" />
      </q-tabs>
    </q-header>

    <q-drawer v-model="left" side="left" bordered elevated>
      <essential-link title="Title"/>
    </q-drawer>

    <q-drawer v-model="right" side="right" bordered>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import EssentialLink from "components/EssentialLink";
export default {
  components: {EssentialLink},
  data () {
    return {
      left: false,
      right: false
    }
  }
}
</script>


