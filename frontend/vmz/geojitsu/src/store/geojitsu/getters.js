/*
export function someGetter (/ * state * /) {
}
*/

export const getUserData = (state) => {
  return state.UserData
}

export const GISRibbonIsOpenGetter = (state) => {
  return state.GISRibbonIsOpen
}

export const mapasBaseGetter = (state) => {
  return state.mapasBase
}

export const mapaBaseGetter = (state) => {
  return state.mapaBase
}

export const capasMapaGetter = (state) => {
  return state.capasMapa
}

export const capaSeleccionadaGetter = (state) => {
  return state.capaSeleccionada
}

export const getDrawerCapas = (state) => {
  return state.drawerCapas
}
