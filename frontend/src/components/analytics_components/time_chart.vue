<template>
  <div v-if="showChart">
    <div style="border-style: double; height: 350px; width: 500px; position: relative">
      <h1 style="font-size: 25">Total Scores Over Time</h1>
      <vue-apex-charts style = "position: absolute" v-show="delay" width="450" type="area" :options="options" :series="series"></vue-apex-charts>
    </div>
    <br>
  </div>
</template>

<script>
//api service
import { apiService } from "../../common/api.service";

//the chart
import VueApexCharts from "vue-apexcharts";

export default {
  name: "TimeChartView",
  components: { VueApexCharts },
  data() {
    return {
      //data for the chart
      series: [],
      options: {
        chart: { id: "timeChart", stacked: true, animations:{enabled: false} },
        dataLabels: { enabled: false },
        xaxis: { type: "datetime", title: { text: "Days", offsetY: 10 } },
        yaxis: { title: { text: "Total Scores" } },
        tooltip: {
          followCursor: true,
          shared: false,
          custom: function({ series, dataPointIndex }) {
            let currentTotal = 0;
            series.forEach(s => {
              currentTotal += s[dataPointIndex];
            });
            return (
              '<div class="custom-tooltip">' +
              "<span><b>Total: </b>" +
              currentTotal +
              "</span>" +
              "</div>"
            );
          }
        }
      },
      //boolean for whether to show the chart
      showChart: false,
      //delay
      delay: false
    };
  },
  //on creation, get data from the api
  async created() {
    //await on the setting of data
    await this.getTimeData();
    //show data
    this.showChart = true;
    //async timeout
    var self = this
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    async function asyncTimeOut() {
      self.delay = true
      await delay(5000);
      console.log('done')
    }
    await asyncTimeOut();
    //emit that the time chart is set up
    this.$emit("timeDone");
  },

  methods: {
    //get data
    async getTimeData() {
      const endpoint = "/api/analytics/timeChart/";
      const method = `GET`;
      return apiService(endpoint, method).then(data => {
        for (const cat in data) {
          if (cat != "days") {
            var data_ = [];
            for (var i = 0; i < data["days"].length; i++) {
              data_.push([data["days"][i], data[cat][i]]);
            }
            this.series.push({ name: cat, data: data_ });
          }
        }
      });
    }
  }
};
</script>