/*
export function someAction (context) {
}
*/

export const setKeyToken = ({commit}, payload) => {
  commit('keyToken', payload)
}

export const setAccessToken = ({commit}, payload) => {
  commit('accessToken', payload)
}

export const setRefreshToken = ({commit}, payload) => {
  commit('refreshToken', payload)
}

export const setUsuario = ({commit}, payload) => {
  commit('usuario', payload)
}
