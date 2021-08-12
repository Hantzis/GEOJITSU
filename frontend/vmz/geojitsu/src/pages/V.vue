<template>
  <q-page class="q-px-md q-pt-md">
    <div class="column fit justify-between" :style="{'min-height': getHeight}">
      <div class="col q-px-md">
        <router-view :page_data="pageData"/>
      </div>
      <div class="col-auto q-py-md">
        <q-separator/>
        <br>
        <div>
          <q-tabs align="center" class="bg-white text-grey-9">
            <div name="logos" class="no-padding">
              <div class="row justify-center">
                <div class="col-auto q-px-md">
                  <img src="https://api.zapopanentrenosotras.com/media/images/2.original.png" height="50px">
                </div>
                <div class="col-auto q-px-md">
                  <img src="https://api.zapopanentrenosotras.com/media/images/3.original.png" height="50px">
                </div>
              </div>
            </div>
          </q-tabs>
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
  computed: {
    getHeight() {
      return this.$q.screen.height - 138 + "px"
    },
  },
  methods: {
    getPaginas() {
      axios.get("https://api.zapopanentrenosotras.com/api/v1/pages/?type=home.StandardPage&fields=*")
        .then(response => {
          this.pageData = response.data.items
        })
    },
    getPagina(slug) {
      console.log(this.items)
    }
  },
  mounted() {
    this.getPaginas()
  }
}
</script>

<style lang="scss" scoped>
</style>
