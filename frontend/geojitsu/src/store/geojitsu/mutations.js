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

export const capaActivaMutation = (state, value) => {
  state.capaActiva = value
}
