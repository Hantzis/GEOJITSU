import { VueJwtAuth, AxiosHttpDriver } from '@mspiderv/vuejwtauth'

export default ({ Vue, router, store }) =>  new VueJwtAuth({
  Vue, // required
  router, // required
  store,
  options: { // optional
    drivers: {
      http: new AxiosHttpDriver({
        // Your API URL here
        apiBaseURL: 'https://api.zapopanentrenosotras.maptitud.xyz/rest/v1/auth/'
      })
    }
  }
})


