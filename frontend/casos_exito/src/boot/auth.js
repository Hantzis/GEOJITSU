// import something here

// "async" is optional;
// more info on params: https://quasar.dev/quasar-cli/cli-documentation/boot-files#Anatomy-of-a-boot-file
//export default async (/* { app, router, Vue ... } */) => {
  // something to do
//}
//import Vue from 'vue'
//import Router from '../router'
//const router = Router()

//console.log(router)

import { VueJwtAuth, AxiosHttpDriver } from '@mspiderv/vuejwtauth'

export default ({ Vue, router, store }) =>  new VueJwtAuth({
  Vue, // required
  router, // required
  store,
  options: { // optional
    drivers: {
      http: new AxiosHttpDriver({
        // Your API URL here
        apiBaseURL: 'https://onsses45.maptitude.xyz/api/v1/rest-auth/'
      })
    }
  }
})


//Vue.prototype.$auth = jwtauth
