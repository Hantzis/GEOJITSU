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
        <div v-if="auth_logged" class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img :src="get_gravatar(auth_user.email, 150)" :alt="auth_user.username">
          </q-avatar>
          <div class="text-weight-bold">
            {{
              auth_user.first_name === "" || auth_user.last_name === "" ? auth_user.username : auth_user.first_name + " " + auth_user.last_name
            }}
          </div>
          <div>
            <a style="cursor: pointer; margin-right: 8px;" @click="profile_dialog = true">Mi perfil</a> |
            <a style="cursor: pointer; margin-left: 8px;" @click="logout_dialog = true">Salir</a>
          </div>
        </div>
        <div v-else class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/logo_unam.png" alt="ONSSES">
          </q-avatar>
          <div class="text-weight-bold">Anónimo</div>
          <div>
            <a style="cursor: pointer; margin-right: 8px;" @click="login_dialog = true">Ingresar</a> |
            <a style="cursor: pointer; margin-left: 8px;" @click="register_dialog = true">Registrar</a>
          </div>
        </div>
      </q-img>
    </q-drawer>


    <q-page-container>
      <router-view/>
    </q-page-container>

    <q-dialog ref="open_login_dialog" v-model="login_dialog" persistent>
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
            <div class="row q-pb-xs">
              <q-checkbox dense v-model="login_rememberme" label="Mantener sesión iniciada"/>

            </div>
            <br>
            <div v-if="login_failure" class="row q-py-xs" style="margin-bottom: 12px;">
              <q-banner class="text-white bg-red">
                Usuario o contraeña incorrectos. Verifique sus datos o restablezca su contraseña.
                <template v-slot:action>
                  <q-btn flat color="white" no-caps dense label="Restablecer contraseña"
                         @click.prevent="open_resetpassword_dialog()"/>
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
    <q-dialog ref="open_logout_dialog" v-model="logout_dialog">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="red" text-color="white"/>
          <q-toolbar-title>Cerrar sesión</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
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
                      <q-btn @click="logout_dialog=false" no-caps
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
    <q-dialog ref="login_dialog" v-model="resetpassword_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="primary" text-color="white"/>
          <q-toolbar-title>Recuperar contraseña</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <q-input outlined class="full-width" name="email" v-model="reset_email"
                     :rules="[isValidEmail]"
                     label="email"/>
          </div>
          <br/>
          <div class="row">
            <div class="col">
              <q-btn :disabled="!(isValidEmail(reset_email) === true)" @click="resetPassword()" color="green"
                     label="Enviar correo de recuperación" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="login_dialog" v-model="resetpassworddone_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="primary" text-color="white"/>
          <q-toolbar-title>Recuperar contraseña</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <br/>
            <p>Se ha envíado un link de recuperación a su correo electrónico.</p>
            <br/>
          </div>
          <div class="row">
            <div class="col">
              <q-btn @click="resetpassworddone_dialog = false" color="green"
                     label="Cerrar" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="login_dialog" v-model="profile_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="primary" text-color="white"/>
          <q-toolbar-title>Perfil de usuario</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <q-input disable outlined class="full-width" name="username" v-model="full_user_data.username"
                     :rules="[val => !!val || 'Username obligatorio']"
                     label="nombre de usuario"/>
          </div>
          <div class="row q-py-xs">
            <q-input outlined class="full-width" name="first_name" v-model="full_user_data.first_name"
                     :rules="[val => !!val || 'Nombre obligatorio']"
                     label="Nombre(s)"/>
          </div>
          <div class="row q-py-xs">
            <q-input outlined class="full-width" name="last_name" v-model="full_user_data.last_name"
                     :rules="[val => !!val || 'Apellidos obligatorio']"
                     label="Apellidos"/>
          </div>
          <div class="row q-py-xs">
            <q-input outlined class="full-width" name="email" v-model="full_user_data.email"
                     :rules="[isValidEmail]"
                     label="email"/>
          </div>
          <div class="row q-py-xs">
            <q-input outlined class="full-width" name="fecha_nacimiento" v-model="user_fecha_nacimiento"
                     :rules="['date']"
                     label="Fecha de nacimiento">
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy ref="qDateProxy" transition-show="scale" mask="date" transition-hide="scale">
                    <q-date v-model="user_fecha_nacimiento">
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Cerrar" color="primary" flat/>
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>
          <div class="row q-py-xs">
            <q-select
              outlined
              v-model="full_user_data.genero"
              :options="genero_options"
              option-value="value"
              option-label="label"
              emit-value
              map-options
              style="min-width: 328px; max-width: 328px"
              use-input
            />
          </div>
          <br/>
          <div class="row">
            <div class="col">
              <q-btn :disabled="(isValidEmail(reset_email) === true)" @click="resetPassword()" color="green"
                     label="Enviar correo de recuperación" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-layout>
