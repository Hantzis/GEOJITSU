<template>


  <q-page class="q-px-md q-pt-md">
    <div class="column fit justify-between" style="min-height: inherit">
      <div class="col">
        <p>.col-8dsad das dsa d</p>
        <p>.col-8dsad das dsa d</p>
        <p>.col-8dsad das dsa d</p>
        <p>.col-8dsad das dsa d</p>

        <router-view/>
      </div>
      <div class="col-auto" style="background-color: red;">
        <p>.col-8dsad das dsa d</p>
        <p>.col-8dsad das dsa d</p>
        <p>.col-8dsad das dsa d</p>
      </div>
    </div>
  </q-page>


</template>

<script>
// import axios from 'axios'

export default {
  name: "Acerca",
  data() {
    return {
      pageData: undefined
    }
  },
}
</script>

<style scoped>

</style>
