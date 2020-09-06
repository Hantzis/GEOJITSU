<template>
    <q-page padding>
      <p class="text-h4">{{ pageData.title }}</p>
      <div v-for="data of pageData.cuerpo" :key="data.id">
        <span v-if="data.type==='header_block'" :class="'text-' + data.value.header" v-text="data.value.text"></span>
        <div v-if="data.type==='paragraph_block'" v-html="data.value"></div>
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
    axios.get("https://conflictossocioambientales.iies.unam.mx/api/v2/pages/9/").then(response => {
      this.pageData = response.data
    }).catch(error => {
      console.log(error)
    })
  }
}
</script>

<style scoped>

</style>
