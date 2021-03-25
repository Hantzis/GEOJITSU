<script>
import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: "PieChart",
  extends: Pie,
  mixins: [reactiveProp],
  props: {
    opciones: Object,
  },
  mounted() {
    console.log("chartData, opciones", this.chartData, this.opciones)
    this.renderChart(this.chartData, this.opciones)
  }
}
</script>
