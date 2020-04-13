<template>
  <div>
      <h1>Analytics</h1>
      <br>
      <h1 v-if = "!pie">Loading...</h1>
      <div v-show = "pie" style="float: left; margin-left: 20px; margin-right:30px">
        <TimeChartView @timeDone = "time = true"/>
      </div>
      <div style = "float: left; margin-left: 20px">
        <PieChartView @pieDone = "pie = true"/>
      </div>
      <div v-show = "pie" style="float:right; margin-right: 20px">
        <ProbView @probDone = "prob = true"/>
      </div>
    </div>
</template>

<script>
//the analytics components
import TimeChartView from "../components/analytics_components/time_chart.vue";
import PieChartView from "../components/analytics_components/pie_chart.vue";
import ProbView from "../components/analytics_components/prob_view.vue";

export default {
  name: "analytics",
  components: { TimeChartView, PieChartView, ProbView },
  data() {
    return {
      //keeps track if components are done
      time: false,
      pie: false,
      prob: false
    };
  },

  method:{

  }
};
</script>