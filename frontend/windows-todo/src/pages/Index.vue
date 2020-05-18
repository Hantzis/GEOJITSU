<template>
  <div class="q-pa-md q-gutter-sm">
    <q-editor
      v-model="editor"
      :definitions="{
        save: {
          tip: 'Save your work',
          icon: 'save',
          label: 'Save',
          handler: saveWork
        }
      }"
      :toolbar="[
        ['bold', 'italic', 'strike', 'underline'],
        ['save']
      ]"
    />

    <q-card class="row" flat bordered v-for="(item, index) in tasks" :key="index">
      <q-card-section class="col" v-html="item.texto" :class="item.estado ? 'tachar' : ''"/>
      <q-btn flat color="blue" @click="item.estado = !item.estado">Acción</q-btn>
      <q-btn flat color="red" @click="eliminar(index, item.id)">Eliminar</q-btn>
    </q-card>
    <div class="flex flex-center" v-if="tasks.length == 0">
      <h4>Sin notas</h4>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { db } from 'boot/firebase'
export default {
  name: 'PageIndex',
  data () {
    return {
      editor: '',
      taskss: [
        { texto: 'Tarea #1', estado: false },
        { texto: 'Tarea #2', estado: true },
        { texto: 'Tarea #3', estado: false }
      ],
      tasks: []
    }
  },
  created () {
    this.listarTareas()
  },
  methods: {
    async listarTareas () {
      try {
        await db.collection('tareas').get().then((restData) => {
          restData.forEach((res) => {
            const dataa = res.data()
            const tarea = {
              id: res.id,
              texto: dataa.texto,
              estado: dataa.estado
            }
            console.log(tarea)
            this.tasks.push(tarea)
          })
        }).catch((e) => {
          console.log('Error promsesdsd: ', e)
        })
      } catch (e) {
        console.log('Error: ', e)
      }
    },
    async saveWork () {
      try {
        const resDB = await db.collection('tareas').add({
          texto: this.editor,
          estado: false
        })
        console.log(resDB)
        this.tasks.push({
          texto: this.editor,
          estado: false,
          id: resDB.id
        })
        this.editor = ''
        this.$q.notify({
          message: 'Saved your text to local storage',
          color: 'green-4',
          textColor: 'white',
          icon: 'cloud_done'
        })
      } catch (e) {
        console.log(e)
      }
    },
    eliminar (index, id) {
      this.$q.dialog({
        title: 'Acción peligrosa',
        message: 'Seguro que quieres eliminar??',
        cancel: true,
        persistent: true
      }).onOk(async () => {
        // console.log('>>>> OK')
        try {
          await db.collection('tareas').doc(id).delete()
          this.tasks.splice(index, 1)
        } catch (e) {
          console.log(e)
        }
      }).onOk(() => {
        // console.log('>>>> second OK catcher')
      }).onCancel(() => {
        // console.log('>>>> Cancel')
      }).onDismiss(() => {
        // console.log('I am triggered on both OK and Cancel')
      })
    }
  }

}
</script>

<style scoped>
.tachar {
  text-decoration: line-through;
}
</style>
