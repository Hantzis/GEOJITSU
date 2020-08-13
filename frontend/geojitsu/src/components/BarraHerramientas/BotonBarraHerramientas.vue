<template>
  <q-icon :name="my_icon">
    <q-tooltip v-if="tooltip_message"
               content-class="bg-black"
               content-style="font-size: 16px"
               anchor="top middle"
               self="bottom middle">
      {{ tooltip_message }}
    </q-tooltip>
  </q-icon>
</template>

<script>
  export default {
    name: "BotonHerramienta",
    props: {
      'tooltip_message': String,
      'icon': String
    },
    computed: {
      my_icon() {
        if (this.icon) {
          return this.icon
        } else
          return "default"
      }
    },
    data() {
      return {
      }
    }
  }
</script>
