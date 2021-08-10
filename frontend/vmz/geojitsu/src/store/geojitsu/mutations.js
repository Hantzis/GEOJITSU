/*
export function someMutation (/ * state * /) {
}
*/

export const userData = (state, value) => {
  state.userData = value
}

export const GISRibbonIsOpenMutation = (state, is_open) => {
  state.GISRibbonIsOpen = is_open
}

export const mapaBaseMutation = (state, value) => {
  state.mapaBase = value
}

export const capaSeleccionadaMutation = (state, value) => {
  state.capaSeleccionada = value
}

export const drawerCapasMutation = (state, value) => {
  state.drawerCapas = value
}

export const capasMapaMutation = (state, value) => {
  state.capasMapa = value
}

export const herramientaActivaMutation = (state, value) => {
  state.herramientaActiva = value
}

export const mapkeyMutation = (state, value) => {
  state.mapkey = value
}

export const userGroupsMutation = (state, value) => {
  state.userGroups = value
}

export const CapasTickedMutation = (state, value) => {
  for (let capa of state.capasMapa) {
    capa.visible = !!value.includes(capa.value);
  }
}

export const CapaTickedMutation = (state, value) => {
  state.capasMapa[state.capasMapa.indexOf(value.capa)].visible = value.visible
}

export const CapaOpacityMutation = (state, value) => {
  state.capasMapa[value.capa].opacity = value.value
}

export const CapaCQLFilterMutation = (state, value) => {
  state.capasMapa[value.capa].params.cql_filter = value.filtro
}

export const SubirCapaMutation = (state, value) => {
  state.capasMapa.splice(value - 1, 0, state.capasMapa.splice(value, 1)[0])
  const tempCapas = state.capasMapa
  state.capasMapa = []
  for (let capa of tempCapas) {
    state.capasMapa.push(capa)
  }
}

export const BajarCapaMutation = (state, value) => {
  state.capasMapa.splice(value + 1, 0, state.capasMapa.splice(value, 1)[0])
  const tempCapas = state.capasMapa
  state.capasMapa = []
  for (let capa of tempCapas) {
    state.capasMapa.push(capa)
  }
}

export const CapaSetFeaturesMutation = (state, value) => {
  state.capasMapa[value.capa].features = value.features
}
