<script>
import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: "PieChart",
  mixins: [Pie, reactiveProp],
  props: {
    options: Object,
  },
  mounted() {
    console.log("chartData, opciones", this.chartData, this.options)
    this.renderChart(this.chartData, this.options)
  }
}
</script>
