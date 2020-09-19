/*
export function someMutation (state) {
}
*/

export const keyToken = (state, value) => {
  state.keyToken = value
}

export const accessToken = (state, value) => {
  state.accessToken = value
}

export const refreshToken = (state, value) => {
  state.refreshToken = value
}

export const usuario = (state, value) => {
  state.usuario = value
}
