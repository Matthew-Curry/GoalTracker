<template>
  <div v-if="showChart">
    <div style="border-style: double; height: 350px; width: 700px; position: relative">
      <h1 style = "font-size: 25x">Weights vs. Performance</h1>
      <div style="float: left; height: 250px; margin-left: 20px">
        <vue-apex-charts width="325" height = "325" type="donut" :options="currOptions" :series="currSeries"></vue-apex-charts>
      </div>
      <div style="float: right; height: 250px; margin-left: 20px">
        <vue-apex-charts
          ref="realTimeChart"
          height = "325"
          width="325"
          type="donut"
          :options="prevOptions"
          :series="pastSeries"
        ></vue-apex-charts>
        </div>
        <div id="myDIV" style = "position: absolute; bottom: 10px">
          <button @click="togglePeriod(1)" :class="{btn: true, active: pastWeek}">Past Week</button>
          <button @click="togglePeriod(2)" :class="{btn: true, active: past30}">Past 30 days</button>
          <button @click="togglePeriod(3)" :class="{btn: true, active: past60}">Past 60 days</button>
          <button @click="togglePeriod(4)" :class="{btn: true, active: past90}">Past 90 days</button>
          <button @click="togglePeriod(5)" :class="{btn: true, active: pastStart}">Since Start</button>
        </div>
    </div>
  </div>
</template>

<script>
//api service
import { apiService } from "../../common/api.service";

//the chart
import VueApexCharts from "vue-apexcharts";

export default {
  name: "PieChartView",
  components: { VueApexCharts },
  data() {
    return {
      //data for the chart
      currSeries: [],
      pastSeries: [],
      currOptions: { chart: { id: "current" }, labels: [] },
      prevOptions: { chart: { id: "previous" }, labels: [] },
      //boolean for whether to show the chart
      showChart: false,
      //to hold the different data in objects
      past_data: {
        past_week: {},
        past_30: {},
        past_60: {},
        past_90: {},
        since_start: {}
      },
      //booleans for the different classes
      pastWeek: false,
      past30: false,
      past60: false,
      past90: false,
      pastStart: false
    };
  },
  //on creation, get data from the api
  async created() {
    //await on the setting of data
    await this.getPieData();
    //show data
    this.showChart = true;
    this.$emit("pieDone")
  },

  methods: {
    //get data
    async getPieData() {
      const endpoint = "/api/analytics/pieChart/";
      const method = `GET`;
      return apiService(endpoint, method).then(data => {
        for (const period in data) {
          if (period === "current") {
            this.currOptions["labels"] = Object.keys(data[period]);
            this.currSeries = Object.values(data[period]);
          } else if (period === "past_week") {
            this.prevOptions["labels"] = Object.keys(data[period]);
            this.pastSeries = Object.values(data[period]);
            this.past_data[period] = data[period];
          } else {
            this.past_data[period] = data[period];
          }
        }
      });
    },

    togglePeriod(val) {
      if (val === 1) {
        this.$refs.realTimeChart.updateSeries(
          Object.values(this.past_data.past_week, true)
        );
        this.$refs.realTimeChart.updateOptions({
          labels: Object.keys(this.past_data.past_week)
        });

        this.pastWeek = true;
        this.past30 = false;
        this.past60 = false;
        this.past90 = false;
        this.pastStart = false;
      } else if (val === 2) {
        this.$refs.realTimeChart.updateSeries(
          Object.values(this.past_data.past_30, true)
        );
        this.$refs.realTimeChart.updateOptions({
          labels: Object.keys(this.past_data.past_30)
        });

        this.pastWeek = false;
        this.past30 = true;
        this.past60 = false;
        this.past90 = false;
        this.pastStart = false;
      } else if (val === 3) {
        this.$refs.realTimeChart.updateSeries(
          Object.values(this.past_data.past_60, true)
        );
        this.$refs.realTimeChart.updateOptions({
          labels: Object.keys(this.past_data.past_60)
        });

        this.pastWeek = false;
        this.past30 = false;
        this.past60 = true;
        (this.past90 = false), (this.pastStart = false);
      } else if (val === 4) {
        this.$refs.realTimeChart.updateSeries(
          Object.values(this.past_data.past_90, true)
        );
        this.$refs.realTimeChart.updateOptions({
          labels: Object.keys(this.past_data.past_90)
        });

        this.pastWeek = false;
        this.past30 = false;
        this.past60 = false;
        this.past90 = true;
        this.pastStart = false;
      } else {
        this.$refs.realTimeChart.updateSeries(
          Object.values(this.past_data.since_start, true)
        );
        this.$refs.realTimeChart.updateOptions({
          labels: Object.keys(this.past_data.since_start)
        });

        this.pastWeek = false;
        this.past30 = false;
        this.past60 = false;
        this.past90 = false;
        this.pastStart = true;
      }
    }
  }
};
</script>

<style>
/* Style the buttons */
.btn {
  border: none;
  outline: none;
  padding: 10px 16px;
  background-color: #f1f1f1;
  cursor: pointer;
}

/* Style the active class (and buttons on mouse-over) */
.active,
.btn:hover {
  background-color: #666;
  color: white;
}
</style>