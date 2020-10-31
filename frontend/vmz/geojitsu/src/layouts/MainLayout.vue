<template>
  <q-layout view="LHH LPR FFF">
    <q-header class="bg-black text-white">
      <q-toolbar class="bg-pink text-white">
        <q-btn dense flat round icon="menu" @click="drawer_left = !drawer_left"/>

        <q-toolbar-title>
          Mapa VCM
        </q-toolbar-title>
        <q-btn v-if="this.$route.path==='/'" dense flat round
               :icon="showGISRibbon ? 'mdi-chevron-up' : 'mdi-chevron-down'"
               @click="showGISRibbon = !showGISRibbon">
          <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            {{ showGISRibbon ? "Ocultar cinta" : "Mostrar cinta" }}
          </q-tooltip>
        </q-btn>

        <q-btn dense flat round icon="mdi-dots-vertical">
          <q-menu content-style="border-radius: 2px;">
            <q-list style="min-width: 130px;">
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="info"/>
                </q-avatar>
                <q-item-section>Acerca de</q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="mdi-clippy"/>
                </q-avatar>
                <q-item-section>Ayuda</q-item-section>
              </q-item>
              <q-separator/>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="login"/>
                </q-avatar>
                <q-item-section>Ingresar</q-item-section>
              </q-item>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="logout"/>
                </q-avatar>
                <q-item-section>Salir</q-item-section>
              </q-item>
              <q-separator/>
              <q-item dense clickable v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="mdi-cog"/>
                </q-avatar>
                <q-item-section>Ajustes</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>

      <q-tabs align="right" no-caps class="bg-pink text-white" indicator-color="black">
        <q-route-tab to="/" label="Inicio"/>
        <q-route-tab to="/" label="Link 1"/>
        <q-route-tab to="/" label="Acerca de"/>
      </q-tabs>

    </q-header>

    <q-drawer v-model="drawer_left" side="left" elevated overlay behavior="mobile">
      <q-scroll-area style="height: calc(100% - 200px); margin-top: 200px; border-right: 1px solid #ddd">
        <q-list padding>
          <q-item to="/" clickable v-ripple exact>
            <q-item-section avatar>
              <q-icon name="home"/>
            </q-item-section>

            <q-item-section>
              Inicio
            </q-item-section>

          </q-item>

          <q-item to="/link" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-file-edit"/>
            </q-item-section>

            <q-item-section>
              Link 1
            </q-item-section>
          </q-item>

          <q-item to="/acerca-de" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="mdi-information"/>
            </q-item-section>

            <q-item-section>
              Acerca de
            </q-item-section>
          </q-item>


        </q-list>
      </q-scroll-area>
      <q-img class="absolute-top" src="~assets/material.png" style="height: 200px">

        <div v-if="auth_logged" class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img :src="get_gravatar(auth_user.email, 150)" :alt="auth_user.username">
          </q-avatar>
          <div class="text-weight-bold">
            {{
              auth_user.first_name === "" || auth_user.last_name === "" ? auth_user.username : auth_user.first_name + " "
                + auth_user.last_name
            }}
          </div>
          <div>
            <a style="cursor: pointer; margin-right: 8px;" @click="profile_dialog = true">Mi perfil</a> |
            <a style="cursor: pointer; margin-left: 8px;" @click="logout_dialog = true">Salir</a>
          </div>
        </div>
        <div v-else class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/logo_zapopan.png" alt="Zapopan">
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

    <q-dialog ref="login_dialog" v-model="login_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-login-variant" color="pink" text-color="white"/>
          <q-toolbar-title>Iniciar sesión</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
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
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="logout_dialog" v-model="logout_dialog">
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
    <q-dialog ref="resetpassword_dialog" v-model="resetpassword_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="pink" text-color="white"/>
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
    <q-dialog ref="resetpassworddone_dialog" v-model="resetpassworddone_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="pink" text-color="white"/>
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
    <q-dialog ref="profileupdated_dialog" v-model="profileupdated_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-user" color="pink" text-color="white"/>
          <q-toolbar-title>Actualización de datos</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <br/>
            <p>Se han actualizado sus datos.</p>
            <br/>
          </div>
          <div class="row">
            <div class="col">
              <q-btn @click="profileupdated_dialog = false" color="green"
                     label="Cerrar" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="profile_dialog" v-model="profile_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-account" color="pink" text-color="white"/>
          <q-toolbar-title>Perfil de usuario</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 50vh" class="scroll">
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
                     label="Email"/>
          </div>
          <div class="row q-py-xs">
            <q-input outlined class="full-width" name="fecha_nacimiento" v-model="full_user_data.fecha_nacimiento"
                     :rules="['date']"
                     label="Fecha de nacimiento">
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy ref="qDateProxy" transition-show="scale" mask="date" transition-hide="scale">
                    <q-date v-model="full_user_data.fecha_nacimiento">
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Cerrar" color="pink" flat/>
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>
          <div class="row q-py-xs" style="padding-bottom: 22px;">
            <q-select class="full-width" outlined v-model="full_user_data.sexo" clearable
                      :options="['Masculino', 'Femenino', 'Otro']" label="Sexo" />
          </div>
          <div class="row q-py-xs" style="padding-bottom: 22px;">
            <q-select class="full-width" outlined v-model="full_user_data.etnia" :options="etnias" label="Etnia"
              clearable emit-value map-options option-value="id" option-label="nombre" />
          </div>
          <div class="row q-py-xs" style="padding-bottom: 22px;">
            <q-select class="full-width" outlined v-model="full_user_data.municipio" :options="municipios" label="Municipio"
                      emit-value map-options option-value="id" option-label="nombre" />
          </div>
          <div class="row q-py-xs" style="padding-bottom: 22px;">
            <q-select class="full-width" outlined v-model="full_user_data.colonia" :options="colonias" label="Colonia"
                      emit-value map-options option-value="id" option-label="nombre" />
          </div>
          <div class="row q-py-xs" style="padding-bottom: 22px;">
            <q-select class="full-width" outlined v-model="full_user_data.discapacidades" :options="discapacidades"
                      multiple clearable use-chips label="Discapacidades" emit-value map-options option-value="id" option-label="nombre" />
          </div>


        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-btn @click="updateProfile()" color="green"
                     label="Actualizar datos" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-footer elevated class="bg-grey-10 text-grey-4">
      <q-toolbar style="min-height: 24px; font-size: 14px;">
        <span class="ellipsis">Consejo Municipal Contra Violencia Contra las Mujeres</span>
        <q-space/>
        <span class="no-wrap">
        <a style="text-decoration: none" class="text-grey-4 no-underline" href="https://saeba.click"
           target="_blank">2020&nbsp;&copy;&nbsp;saeba.click</a>
        </span>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
