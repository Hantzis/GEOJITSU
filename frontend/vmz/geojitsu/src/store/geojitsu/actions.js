/*
export function someAction (/ * context * /) {
}
*/

export const setUserData = ({commit}, payload) => {
  commit('UserData', payload)
}

export const GISRibbonIsOpenAction = ({commit}, payload) => {
  commit('GISRibbonIsOpenMutation', payload)
}

export const mapaBaseAction = ({commit}, payload) => {
  commit('mapaBaseMutation', payload)
}

export const setHerramientaActiva = ({commit}, payload) => {
  commit('herramientaActivaMutation', payload)
}

export const setMapkey = ({commit}, payload) => {
  commit('mapkeyMutation', payload)
}

export const setUserGroups = ({commit}, payload) => {
  commit('userGroupsMutation', payload)
}

export const capasMapaAction = ({commit}, payload) => {
  commit('capasMapaMutation', payload)
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

export const setCapaTicked = ({commit}, payload) => {
  commit('CapaTickedMutation', payload)
}

export const setCapaOpacity = ({commit}, payload) => {
  commit('CapaOpacityMutation', payload)
}

export const setCapaCQLFilter = ({commit}, payload) => {
  console.log("aqui setCapaCQLFilter")
  commit('CapaCQLFilterMutation', payload)
}

export const subirCapaAction  = ({commit}, payload) => {
  commit('SubirCapaMutation', payload)
}

export const bajarCapaAction  = ({commit}, payload) => {
  commit('BajarCapaMutation', payload)
}

export const setCapaFeatures = ({commit}, payload) => {
  commit('CapaSetFeaturesMutation', payload)
}
