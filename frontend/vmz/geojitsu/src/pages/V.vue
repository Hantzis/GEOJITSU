<template>


  <q-page class="q-px-md q-pt-md">
    <div class="column fit justify-between" style="min-height: inherit">
      <div class="col">
        <router-view :page_data="pageData"/>
      </div>
      <div class="col-auto q-py-md">
        <q-separator></q-separator>
        <br>
        <div v-scroll class="row justify-center no-wrap">
          <div class="col-auto q-px-sm">
            <img src="https://repvmz.maptitude.xyz/media/images/1.original.png" height="110px">
          </div>
          <div class="col-auto q-px-sm">
            <img src="https://repvmz.maptitude.xyz/media/images/2.original.png" height="110px">
          </div>
          <div class="col-auto q-px-sm">
            <img src="https://repvmz.maptitude.xyz/media/images/3.original.png" height="110px">
          </div>
        </div>
      </div>
    </div>
  </q-page>


</template>

<script>
// import axios from 'axios'

import axios from "axios";

export default {
  name: "Acerca",
  data() {
    return {
      pageData: undefined
    }
  },
  methods: {
    getPaginas() {
      axios.get("https://repvmz.maptitude.xyz/back/api/v1/pages/?type=home.StandardPage&fields=*")
      .then(response => {
        console.log("response getPaginas", response)
        console.log("response urlpat", this.urlPath)
        this.pageData = response.data.items
        response.data.items.forEach(row => {
          console.log("row", row)
        })
      })
    },
    getPagina(slug) {
      console.log("slug qqq", slug)
      console.log(this.items)
      for (let item of items) {
        if (item.meta.slug === slug) {
          console.log("aqui", slug)
        }
      }
    }
  },

  mounted() {
    this.getPaginas()
  }
}
</script>

<style scoped>

</style>
