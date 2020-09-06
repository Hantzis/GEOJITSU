<template>
    <q-page padding>
      <p class="text-h4">{{ pageData.title }}</p>
      <div v-for="data of pageData.cuerpo" :key="data.id">
        <div v-html="data.value"></div>
      </div>
    </q-page>
</template>

<script>
import axios from 'axios'

export default {
  name: "Acerca",
  data() {
    return {
      pageData: undefined
    }
  },
  created() {
    axios.get("https://conflictossocioambientales.iies.unam.mx/api/v2/pages/10/").then(response => {
      this.pageData = response.data
    }).catch(error => {
      console.log(error)
    })
  }
}
</script>

<style scoped>

</style>
