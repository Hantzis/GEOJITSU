<template>
  <div>
    <div v-for="item of page_data" :key="item.id">
      <div v-if="item.meta.slug === urlPath">
        <h4 style="margin: 12px 0 22px 0;">{{ item.title }}</h4>
        <div v-for="block of item.contenido" :key="block.id">
          <div v-if="block.type === 'image'">
            <div v-html="block.value"></div>
          </div>
          <div v-if="block.type === 'paragraph'">
            <div v-html="block.value"></div>
          </div>
          <div v-if="block.type === 'title'">
            <h5>{{ block.value  }}</h5>
          </div>
        </div>
      </div>
    </div>

  </div>


</template>

<script>
import axios from 'axios'


export default {
  name: "Acerca",
  props: ['page_data'],
  data() {
    return {
      pageData: undefined,
      items: undefined,
      detail_url: undefined,
    }
  },
  computed: {
    urlPath() {
      const slug = this.$route.fullPath.split("/")[2]
      return slug
    },
  },
  methods: {
    getPagina(slug) {
      // console.log("getPagina", slug)
    }
  },
}
</script>


