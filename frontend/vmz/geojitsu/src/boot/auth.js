import { VueJwtAuth, AxiosHttpDriver } from '@mspiderv/vuejwtauth'

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

export default ({ Vue, router, store }) => {
  const auth = new VueJwtAuth({
    Vue,
    router,
    store,
    options: {
      drivers: {
        http: new AxiosHttpDriver({
          apiBaseURL: 'https://api.zapopanentrenosotras.com/rest/v1/auth/'
        })
      }
    }
  })

  // 🔴 ESTA ES LA LÍNEA QUE TE FALTA
  const token = getCookie('auth_token')
  if (token) {
    auth.setToken(token)
  }

  return auth
}

