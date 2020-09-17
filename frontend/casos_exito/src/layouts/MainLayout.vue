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
        <q-route-tab to="/proyectos" label="Proyectos" />
        <q-route-tab to="/evaluaciones" label="Evaluaciones" />
        <q-route-tab to="/casos-exito" label="Casos de éxito" />
        <q-route-tab to="/acerca-de" label="Acerca de" />
      </q-tabs>
    </q-header>

    <q-drawer
      v-model="left"
      side="left" bordered elevated
    >
      <q-scroll-area style="height: calc(100% - 142px); margin-top: 142px; border-right: 1px solid #ddd">
        <q-list padding>
          <q-item to="/" clickable v-ripple exact>
            <q-item-section avatar>
              <q-icon name="home"/>
            </q-item-section>
            <q-item-section>
              Inicio
            </q-item-section>
          </q-item>

          <q-item to="/proyectos" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-chart-timeline"/>
            </q-item-section>
            <q-item-section>
              Proyectos
            </q-item-section>
          </q-item>

          <q-item to="/evaluaciones" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-format-list-checks"/>
            </q-item-section>
            <q-item-section>
              Evaluaciones
            </q-item-section>
          </q-item>

          <q-item to="/casos-exito" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-checkbox-marked-outline"/>
            </q-item-section>
            <q-item-section>
              Casos de éxito
            </q-item-section>
          </q-item>

          <q-item to="/acerca-de" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="place"/>
            </q-item-section>
            <q-item-section>
              Acerca de
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>

      <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
        <div v-if="es_usuario" class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img :src="get_gravatar(usuario.email, 150)" :alt="usuario.displayName">
          </q-avatar>
          <div class="text-weight-bold">{{ usuario.displayName }}</div>
          <div>
            <a style="cursor: pointer; margin-right: 8px;" @click="open_dialog_profile = true">Mi perfil</a> |
            <a style="cursor: pointer; margin-left: 8px;" @click="open_dialog_logout = true">Salir</a>
          </div>
        </div>
        <div v-else class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/logo_unam.png" :alt="usuario.displayName">
          </q-avatar>
          <div class="text-weight-bold">Anónimo</div>
          <div>
            <a style="cursor: pointer;" @click="open_dialog_login = true">Iniciar sesión</a>
          </div>
        </div>
      </q-img>
    </q-drawer>


    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>

export default {
  components: {},
  data () {
    return {
      left: false,
      usuario: {},
    }
  }
}
</script>


