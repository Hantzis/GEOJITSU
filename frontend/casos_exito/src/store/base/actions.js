/*
export function someAction (context) {
}
*/

export const setUserData = ({commit}, payload) => {
  commit('UserData', payload)
}
