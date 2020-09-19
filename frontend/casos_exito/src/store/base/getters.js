/*
export function someGetter (state) {
}
*/

export const getKeyToken = (state) => {
  return state.keyToken
}

export const getAccessToken = (state) => {
  return state.accessToken
}

export const getRefreshToken = (state) => {
  return state.refreshToken
}

export const getUsuario = (state) => {
  return state.usuario
}
