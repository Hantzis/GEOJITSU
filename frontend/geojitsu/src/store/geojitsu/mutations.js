/*
export function someMutation (/ * state * /) {
}
*/

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

export const CapasTickedMutation = (state, value) => {
  for (let capa of state.capasMapa) {
    capa.visible = !!value.includes(capa.value);
  }
}

export const CapaOpacityMutation = (state, value) => {
  state.capasMapa[value.capa].opacity = value.value
}

export const SubirCapaMutation = (state, value) => {
  state.capasMapa.splice(value-1,0,state.capasMapa.splice(value,1)[0])
}

export const BajarCapaMutation = (state, value) => {
  state.capasMapa.splice(value+1,0,state.capasMapa.splice(value,1)[0])
}
