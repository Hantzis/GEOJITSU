<template>
  <div class="q-pa-md">
    <q-card flat bordered class="my-card">
      <q-card-section>
        <div class="text-h6">{{ title }}</div>
      </q-card-section>

      <q-separator inset/>

      <q-card-section>
        <pie-chart v-if="loaded && dataGrafica.length > 0" :chart-data="chartData" :options="options"></pie-chart>
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
    dataGrafica: Array,
  },
  data() {
    return {
      colorScheme: [
        "#25CCF7", "#FD7272", "#54a0ff", "#00d2d3",
        "#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e",
        "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50",
        "#f1c40f", "#e67e22", "#e74c3c", "#ecf0f1", "#95a5a6",
        "#f39c12", "#d35400", "#c0392b", "#bdc3c7", "#7f8c8d",
        "#55efc4", "#81ecec", "#74b9ff", "#a29bfe", "#dfe6e9",
        "#00b894", "#00cec9", "#0984e3", "#6c5ce7", "#ffeaa7",
        "#fab1a0", "#ff7675", "#fd79a8", "#fdcb6e", "#e17055",
        "#d63031", "#feca57", "#5f27cd", "#54a0ff", "#01a3a4"
      ],
      loaded: false,
      options: {
        legend: {
          display: false
        },
        responsive: true,
        maintainAspectRatio: false
      },
      etiquetas: [],
      datos: [],
      colores: [],
      chartData: {
        datasets: [
          {
            data: [],
            backgroundColor: [],
          }
        ]
      }
    }
  },
  methods: {
    fillData() {
    },
  },
  watch: {
    chartData() {
      console.log("this.chartData", this.chartData)
      console.log("this.chartData len", this.chartData.datasets[0].data.length)
    },
    dataGrafica() {
      this.loaded = false
      if (this.dataGrafica) {
        this.dataGrafica.forEach(val => {
          this.etiquetas.push(Object.entries(val)[0][0])
          this.datos.push(Object.entries(val)[0][1])
          this.colores.push(this.colorScheme[Math.floor(Math.random() * 44)])
        })
        this.chartData.labels = this.etiquetas
        this.chartData.datasets[0].data = this.datos
        this.chartData.datasets[0].backgroundColor = this.colores
        this.loaded = true
      }
    },
  },
  mounted() {
    this.loaded = false
    if (this.dataGrafica) {
      this.dataGrafica.forEach(val => {
        this.etiquetas.push(Object.entries(val)[0][0])
        this.datos.push(Object.entries(val)[0][1])
        this.colores.push(this.colorScheme[Math.floor(Math.random() * 44)])
      })
      this.chartData.labels = this.etiquetas
      this.chartData.datasets[0].data = this.datos
      this.chartData.datasets[0].backgroundColor = this.colores
      this.loaded = true
    }
  },
}
</script>

<style lang="scss" scoped>
.my-card {
  width: 100%;
  max-width: 400px;
}

</style>
