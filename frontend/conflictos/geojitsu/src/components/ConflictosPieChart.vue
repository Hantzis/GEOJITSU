<template>
  <div class="q-pa-md">
    <q-card flat bordered class="my-card">
      <q-card-section>
        <div class="text-h6">{{ title }}</div>
      </q-card-section>

      <q-separator inset/>

      <q-card-section>
        {{ dataGrafica }}
        <!--
        <pie-chart v-if="chartData.datasets.data.length > 0" :chart-data="chartData" :options="options"></pie-chart>
        -->
      </q-card-section>

    </q-card>
  </div>
</template>

<script>
import PieChart from "components/PieChart";

export default {
  components: {},
  name: "ConflictosPieChart",
  props: {
    title: String,
    dataGrafica: Array
  },
  data() {options
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false
      },
      etiquetas: [],
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
      this.etiquetas.push(Object.entries(val)[0][0])
      this.datos.push(Object.entries(val)[0][1])
    })
    this.chartData.labels = this.etiquetas
    this.chartData.datasets.data = this.datos
  },
}
</script>

<style lang="scss" scoped>
.my-card {
  width: 100%;
  max-width: 400px;
}

</style>
