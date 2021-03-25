<template>
  <div class="q-pa-md">
    <q-card flat bordered class="my-card">
      <q-card-section>
        <div class="text-h6">{{ title }}</div>
      </q-card-section>

      <q-separator inset/>

      <q-card-section>
        <pie-chart :chart-data="datos" :opciones="opciones"></pie-chart>
      </q-card-section>

    </q-card>
  </div>
</template>

<script>
import PieChart from "components/PieChart";

export default {
  components: {PieChart},
  name: "ConflictosPieChart",
  props: {
    title: String,
    data: Array
  },
  data() {
    return {
      opciones: [],
      datos: [],
    }
  },
  methods: {
    fillData() {
    },
  },
  mounted() {
    this.data.forEach(val => {
      this.opciones.push(Object.entries(val)[0][0])
      this.datos.push(Object.entries(val)[0][1])
    })
  },
}
</script>

<style lang="scss" scoped>
.my-card {
  width: 100%;
  max-width: 400px;
}

</style>
