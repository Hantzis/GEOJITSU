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
        <div v-if="usuario" class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img :src="get_gravatar(usuario.email, 150)" :alt="usuario.username">
          </q-avatar>
          <div class="text-weight-bold">
            {{
              usuario.first_name === "" || usuario.last_name === "" ? usuario.username : usuario.first_name + " " + usuario.last_name
            }}
          </div>
          <div>
            <a style="cursor: pointer; margin-right: 8px;" @click="open_profile_dialog = true">Mi perfil</a> |
            <a style="cursor: pointer; margin-left: 8px;" @click="open_logout_dialog = true">Salir</a>
          </div>
        </div>
        <div v-else class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/logo_unam.png" alt="ONSSES">
          </q-avatar>
          <div class="text-weight-bold">Anónimo</div>
          <div>
            <a style="cursor: pointer; margin-right: 8px;" @click="open_login_dialog = true">Ingresar</a> |
            <a style="cursor: pointer; margin-left: 8px;" @click="open_register_dialog = true">Registrar</a>
          </div>
        </div>
      </q-img>
    </q-drawer>


    <q-page-container>
      <router-view/>
    </q-page-container>

    <q-dialog ref="open_login_dialog" v-model="open_login_dialog" persistent>
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
                  <q-btn flat color="white" no-caps dense label="Restablecer contraseña"
                         @click.prevent="resetPassword()"/>
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
    <q-dialog ref="open_logout_dialog" v-model="open_logout_dialog">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="red" text-color="white"/>
          <q-toolbar-title>Cerrar sesión</q-toolbar-title>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row">
            <div class="col">
              <div class="row">
                <div class="col" style="min-width: 256px;">
                  <div class="row q-py-xs">
                    <div class="col">
                      <q-btn @click="logout()" no-caps color="red"
                             label="Salir" class="full-width"/>
                    </div>
                  </div>
                  <div class="row q-py-xs">
                    <div class="col">
                      <q-btn @click="open_logout_dialog=false" no-caps
                             label="Cancelar" class="full-width"/>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="login_dialog" v-model="open_resetpassword_dialog" persistent>
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
            <br/>
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
import md5 from 'crypto-md5';
import axios from 'axios'
import {mapGetters, mapActions} from 'vuex'

export default {
  components: {},
  data() {
    return {
      drawer_left: false,
      login_failure: false,
      open_login_dialog: false,
      open_logout_dialog: false,
      open_register_dialog: false,
      open_resetpassword_dialog: false,
      login_username: undefined,
      login_password: undefined,
      recover_username: undefined,
      recover_email: undefined,
    }
  },
  computed: {
    ...mapGetters('base', ['getKeyToken', 'getUsuario', 'getAccessToken', 'getRefreshToken']),
    keyToken: {
      get() {
        return this.getKeyToken
      },
      set(value) {
        this.setKeyToken(value)
      }
    },
    accessToken: {
      get() {
        return this.getAccessToken
      },
      set(value) {
        this.setAccessToken(value)
      }
    },
    refreshToken: {
      get() {
        return this.getRefreshToken
      },
      set(value) {
        this.setRefreshToken(value)
      }
    },
    authorization: {
      get() {
        return {headers: {"Authorization": `Bearer ${this.accessToken}`}}
      }
    },
    usuario: {
      get() {
        return this.getUsuario
      },
      set(value) {
        this.setUsuario(value)
      }
    }
  },
  methods: {
    ...mapActions('base', ['setKeyToken', 'setUsuario', 'setAccessToken', 'setRefreshToken']),
    login() {
      console.log("login")
      axios.post("https://onsses45.maptitude.xyz/api/v1/rest-auth/login/", {
        username: this.login_username,
        password: this.login_password
      }).then(response => {
        console.log("response: ", response)
        if (response.status === 200) {
          console.log("200: ", response.data['access_token'])
          this.accessToken = response.data.access_token
          this.refreshToken = response.data.refresh_token
          this.usuario = response.data.user
          this.open_login_dialog = false
          this.login_username = undefined
          this.login_password = undefined
        }
      }).catch(error => {
        this.login_failure = true
        console.log("error", error)
        console.log("response", error.response)
      })
    },
    resetPassword() {
      this.open_resetpassword_dialog = true
      this.open_login_dialog = false
      this.login_failure = false
    },
    get_gravatar(email, argsize) {
      const size = argsize
      return 'https://www.gravatar.com/avatar/' + md5(email.trim().toLowerCase(), 'hex') + '.jpg?s=' + size;
    },
  },
  watch: {
    open_login_dialog() {
      if (!this.open_login_dialog) {
        this.login_username = undefined
        this.login_password = undefined
      }
    },
    open_resetpassword_dialog() {
      if (!this.open_login_dialog) {
        this.recover_username = undefined
        this.login_password = undefined
      }
    },

  }
}
</script>