</template>

<script>
import md5 from 'crypto-md5';
import axios from 'axios'
import {mapGetters, mapActions} from 'vuex'
import cookies from 'browser-cookies'

export default {
  components: {},
  data() {
    return {
      drawer_left: false,
      login_failure: false,
      login_dialog: false,
      logout_dialog: false,
      register_dialog: false,
      resetpassword_dialog: false,
      resetpassworddone_dialog: false,
      profile_dialog: false,
      login_username: undefined,
      login_password: undefined,
      login_rememberme: false,
      reset_email: undefined,
      full_user_data: {},
      user_fecha_nacimiento: undefined,
      genero_options: [{value: 'masculino', label: 'Masculino'}, {value: 'femenino', label: 'Femenino'}, {
        value: 'otro',
        label: 'Otro'
      }]
    }
  },
  computed: {
    ...mapGetters('base', ['getUserData']),
    ...mapGetters('auth', ['logged', 'user']),
    auth_user: {
      get() {
        console.log(this.user)
        return this.user
      }
    },
    auth_logged: {
      get() {
        return this.logged
      }
    },
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
    }
  },
  methods: {
    ...mapActions('base', ['setUserData']),
    login() {
      this.$auth.attemptLogin(
        {
          username: this.login_username,
          password: this.login_password
        }, this.login_rememberme
      ).then(response => {
        console.log('You were logged in')
        this.login_dialog = false
        this.auth_user = response
      }).catch(error => {
        console.log(error && error.response && error.response.status === 401
          ? 'Wrong e-mail or password'
          : 'Something went wrong'
        )
        this.login_failure = true
      })
    },
    logout() {
      this.$auth.logout(
      ).then(() => {
        console.log('You were logged out')
        this.logout_dialog = false
      }).catch(error => {
        console.log(error && error.response && error.response.status === 401
          ? 'Wrong e-mail or password'
          : 'Something went wrong'
        )
      })
    },
    open_resetpassword_dialog() {
      this.login_dialog = false
      this.resetpassword_dialog = true
      this.login_failure = false
      this.login_username = undefined
      this.login_password = undefined
    },
    isValidEmail(val) {
      const emailPattern = /^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
      return emailPattern.test(val) || 'La dirección email no tiene formato correcto.';
    },
    resetPassword() {
      axios.post("https://onsses45.maptitude.xyz/api/v1/rest-auth/password/reset/", {email: this.reset_email})
        .then(response => {
          this.resetpassword_dialog = false
          this.resetpassworddone_dialog = true
        })
    },
    get_gravatar(email, argsize) {
      let mail = "default@gravatar.com"
      if (email) {
        mail = email
      }
      return 'https://www.gravatar.com/avatar/' + md5(mail.trim().toLowerCase(), 'hex') + '.jpg?s=' + argsize;
    }
    ,
  },
  watch: {
    login_dialog() {
      if (!this.login_dialog) {
        this.login_username = undefined
        this.login_password = undefined
      }
    },
    resetpassword_dialog() {
      if (!this.resetpassword_dialog) {
        this.reset_email = undefined
      }
    },
    profile_dialog() {
      if (this.profile_dialog) {
        const token = cookies.get("access_token")
        axios.get(`https://onsses45.maptitude.xyz/api/v1/ce/usuarios-registrado/${this.auth_user.pk}/`,
          {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
          this.full_user_data = response.data
          if (this.full_user_data.fecha_nacimiento) {
            this.user_fecha_nacimiento = this.full_user_data.fecha_nacimiento.split("-").join('/')
          }
        }).catch(error => {
          console.log(error)
        })
      } else {
        this.full_user_data = {}
      }
    },
    user_fecha_nacimiento() {
      if (this.user_fecha_nacimiento) {
        this.full_user_data.fecha_nacimiento = this.user_fecha_nacimiento.split("/").join('-')
      }
    }
  }
}
</script>


