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
