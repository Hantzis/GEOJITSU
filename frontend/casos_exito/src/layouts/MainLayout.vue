<template>
  <q-layout view="lHh lpR fff">

    <q-header elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="drawer_left = !drawer_left"/>

        <q-toolbar-title>
          Casos de éxito ONSSES
        </q-toolbar-title>

        <q-btn dense flat round icon="mdi-cube" @click2="right = !right"/>
      </q-toolbar>

      <q-tabs align="right" no-caps>
        <q-route-tab to="/" label="Inicio"/>
        <q-route-tab to="/proyectos" label="Proyectos"/>
        <q-route-tab to="/evaluaciones" label="Evaluaciones"/>
        <q-route-tab to="/casos-exito" label="Casos de éxito"/>
        <q-route-tab to="/acerca-de" label="Acerca de"/>
      </q-tabs>
    </q-header>

    <q-drawer
      v-model="drawer_left"
      side="left" elevated
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
            <a style="cursor: pointer;" @click="login_dialog = true">Ingresar</a> | <a style="cursor: pointer;"
                @click="register_dialog = true">Registrar</a>
          </div>
        </div>
      </q-img>
    </q-drawer>


    <q-page-container>
      <router-view/>
    </q-page-container>

    <q-dialog ref="login_dialog" v-model="login_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-login-variant" color="primary" text-color="white"/>
          <q-toolbar-title>Iniciar sesión</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <q-form>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="username"
                       :rules="[val => !!val || 'Falta nombre de usuario']"
                       v-model="login_username" label="Usuario"/>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="password" v-model="login_password" type="password"
                       :rules="[val => !!val || 'Falta contraseña']"
                       label="Contraseña"/>
            </div>
            <div v-if="login_failure" class="row q-py-xs" style="margin-bottom: 12px;">
              <q-banner class="text-white bg-red">
                Usuario o contraeña incorrectos. Verifique sus datos o restablezca su contraseña.
                <template v-slot:action>
                  <q-btn flat color="white" no-caps dense label="Restablecer contraseña" @click.prevent="resetPassword()"/>
                </template>
              </q-banner>
            </div>
            <div class="row">
              <div class="col">
                <q-btn :disabled="!login_username || !login_password" @click="login()" color="green"
                       label="Ingresar" no-caps class="full-width"/>
              </div>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="login_dialog" v-model="recoverpassword_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="primary" text-color="white"/>
          <q-toolbar-title>Recuperar contraseña</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <q-form>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="username"
                       :rules="[val => !!val || 'Falta nombre de usuario']"
                       v-model="recover_username" label="Usuario"/>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="email" v-model="recover_email"
                       :rules="[val => !!val || 'Falta email']"
                       label="email"/>
            </div>
            <br />
            <div class="row">
              <div class="col">
                <q-btn :disabled="!recover_username || !recover_email" @click="login()" color="green"
                       label="Enviar a mi email" no-caps class="full-width"/>
              </div>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-layout>
</template>

<script>
import axios from 'axios'

export default {
  components: {},
  data() {
    return {
      drawer_left: false,
      login_dialog: false,
      login_failure: false,
      register_dialog: false,
      recoverpassword_dialog: false,
      usuario: {},
      login_username: undefined,
      login_password: undefined,
      recover_username: undefined,
      recover_email: undefined,
      es_usuario: false,
    }
  },
  methods: {
    login() {
      console.log("login")
      axios.post("https://onsses45.maptitude.xyz/api/v1/rest-auth/login/",
        {username: this.login_username, password: this.login_password}).then(response => {
          console.log("reponse: ", response)
          console.log("reponse.status: ", response.status)
          console.log("reponse.data: ", response.data)
      }).catch(error  => {
        this.login_failure = true
        console.log("msg", error.response)
        console.log("status", error.response.status)
      })
    },
    resetPassword() {

      this.recoverpassword_dialog = true
      this.login_dialog = false
      this.login_failure = false
    }
  },
  watch: {
    login_dialog() {
      if (!this.login_dialog) {
        this.login_username = undefined
        this.login_password = undefined
      }
    },
    recoverpassword_dialog() {
      if (!this.login_dialog) {
        this.recover_username = undefined
        this.login_password = undefined
      }
    },

  }
}
</script>


