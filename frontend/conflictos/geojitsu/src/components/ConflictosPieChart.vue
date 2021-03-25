<template>
  <div class="q-pa-md">
    <q-card flat bordered class="my-card">
      <q-card-section>
        <div class="text-h6">{{ title }}</div>
      </q-card-section>

      <q-separator inset/>

      <q-card-section>
        <pie-chart v-if="dataGrafica" :chart-data="chartData" :opciones="options"></pie-chart>
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
    dataGrafica: Array
  },
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
      opciones: [],
      datos: [],
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#9ff879',
            data: []
          }
        ]
      }
    }
  },
  methods: {
    fillData() {
    },
  },
  mounted() {
    this.dataGrafica.forEach(val => {
      this.opciones.push(Object.entries(val)[0][0])
      this.datos.push(Object.entries(val)[0][1])
    })
    this.chartData.labels = this.opciones
    this.chartData.datasets.data = this.opciones
  },
}
</script>

<style lang="scss" scoped>
.my-card {
  width: 100%;
  max-width: 400px;
}

</style>
