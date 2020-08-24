/*
export function someAction (/ * context * /) {
}
*/

export const GISRibbonIsOpenAction = ({commit}, payload) => {
  commit('GISRibbonIsOpenMutation', payload)
}

export const mapaBaseAction = ({commit}, payload) => {
  commit('mapaBaseMutation', payload)
}

export const capaSeleccionadaAction = ({commit}, payload) => {
  commit('capaSeleccionadaMutation', payload)
}

export const setDrawerCapas = ({commit}, payload) => {
  commit('drawerCapasMutation', payload)
}

export const setCapasTicked = ({commit}, payload) => {
  commit('CapasTickedMutation', payload)
}
