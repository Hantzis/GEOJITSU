import * as firebase from 'firebase/app'
import 'firebase/firestore'

const firebaseConfig = {
  apiKey: 'AIzaSyAlli3CVLPLJXQK8JT9koDzsltdnAE--80',
  authDomain: 'windows-todo.firebaseapp.com',
  databaseURL: 'https://windows-todo.firebaseio.com',
  projectId: 'windows-todo',
  storageBucket: 'windows-todo.appspot.com',
  messagingSenderId: '824097207715',
  appId: '1:824097207715:web:665464bdd0d995d4881616'
}
// Initialize Firebase
// eslint-disable-next-line no-unused-vars
const firebaseApp = firebase.initializeApp(firebaseConfig)
const db = firebase.firestore()

export { db, firebase }