import md5 from 'crypto-md5';
import axios from 'axios'
import {mapGetters, mapActions} from 'vuex'
import cookies from 'browser-cookies'

export default {
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
      profileupdated_dialog: false,
      login_username: undefined,
      login_password: undefined,
      login_rememberme: false,
      reset_email: undefined,
      full_user_data: {username: undefined, first_name: undefined, last_name: undefined, email: undefined,
        is_staff: false, sexo: undefined, municipio: undefined, colonia: undefined, etnia: undefined,
        discapacidades: []
      },
      etnias: undefined,
      municipios: undefined,
      colonias: undefined,
      discapacidades: undefined,
    }
  },
  watch: {
    auth_user() {
      console.log("cambio")
      console.log(this.auth_user)
      this.getProfile(this.auth_user.pk)
    },
    'full_user_data.municipio': function (newVal, oldVal) {
      console.log(newVal)
      console.log(oldVal)
      this.getColonias(newVal)
    },
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter']),
    ...mapGetters('auth', ['logged', 'user']),
    auth_user: {
      get() {
        return this.user
      }
    },
    auth_logged: {
      get() {
        return this.logged
      }
    },
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      },
      set(value) {
        this.GISRibbonIsOpenAction(value)
      }
    }
  },
  methods: {
    ...mapActions('geojitsu', ['GISRibbonIsOpenAction']),
    ...mapActions('auth', ['setUser']),
    login() {
      this.$auth.attemptLogin(
        {
          username: this.login_username,
          password: this.login_password
        }, this.login_rememberme
      ).then(response => {
        console.log('You were logged in')
        this.login_dialog = false
        //this.auth_user = response
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
      axios.post("https://repvmz.maptitude.xyz/back/api/v1/auth/password/reset/", {email: this.reset_email})
        .then(response => {
          this.resetpassword_dialog = false
          this.resetpassworddone_dialog = true
        })
    },
    getEtnias() {
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/etnias/`).then(response => {
        this.etnias = response.data
        console.log("etnias", this.etnias)
      }).catch(error => console.log(error))
    },
    getMunicipios() {
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/municipios/`).then(response => {
        this.municipios = response.data
        console.log("municipios", this.municipios)
      }).catch(error => console.log(error))
    },
    getColonias(municipio) {
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/colonias/?municipio=${municipio}`).then(response => {
        this.colonias = response.data
        console.log("colonias", this.colonias)
      }).catch(error => console.log(error))
    },
    getDiscapacidades() {
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/discapacidades/`).then(response => {
        this.discapacidades = response.data
        console.log("discapacidades", this.discapacidades)
      }).catch(error => console.log(error))
    },
    getProfile(id) {
      const token = cookies.get("access_token")
      axios.get(`https://repvmz.maptitude.xyz/back/api/v1/usuarios-autenticado/${id}/`,
        {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
          console.log("getProfile");
          console.log(response);
          this.full_user_data.username = response.data.username
          this.full_user_data.first_name = response.data.first_name
          this.full_user_data.last_name = response.data.last_name
          this.full_user_data.email = response.data.email
          this.full_user_data.fecha_nacimiento = response.data.fecha_nacimiento
        console.log(this.full_user_data)
      }).catch(error => console.log(error))
    },
    updateProfile() {
      const token = cookies.get("access_token")
      axios.put(`https://repvmz.maptitude.xyz/back/api/v1/usuarios-registrado/${this.auth_user.pk}/`,
        this.full_user_data, {headers: {'Authorization': `Bearer ${token}`}})
        .then(response => {
          console.log(response);
          this.profile_dialog = false
          this.profileupdated_dialog = true
        })
    },
    get_gravatar(email, argsize) {
      let mail = "default@gravatar.com"
      if (email) {
        mail = email
      }
      return 'https://www.gravatar.com/avatar/' + md5(mail.trim().toLowerCase(), 'hex') + '.jpg?s=' + argsize;
    },
    testa(val) {
      alert(val);
    },
  },

  mounted() {
    if (this.auth_logged) {
      console.log("mount")
      this.$auth.refreshToken().then(response => {
        console.log("refreshToken")
        console.log(response)
      }).catch(error => console.log("no auth", error))
    }
    this.getMunicipios();
    this.getEtnias();
    this.getDiscapacidades();
  }
}
</script>

<style lang="css" scoped>
.q-drawer--right {
  z-index: 999;
  border-left: 1px solid rgba(0, 0, 0, 0.12);
}

.top-menu {
  border-radius: 0;
}
</style>
