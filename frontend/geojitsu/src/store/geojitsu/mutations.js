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
  console.log("CapasTickedMutation", value)
  for (let capa of state.capasMapa) {
    console.log("capa: ",capa.value, capa.visible)
    capa.visible = false
    if (value.includes(capa.value))
      capa.visible = true
  }
  console.log("state.capasMapa", state.capasMapa)
}
