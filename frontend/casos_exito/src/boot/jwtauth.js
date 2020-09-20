// import something here

// "async" is optional;
// more info on params: https://quasar.dev/quasar-cli/cli-documentation/boot-files#Anatomy-of-a-boot-file
//export default async (/* { app, router, Vue ... } */) => {
  // something to do
//}
//import Vue from 'vue'
//import router from '../router'
//import base from '../store/base'

import { VueJwtAuth, AxiosHttpDriver } from '@mspiderv/vuejwtauth'

//export default ({ Vue, store, router }) => new VueJwtAuth({
export default ({ Vue, store, router }) => new VueJwtAuth({
  Vue,
  router,
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
