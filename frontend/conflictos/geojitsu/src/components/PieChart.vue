<script>
import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: "PieChart",
  extends: Pie,
  mixins: [reactiveProp],
  props: {
    opciones: Array,
    datos: Array
  },
  mounted() {
    console.log("this.datos, this.opciones", this.datos, this.opciones)
    this.renderChart(this.chartData, this.opciones)
  }
}
</script>
