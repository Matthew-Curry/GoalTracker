<template>
  <div>
    <div v-if = "isReady" style = "position: relative">
    <div style="border-style: double; width: 500px; height: 350px">
      <h1>Probabilites:</h1>
      {{dayMostStr}}
      <br>{{dayLeastStr}}
      <br>{{catMostStr}}
      <br>{{catLeastStr}}
    </div>
    </div>
    <div>
  </div>
  </div>
</template>

<script>
//api service
import { apiService } from "../../common/api.service";

export default {
  name: "ProbView",
  data() {
    return {
      //hold the probabilities for each case
      dayMostProb: null,
      dayLeastProb: null,
      catMostProb: null,
      catLeastProb: null,
      //hold lists for each case
      dayMostList: null,
      dayLeastList: null,
      catMostList: null,
      catLeastList: null,
      //the strings to use
      dayMostStr: null,
      dayLeastStr: null,
      catMostStr: null,
      catLeastStr: null,
      //boolean for ready
      isReady: false
    };
  },
  //get the data
  async created() {
    await this.getProbData();
    //format the list strings

    this.dayMostStr = this.formatListStr(
      this.dayMostList,
      this.dayMostProb,
      "Day",
      "most"
    );
    this.dayLeastStr = this.formatListStr(
      this.dayLeastList,
      this.dayLeastProb,
      "Day",
      "least"
    );
    this.catMostStr = this.formatListStr(
      this.catMostList,
      this.catMostProb,
      "Category",
      "most"
    );
    this.catLeastStr = this.formatListStr(
      this.catLeastList,
      this.catLeastProb,
      "Category",
      "least"
    );

    this.isReady = true
    this.$emit("probDone")
  },

  methods: {
    //get data
    async getProbData() {
      const endpoint = "/api/analytics/probs/";
      const method = `GET`;
      return apiService(endpoint, method).then(data => {
        console.log(data);
        //assign probablities
        this.dayMostProb = data["dayMost"].shift();
        this.dayLeastProb = data["dayLeast"].shift();
        this.catMostProb = data["catMost"].shift();
        this.catLeastProb = data["catLeast"].shift();
        //the lists
        this.dayMostList = data["dayMost"];
        this.dayLeastList = data["dayLeast"];
        this.catMostList = data["catMost"];
        this.catLeastList = data["catLeast"];
      });
    },

    formatListStr(list, prob, unit, dir) {
      console.log("in the format str");
      if (list.length === 1) {
        var the_str =
          unit +
          " " +
          dir +
          " likely to complete: " +
          list[0] +
          " (" +
          prob +
          "%" +
          ")";
      } else {
        if (unit === "Day") {
          unit = "Days";
        } else if (unit === "Category") {
          unit = "Categories";
        }
        var day_str = "";
        for (var i = 0; i < list.length; i++) {
          //if next item is last, append and, else append ,
          if (i === list.length - 2) {
            day_str = day_str + list[i] + " and ";
          } else if (i === list.length - 1) {
            day_str = day_str + list[i];
          } else {
            day_str = day_str + list[i] + ",";
          }
        }
        the_str =
          unit +
          " " +
          dir +
          " likely to complete: " +
          day_str +
          " (" +
          prob +
          "%" +
          ")";
      }
      return the_str;
    }
  }
};
</script>