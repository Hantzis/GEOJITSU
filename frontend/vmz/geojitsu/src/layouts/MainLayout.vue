<template>
  <q-layout view="LHH LPR FFF">
    <q-header class="bg-black text-white">
      <q-toolbar class="text-white" style="background-color: #8564c8;">
        <q-btn dense flat round icon="menu" @click="drawer_left = !drawer_left"/>

        <q-toolbar-title>
          Ciudad÷Nosotras
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
            <q-list style="min-width: 190px;">

              <q-item v-if="!auth_logged" dense clickable v-close-popup style="padding: 0;" @click="openLogin()">
                <q-avatar>
                  <q-icon name="login"/>
                </q-avatar>
                <q-item-section>Ingresar</q-item-section>
              </q-item>
              <q-item v-else dense clickable v-close-popup style="padding: 0;" @click="logout_dialog = true">
                <q-avatar>
                  <q-icon name="logout"/>
                </q-avatar>
                <q-item-section>Salir</q-item-section>
              </q-item>
              <q-item v-if="!auth_logged" dense clickable v-close-popup style="padding: 0;"
                      @click="create_account_dialog = true">
                <q-avatar>
                  <q-icon name="mdi-account-plus"/>
                </q-avatar>
                <q-item-section>Crear cuenta</q-item-section>
              </q-item>
              <q-item v-if="auth_logged" dense clickable v-close-popup style="padding: 0;"
                      @click="profile_dialog = true">
                <q-avatar>
                  <q-icon name="mdi-account"/>
                </q-avatar>
                <q-item-section>Mi perfil</q-item-section>
              </q-item>
              <q-separator/>

              <q-item v-for="pagina of paginas.items" :to="'/v/' + pagina.meta.slug" :key="pagina.id" dense clickable
                      v-close-popup style="padding: 0;">
                <q-avatar>
                  <q-icon name="info"/>
                </q-avatar>
                <q-item-section>{{ pagina.title }}</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
      <q-tabs align="right" no-caps class="text-white" indicator-color="cyan-4" style="background-color: #8564c8;">
        <q-route-tab to="/" label="Inicio"/>
        <q-route-tab v-for="pagina of paginas.items" :to="'/v/' + pagina.meta.slug" :label="pagina.title"
                     :key="pagina.id"/>
      </q-tabs>
    </q-header>
    <q-drawer v-model="drawer_left" side="left" elevated overlay behavior="mobile">
      <q-scroll-area style="height: calc(100% - 260px); margin-top: 260px; border-right: 1px solid #ddd">
        <div class="column fit justify-between" :style="{'min-height': drawerHeight}">
          <div class="col-auto">
            <q-list padding>
              <q-item to="/" clickable v-ripple exact>
                <q-item-section avatar>
                  <q-icon name="home"/>
                </q-item-section>

                <q-item-section>
                  Inicio
                </q-item-section>
              </q-item>

              <q-item v-for="pagina of paginas.items" :to="'/v/' + pagina.meta.slug" :key="pagina.id" clickable
                      v-ripple>
                <q-item-section avatar>
                  <q-icon name="mdi-information"/>
                </q-item-section>
                <q-item-section>
                  {{ pagina.title }}
                </q-item-section>
              </q-item>
            </q-list>
          </div>
          <div class="col-auto q-py-xs">
            <q-separator/>
            <div class="row justify-center q-pt-sm">
              <div class="col text-center">
                <img src="statics/logos_principal.png">
              </div>
            </div>
          </div>
        </div>
      </q-scroll-area>
      <q-img class="absolute-top" src="~assets/material.png" style="height: 260px">
        <div v-if="auth_logged" class="bg-transparent">
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
        <div v-else class="bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="~assets/logo_mujeres.png" alt="Zapopan">
          </q-avatar>
          <div class="text-weight-bold">Anónimo</div>
          <div>
            <a style="cursor: pointer; margin-right: 8px;" @click="openLogin()">Ingresar</a> |
            <a style="cursor: pointer; margin-left: 8px;" @click="create_account_dialog = true">Crear cuenta</a>
          </div>
        </div>
        <div class="absolute-bottom bg-transparent">
          <div class="text-right" style="font-size: 20px; font-weight: 300;">Ciudad÷nosotras</div>
          <div class="text-right" style="font-size: 16px; font-weight: 300;">Zapopan para nosotras</div>
          <p style="margin-bottom: 2px; margin-top: 12px;">Instituto Municipal de las Mujeres Zapopanas para la Igualdad
            Sustantiva</p>
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
          <div class="row q-py-xs" style="margin-bottom: 12px;">
            <q-input outlined class="full-width" name="password" v-model="login_password"
                     :type="isPwd ? 'password' : 'text'"
                     :rules="[val => !!val || 'Falta contraseña']" label="Contraseña">
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
          </div>
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
          <div class="row full-width">
            <div class="col full-width">
              <q-btn @click="logout()" no-caps color="red"
                     label="Salir" class="full-width"/>
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
          <q-form ref="form_profile" autocomplete="off" greedy>
            <div class="row q-py-xs">
              <q-input disable outlined class="full-width" name="username" v-model="full_user_data.username"
                       :rules="[val => !!val || 'Username obligatorio']"
                       label="Nombre de usuario"/>
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
              <q-input outlined class="full-width" mask="date"
                       name="user_fecha_nacimiento" v-model="user_fecha_nacimiento"
                       label="Fecha de nacimiento" :rules="[val => !!val || 'Fecha de nacimiento obligatoria']">

                <template v-slot:default>
                  <q-popup-proxy ref="qDateProxy" transition-show="scale" mask="date" transition-hide="scale">
                    <q-date v-model="user_fecha_nacimiento">
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Cerrar" color="primary" flat/>
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </template>
                <template v-slot:append>
                  <q-icon name="event"/>
                </template>
              </q-input>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 22px;">
              <q-select class="full-width" outlined v-model="full_user_data.sexo"
                        :options="['Femenino', 'Masculino', 'Otro']" label="Sexo"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 22px;">
              <q-select class="full-width" outlined v-model="full_user_data.etnia" :options="etnias" label="Etnia"
                        clearable emit-value map-options option-value="id" option-label="nombre"/>
            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined v-model="full_user_data.municipio" :options="municipios"
                        label="Municipio" :rules="[val => !!val || 'Municipio obligatorio']"
                        emit-value map-options option-value="id" option-label="nombre"/>
            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined v-model="full_user_data.colonia" :options="colonias" label="Colonia"
                        emit-value map-options option-value="id" option-label="nombre"
                        :rules="[val => !!val || 'Colonia obligatoria']"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 22px;">
              <q-select class="full-width" outlined v-model="full_user_data.discapacidades" :options="discapacidades"
                        multiple clearable use-chips label="Discapacidades" emit-value map-options option-value="id"
                        option-label="nombre"/>
            </div>

            <div class="row q-py-xs" style="margin-bottom: 12px;">
              <q-banner class="text-white bg-info">
                Si desea cambiar su contraseña, de click en el botón 'Cambiar contraseña'.
                <template v-slot:action>
                  <q-btn outline color="white" no-caps dense label=" Cambiar contraseña "
                         @click.prevent="open_changepassword_dialog()"/>
                </template>
              </q-banner>
            </div>
          </q-form>
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
    <q-dialog ref="changepassword_dialog" v-model="changepassword_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-key-variant" color="pink" text-color="white"/>
          <q-toolbar-title>Cambiar contraseña</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <q-input :type="isPwd ? 'password' : 'text'" outlined class="full-width" name="new_password1"
                     v-model="old_password"
                     :rules="[val => !!val || 'Falta contraseña actual']"
                     label="Contraseña actual">
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
          </div>
          <div class="row q-py-xs">
            <q-input :type="isPwd ? 'password' : 'text'" outlined class="full-width" name="new_password1"
                     v-model="new_password1"
                     :rules="[val => !!val || 'Falta contraseña nueva']"
                     label="Nueva contraseña">
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
          </div>
          <div class="row q-py-xs">
            <q-input :type="isPwd ? 'password' : 'text'" outlined class="full-width" name="new_password2"
                     v-model="new_password2"
                     :rules="[val => !!val || 'Falta contraseña de confirmación']"
                     label="Confirmar contraseña nueva">
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
          </div>
          <div v-if="new_password1 && new_password2 && new_password1 != new_password2" class="row q-px-xs">
            <p class="text-red">Las contraseñas no coinciden</p>
          </div>
          <br/>
          <div class="row">
            <div class="col">
              <q-btn :disabled="!old_password || !new_password1 || !new_password2 || new_password1 != new_password2"
                     @click="changePassword()" color="green"
                     label="Cambiar contraseña" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="create_account_dialog" v-model="create_account_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-account" color="pink" text-color="white"/>
          <q-toolbar-title>Crear cuenta</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup @click="cleanRegisterForm()"/>
        </q-card-section>
        <q-separator/>
        <q-card-section style="max-height: 50vh" class="scroll">
          <q-form ref="form_register" autocomplete="off" greedy>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="username" v-model="new_user_data.username"
                       :rules="[val => !!val || 'Username obligatorio']"
                       :error="usernameExists"
                       error-message="El nombre de usuario ya existe"
                       label="nombre de usuario"/>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="first_name" v-model="new_user_data.first_name"
                       :rules="[val => !!val || 'Nombre obligatorio']"
                       label="Nombre(s)"/>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="last_name" v-model="new_user_data.last_name"
                       :rules="[val => !!val || 'Apellidos obligatorio']"
                       label="Apellidos"/>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" name="email" v-model="new_user_data.email"
                       :rules="[isValidEmail]"
                       label="Email"/>
            </div>
            <div class="row q-py-xs">
              <q-input outlined class="full-width" mask="date"
                       name="user_fecha_nacimiento" v-model="user_fecha_nacimiento"
                       label="Fecha de nacimiento" :rules="[val => !!val || 'Fecha de nacimiento obligatoria']">

                <template v-slot:default>
                  <q-popup-proxy ref="qDateProxy" transition-show="scale" mask="date" transition-hide="scale">
                    <q-date v-model="user_fecha_nacimiento">
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Cerrar" color="primary" flat/>
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </template>
                <template v-slot:append>
                  <q-icon name="event"/>
                </template>
              </q-input>
            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined v-model="new_user_data.sexo"
                        :rules="[val => !!val || 'Sexo obligatorio']"
                        :options="['Femenino', 'Masculino', 'Otro']" label="Sexo"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 22px;">
              <q-select class="full-width" outlined v-model="new_user_data.etnia" :options="etnias" label="Etnia"
                        clearable emit-value map-options option-value="id" option-label="nombre"/>
            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined v-model="new_user_data.municipio" :options="municipios"
                        label="Municipio" :rules="[val => !!val || 'Municipio obligatorio']"
                        emit-value map-options option-value="id" option-label="nombre"/>
            </div>
            <div class="row q-py-xs">
              <q-select class="full-width" outlined v-model="new_user_data.colonia" :options="colonias" label="Colonia"
                        emit-value map-options option-value="id" option-label="nombre"
                        :rules="[val => !!val || 'Colonia obligatoria']"/>
            </div>
            <div class="row q-py-xs" style="padding-bottom: 22px;">
              <q-select class="full-width" outlined v-model="new_user_data.discapacidades" :options="discapacidades"
                        multiple clearable use-chips label="Discapacidades" emit-value map-options option-value="id"
                        option-label="nombre"/>
            </div>
            <div class="row q-py-xs">
              <q-input :type="isPwd ? 'password' : 'text'" outlined class="full-width" name="password1"
                       v-model="new_user_data.password1"
                       :rules="[val => !!val || 'Falta contraseña', val => val.length >= 8 || 'Mínimo 8 caracteres']"
                       label="Contraseña">
                <template v-slot:append>
                  <q-icon
                    :name="isPwd ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="isPwd = !isPwd"
                  />
                </template>
              </q-input>
            </div>
            <div class="row q-py-xs">
              <q-input :type="isPwd ? 'password' : 'text'" outlined class="full-width" name="password2"
                       v-model="new_user_data.password2"
                       :rules="[val => !!val || 'Falta confirmación de contraseña', val => val.length >= 8 || 'Mínimo 8 caracteres']"
                       label="Confirmar contraseña">
                <template v-slot:append>
                  <q-icon
                    :name="isPwd ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="isPwd = !isPwd"
                  />
                </template>
              </q-input>
            </div>
            <div
              v-if="new_user_data.password1 && new_user_data.password2 && new_user_data.password1 != new_user_data.password2"
              class="row q-px-xs">
              <p class="text-red">Las contraseñas no coinciden</p>
            </div>
            <br/>

          </q-form>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row">
            <div class="col">
              <q-btn @click="createAccount()" color="green"
                     :disabled="!new_user_data.password1 || !new_user_data.password2 || new_user_data.password1 != new_user_data.password2"
                     label="Crear cuenta" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
    <q-dialog ref="accountcreated_dialog" v-model="accountcreated_dialog" persistent>
      <q-card style="width: 360px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-info" color="pink" text-color="white"/>
          <q-toolbar-title>Cuenta creada</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section>
          <div class="row q-py-xs">
            <br/>
            <p>Su cuenta se ha creado con éxito y se ha iniciado sesión.</p>
            <br/>
          </div>
          <div class="row">
            <div class="col">
              <q-btn @click="accountcreated_dialog = false" color="green"
                     label="Aceptar" no-caps class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog style="width: 1000px" ref="bienvenida_dialog" v-model="bienvenida_dialog">
      <q-card style="width: 1000px">
        <q-card-section class="row items-center">
          <q-avatar icon="mdi-home" color="red" text-color="white"/>
          <q-toolbar-title>Ciudad÷Nosotras</q-toolbar-title>
          <q-btn icon="close" flat round dense v-close-popup/>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <div v-for="block of homeData.contenido" :key="block.id">
                <div v-if="block.type === 'image'">
                  <div v-html="block.value"></div>
                </div>
                <div v-if="block.type === 'paragraph'">
                  <span v-html="block.value"></span>
                </div>
                <div v-if="block.type === 'title'">
                  <h5>{{ block.value }}</h5>
                </div>

                <q-list bordered class="rounded-borders">
                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="mdi-account-plus"
                    label="Crear cuenta"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Para poder utilizar esta plataforma es necesario acceder con una cuenta de usuario, si no se
                          tiene una cuenta es muy sencillo crear una. Para crear una cuenta de usuario hay que ir al
                          menú principal ubicado en la esquina superior derecha, en la opción <strong>Crear
                            cuenta</strong>.</p>
                        <img src="statics/bienvenida/crear_cuenta.PNG" width="474">
                        <p>Al acceder a la opción crear cuenta, se desplegará un cuadro de dialogo con varios campos que
                          se deben llenar, estos se detallan a continuación:</p>
                        <p>Nota: todos los campos son obligatorios excepto los que se especifique lo contrario.</p>
                        <ul>
                          <li><strong>Nombre de usuario</strong>: es el identificador (username) a usar para iniciar
                            sesión
                            posteriormente
                          </li>
                          <li><strong>Nombre(s)</strong>: Nombre o nombres, sin apellidos</li>
                          <li><strong>Apellidos</strong>: Apellidos como constan en el registro civil</li>
                          <li><strong>Email</strong>: Dirección de correo electrónico actual</li>
                          <li><strong>Fecha de nacimiento</strong>: Fecha de nacimiento en formato AAAA-MM-DD</li>
                          <li><strong>Sexo</strong>: Género sexual</li>
                          <li><strong>Etnia</strong>: En caso de pertenecer a alguna etnia, seleccionarla, de lo
                            contrario omitirla.
                            (campo no obligatorio)
                          </li>
                          <li><strong>Municipio</strong>: Municipio donde se radica actualmente</li>
                          <li><strong>Colonia</strong>: Colonia donde se radica actualmente</li>
                          <li><strong>Discapacidades</strong>: Si se tiene algúna (o más) tipo de discapacidad, de lo
                            contrario omitir.
                            (campo no obligatorio)
                          </li>
                          <li><strong>Contraseña</strong>: Contraseña (password) para ingresar a la plataforma</li>
                          <li><strong>Confirmar Contraseña</strong>: Contraseña (password) para ingresar a la
                            plataforma, debe ser
                            identica que en campo anterior y se usa una confirmación para asegurar que se ha escrito
                            correctamente.
                          </li>
                        </ul>
                        <p>Una vez llenados todos los campos, se puede pulsar sobre el botón "Crear cuenta", seguido de
                          lo
                          cual, la cuenta estará creada y lista para usar.</p>

                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="login"
                    label="Ingresar (iniciar sesión)"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Como ya se menciona en el punto de arriba, es importante tener una cuenta para poder crear
                          reportes, con dicha cuenta se puede ingresar y entonces registrar reportes.</p>
                        <p>Para ingresar, hay que ir al menú principal ubicado en la esquina superior derecha, en la
                          opción <strong>Ingresar</strong>.</p>
                        <img src="statics/bienvenida/ingresar_cuenta.PNG" width="474">
                        <p>Una vez ahì se solicitara los datos de acceso de nombre de usuario y contraseña, los cuales
                          fueron elegidos durante el registro.</p>
                        <p>Si no se recuerda la contraseña, hay que ingresar alguna contraseña que se recuerde, donde si
                          no es exactamente la contraseña, se mostrará un mensaje que indica que la contraseña es
                          incorrecta, y se mostrará también un botón para recuperar la contraseña.</p>
                        <img src="statics/bienvenida/iniciar_sesion_incorrecto.PNG" width="474">
                        <p>Para recuperar la contraseña hay que pulsar el botón "Restablecer contraseña", el cual
                          mostrará una ventana solicitado la dirección de correo que se utilizó para crear la cuenta. Se
                          debe introducir la dirección de correo y a continuación pulsar el botón "Enviar correo de
                          recuperación". Posteriormente hay que revisar el correo electronico, a donde llegará un enlace
                          para asignar una nueva contraseña. Despues de cambiarla ya se debe poder acceder con la nueva
                          contraseña.</p>
                        <img src="statics/bienvenida/recuperar_contra.PNG" width="474">
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="info"
                    label="Ver info de un reporte"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Para poder visualizar la info de un reporte en particular se debe tener seleccionara la
                          herramienta "info" de la barra de herramientas, en la parte superior izquierda.</p>
                        <img src="statics/bienvenida/info.PNG" width="474">
                        <br>
                        <p>Teniendo seleccionada la herramienta "info", se puede ir al mapa y dar click sobre cualquier
                          punto para obtener la ficha de los detalles de dicho reporte, los cuales se mostraran en una
                          ficha cuya esquina superior izquierda coincide con la ubicación del punto seleccionado</p>
                        <img src="statics/bienvenida/info_ficha.PNG" width="474">
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="mdi-playlist-plus"
                    label="Agregar reporte basado en domicilio"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Se pueden crear reportes a partir de conocer la ubicación de la calle y número del lugar o
                          calles y su calle de intersección.</p>
                        <p>Para crear un nuevo reporte en este modo hay que seleccionar la herramienta de "Agrear
                          reporte basado en domicilio" de la barra de herramientas.</p>
                        <img src="statics/bienvenida/nuevo_domicilio.PNG" width="474">
                        <p>A continuación hay que llenar el formulario con los datos correspondientes a cada campo,
                          dependiendo de las opciones seleccionadas se iran desplegando nuevos campos acorde a lo
                          previamente seleccionado.</p>
                        <p>En esta modalidad de registro, la ubicación espacial se logra a partir de los datos del
                          domicilio. Para una mejor precisión es importante escribir el nombre de la calle completo y
                          solo uno de estos dos: el número postal de la ubicación del caso, o una calle cercana que
                          intersecte.</p>
                        <p>Una vez se ha terminado de llenar los datos, se debe dar clic en el botón <strong>Guardar
                          reporte</strong> y si todo es correcto, se almacenará el registro correspondiente en la base
                          de datos.</p>
                        <p>Nota: Los reportes nuevos no se reflejan en el mapa inmediatamente, hay que esperar unos
                          segundos para su almacenamiento.</p>
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                  <q-expansion-item
                    group="somegroup"
                    expand-separator
                    icon="mdi-map-marker-plus"
                    label="Agregar reporte a partir de un marcador en el mapa"
                  >
                    <q-card>
                      <q-card-section>
                        <p>Se pueden crear reportes a partir de poner un marcador o pin directamente sobre el mapa, en
                          los casos donde resulte más facil ubicar directamente en el mapa esta es la mejor opción.</p>
                        <p>Para crear un nuevo reporte en este modo hay que seleccionar la herramienta de "Agrear
                          reporte ubicando en el mapa" de la barra de herramientas.</p>
                        <img src="statics/bienvenida/nuevo_marcador.PNG" width="474">
                        <p>A continuación hay que llenar el formulario con los datos correspondientes a cada campo,
                          dependiendo de las opciones seleccionadas se iran desplegando nuevos campos acorde a lo
                          previamente seleccionado.</p>
                        <p>En esta modalidad de registro, Los datos de la ubicación del domicilio se obtienen a partir
                          de una consulta espacial a partir de las coordenadas donde se haya hecho click sobre el mapa,
                          y los datos referentes al domicilio se llenan automaticamente.</p>
                        <p>Una vez se ha terminado de llenar los datos del reporte, se debe dar clic en el botón
                          <strong>Guardar reporte</strong> y si todo es correcto, se almacenará el registro
                          correspondiente en la base de datos.</p>
                        <p>Nota: Los reportes nuevos no se reflejan en el mapa inmediatamente, hay que esperar unos
                          segundos para su almacenamiento.</p>
                      </q-card-section>
                    </q-card>
                  </q-expansion-item>

                </q-list>

              </div>
            </div>
          </div>
        </q-card-section>
        <q-separator/>
        <q-card-section class="row items-center">
          <div class="row full-width">
            <div class="col full-width">
              <q-btn @click="bienvenida_dialog = false" no-caps color="green"
                     label="Entendido" class="full-width"/>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-footer elevated class="bg-grey-10 text-grey-4">
      <q-toolbar style="min-height: 24px; font-size: 14px;">
        <span class="ellipsis">Instituto Municipal de las Mujeres Zapopanas para la Igualdad Sustantiva</span>
        <q-space/>
        <span class="no-wrap">
        <a style="text-decoration: none" class="text-grey-4 no-underline" href="https://saeba.click"
           target="_blank">2020&nbsp;&copy;&nbsp;saeba.click
         <q-tooltip content-class="bg-black no-border-radius" content-style="font-size: 16px" anchor="top middle"
                     self="bottom middle">
            Desarrollo: César Benjamín
          </q-tooltip>
        </a>
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
      homeData: {},
      drawer_left: false,
      isPwd: true,
      login_failure: false,
      login_dialog: false,
      logout_dialog: false,
      register_dialog: false,
      resetpassword_dialog: false,
      changepassword_dialog: false,
      resetpassworddone_dialog: false,
      changepassworddone_dialog: false,
      profile_dialog: false,
      profileupdated_dialog: false,
      accountcreated_dialog: false,
      bienvenida_dialog: false,
      login_username: undefined,
      login_password: undefined,
      reset_email: undefined,
      full_user_data: {
        username: undefined, first_name: undefined, last_name: undefined, email: undefined,
        is_staff: false, sexo: undefined, municipio: undefined, colonia: undefined, etnia: undefined,
        fecha_nacimiento: undefined, discapacidades: undefined
      },
      new_user_data: {
        username: undefined, first_name: undefined, last_name: undefined, email: undefined,
        sexo: undefined, municipio: undefined, colonia: undefined, etnia: undefined,
        fecha_nacimiento: undefined, password1: undefined, password2: undefined, discapacidades: undefined
      },
      user_fecha_nacimiento: "",
      etnias: undefined,
      municipios: undefined,
      colonias: undefined,
      discapacidades: undefined,
      paginas: {items: [], meta: {total_count: 0}},
      create_account_dialog: false,
      old_password: undefined,
      new_password1: undefined,
      new_password2: undefined,
      registration_response_error: {username: undefined, email: undefined},
      registration_response_data: undefined,

    }
  },
  watch: {
    auth_user() {
      if (this.auth_user.pk) {
        setTimeout(() => {
          this.getProfile(this.auth_user.pk)
        }, 200)
      } else {
        console.log("no auth_user")
      }
    },
    'full_user_data.municipio': function (newVal, oldVal) {
      if (oldVal) {
        this.getColonias(newVal)
      }
      if (newVal) {
        if (!this.new_user_data.colonia)
          this.full_user_data.colonia = undefined
        this.getColonias(newVal)
      }
    },
    'new_user_data.municipio': function (newVal, oldVal) {
      if (newVal) {
        this.new_user_data.colonia = undefined
        this.getColonias(newVal)
      }
    },
    homeData() {
      if (this.homeData) {
        if (!this.auth_logged) {
          this.bienvenida_dialog = true
        }
      }
    },
    profile_dialog() {
      if (this.profile_dialog) {
        const token = cookies.get("auth_token") || this.auth_token
        axios.get(`https://api.zapopanentrenosotras.com/rest/v1/usuarios-autenticado/${this.auth_user.pk}/`,
          {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
          this.full_user_data = response.data
          this.is_user_staff = response.data.is_staff
          if (this.full_user_data.fecha_nacimiento) {
            this.user_fecha_nacimiento = this.full_user_data.fecha_nacimiento.split("-").join('/')
          }
        }).catch(error => {
          console.log(error)
        })
      }
    },
    user_fecha_nacimiento() {
      if (this.user_fecha_nacimiento) {
        this.full_user_data.fecha_nacimiento = this.user_fecha_nacimiento.split("/").join('-')
        this.new_user_data.fecha_nacimiento = this.user_fecha_nacimiento.split("/").join('-')
      }
    },
  },
  computed: {
    ...mapGetters('geojitsu', ['GISRibbonIsOpenGetter', 'getHerramientaActiva', 'getUserGroups', 'getIsUserStaff']),
    ...mapGetters('auth', ['logged', 'user', 'token']),
    is_user_staff: {
      get() {
        return this.getIsUserStaff
      },
      set(value) {
        this.setUserIsStaff(value)
      }
    },
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
    auth_token: {
      get() {
        return this.token
      }
    },
    herramientaActiva: {
      get() {
        return this.getHerramientaActiva
      },
      set(value) {
        this.setHerramientaActiva(value)
      }
    },
    userGroups: {
      get() {
        return this.getUserGroups
      },
      set(value) {
        this.setUserGroups(value)
      }
    },
    showGISRibbon: {
      get() {
        return this.GISRibbonIsOpenGetter
      },
      set(value) {
        this.GISRibbonIsOpenAction(value)
      }
    },
    usernameExists() {
      return this.registration_response_error.username !== undefined
    },
    emailExists() {
      return this.registration_response_error.email !== undefined
    },
    drawerHeight() {
      return this.$q.screen.height - 260 + "px"
    },
  },
  methods: {
    ...mapActions('geojitsu', ['GISRibbonIsOpenAction', 'setHerramientaActiva', 'setUserGroups', 'setUserIsStaff']),
    ...mapActions('auth', ['setUser']),
    openLogin() {
      // this.accountcreated_dialog = false
      this.login_dialog = true
    },
    login() {
      this.$auth.attemptLogin(
        {
          username: this.login_username,
          password: this.login_password
        }, true
      ).then(response => {
        this.login_dialog = false
        this.user_fecha_nacimiento = ""
      }).catch(error => {
        this.login_failure = true
      })
    },
    logout() {
      this.$auth.logout(
      ).then(() => {
        this.logout_dialog = false
        this.user_fecha_nacimiento = ""
        this.herramientaActiva = "info"
      }).catch(error => {
        console.log(error)
      }).finally(() => {
        this.userGroups = []
      })
    },
    open_resetpassword_dialog() {
      this.login_dialog = false
      this.resetpassword_dialog = true
      this.login_failure = false
      this.login_username = undefined
      this.login_password = undefined
    },
    open_changepassword_dialog() {
      this.profile_dialog = false;
      this.changepassword_dialog = true;
      this.old_password = undefined;
      this.new_password1 = undefined;
      this.new_password2 = undefined;
    },
    isValidEmail(val) {
      const emailPattern = /^(?=[a-zA-Z0-9@.%+-]{6,254}$)[a-zA-Z0-9.%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
      if (this.emailExists) {
        return "Ya existe una cuenta con el mismo email"
      } else {
        return emailPattern.test(val) || 'La dirección email no tiene formato correcto.';
      }
    },
    cleanRegisterForm() {
      this.new_user_data = {
        username: undefined, first_name: undefined, last_name: undefined, email: undefined,
        sexo: undefined, municipio: undefined, colonia: undefined, etnia: undefined,
        fecha_nacimiento: undefined, password1: undefined, password2: undefined, discapacidades: undefined
      }
      this.registration_response_data = undefined
      this.user_fecha_nacimiento = ""
    },
    createAccount() {
      this.registration_response_error = {username: undefined, email: undefined}
      if (this.new_password1 === this.new_password2) {
        this.new_user_data.password = this.new_password1
      }
      if (this.new_user_data.discapacidades === null) {
        this.new_user_data.discapacidades = []
      }
      this.$refs.form_register.validate().then(valid => {
          if (valid) {
            axios.post("https://api.zapopanentrenosotras.com/rest/v1/auth/registration/", this.new_user_data)
              .then(response => {
                this.create_account_dialog = false;
                this.create_account_info_dialog = true;
                this.accountcreated_dialog = true;
                this.login_username = this.new_user_data.username
                this.login_password = this.new_user_data.password1
                this.login()
              }).catch(error => {
              console.log("registration error", error)
              if (error.response) {
                this.registration_response_error = error.response.data
                this.$refs.form_register.validate()
              }
            })
          } else {
            return false;
          }
        }
      ).catch(error => {
      })
    },
    getPaginaHome() {
      axios.get("https://api.zapopanentrenosotras.com/rest/v1/pages/?type=home.HomePage&fields=*")
        .then(response => {
          this.homeData = response.data.items[0]
        })
    },
    resetPassword() {
      axios.post("https://api.zapopanentrenosotras.com/rest/v1/auth/password/reset/", {email: this.reset_email})
        .then(response => {
          this.resetpassword_dialog = false
          this.resetpassworddone_dialog = true
        }).catch(error => {
      })
    },
    changePassword() {
      const token = cookies.get("auth_token");
      axios.post("https://api.zapopanentrenosotras.com/rest/v1/auth/password/change/",
        {old_password: this.old_password, new_password1: this.new_password1, new_password2: this.new_password2},
        {headers: {'Authorization': `Bearer ${token}`}})
        .then(response => {
          this.changepassword_dialog = false
          this.changepassworddone_dialog = true
        }).catch(error => {
      })
    },
    getEtnias() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/etnias/`).then(response => {
        this.etnias = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    getMunicipios() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/municipios/`).then(response => {
        this.municipios = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    getColonias(municipio) {
      if (municipio) {
        axios.get(`https://api.zapopanentrenosotras.com/rest/v1/colonias/?municipio=${municipio}`).then(response => {
          this.colonias = response.data
        }).catch(error => {
          console.log(error)
        })
      }
    },
    getDiscapacidades() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/discapacidades/`).then(response => {
        this.discapacidades = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    getPaginas() {
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/pages/?type=home.StandardPage`).then(response => {
        this.paginas = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    getProfile(id) {
      const token = cookies.get("auth_token") || this.auth_token
      axios.get(`https://api.zapopanentrenosotras.com/rest/v1/usuarios-autenticado/${id}/`,
        {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
        this.full_user_data.username = response.data.username
        this.full_user_data.first_name = response.data.first_name
        this.full_user_data.last_name = response.data.last_name
        this.full_user_data.email = response.data.email
        this.full_user_data.fecha_nacimiento = response.data.fecha_nacimiento
        this.full_user_data.sexo = response.data.sexo
        this.full_user_data.etnia = response.data.etnia
        this.full_user_data.municipio = response.data.municipio
        this.full_user_data.colonia = response.data.colonia
        this.full_user_data.discapacidades = response.data.discapacidades
        this.is_user_staff = response.data.is_staff
      }).then(() => {
        this.getUserGroupsData()
      }).catch(error => {
        console.log(error)
      })
    },
    updateProfile() {
      const token = cookies.get("auth_token")
      if (this.full_user_data.discapacidades === null) {
        this.full_user_data.discapacidades = []
      }
      this.$refs.form_profile.validate().then(valid => {
        if (valid) {
          axios.patch(`https://api.zapopanentrenosotras.com/rest/v1/usuarios-autenticado/${this.auth_user.pk}/`,
            this.full_user_data, {headers: {'Authorization': `Bearer ${token}`}})
            .then(response => {

              this.profile_dialog = false
              this.profileupdated_dialog = true
              this.$auth.refreshToken().then(response => {
              }).catch(error => {
                console.log(error)
              })
            })
        } else {
          return false;
        }
      }).catch(error => {
      });
    },
    get_gravatar(email, argsize) {
      let mail = "default@gravatar.com"
      if (email) {
        mail = email
      }
      return 'https://www.gravatar.com/avatar/' + md5(mail.trim().toLowerCase(), 'hex') + '.jpg?s=' + argsize;
    },
    getUserGroupsData() {
      if (this.auth_user) {
        const token = cookies.get("auth_token")
        axios.get(`https://api.zapopanentrenosotras.com/rest/v1/usuarios-autenticado/${this.auth_user.pk}/`,
          {headers: {'Authorization': `Bearer ${token}`}}).then(response => {
          this.userGroups = response.data.groups
        }).catch(error => {
          console.log(error)
        })
      }
    },
    testa(val) {
      alert(val);
    },
  },
  mounted() {
    this.getPaginaHome()
    this.getMunicipios()
    this.getEtnias()
    this.getDiscapacidades()
    this.getPaginas()
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
