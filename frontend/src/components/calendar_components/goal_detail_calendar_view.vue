<template>
  <div>
    <modal height="auto" name="pop">
      <template v-if="isReady">
        <h1>Individual Scores:</h1>
        <div v-for="(values, key) in ind_goals" :key="key">
          <h1>{{key}}: {{values[0]}} {{values[1]}}</h1>
        </div>
        <button @click="tearDown">close</button>
      </template>
    </modal>
  </div>
</template>

<script>
//api service
import { apiService } from "../../common/api.service";
//the modal component
export default {
  name: "GoalDetailView",
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      //the object containing the list of goal info from the API
      ind_goals: {},
      //is the data ready
      isReady: false
    };
  },
  //when created, use the id to access indivdual scores for that day
  async created() {
    //builds mapping of goal ids to individual score
    await this.loadDetailViewInfo();
    //once info is gathered, can display
    await this.displayModal();
  },

  methods: {
    //method to take in mapping of goal name to [score, unit]
    async loadDetailViewInfo() {
      var endpoint = `/api/endpoints/goal-to-scores/?id=` + this.id;
      const method = "GET";

      //build mapping from goal ids to individual scores
      await apiService(endpoint, method).then(data => {
        this.ind_goals = data;
      });
    },

    //displays the modal container when the information after it has been gathered
    async displayModal() {
      this.isReady = true;
      this.$modal.show("pop");
    },
    //emit a teadown event so the parent component removes pop up
    tearDown() {
      this.$emit("tearDown");
    }
  }
};
</script>