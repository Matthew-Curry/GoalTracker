<template>
  <div class="ScoreToday">
    <h1>Scores Today:</h1>
    <div v-if="goalByCatReady">
      <div v-for="value in catList" :key="value">
        <GoalsInCategory
          :category="value"
          :goal_list="goalByCat[value]"
          :submit_checked="submitClicked"
          @submitToReview="checkInput"
        ></GoalsInCategory>
      </div>
      <button @click="toggleClicked">Submit Scores</button>
    </div>
    <h1 v-if="noInputError">There is no input for a goal</h1>
  </div>
</template>

<script>
// @ is an alias to /src
import { apiService } from "../common/api.service";
//the component to show goals for a catagory
import GoalsInCategory from "../components/goals_in_category.vue";
export default {
  name: "ScoreToday",
  components: { GoalsInCategory },
  data() {
    return {
      //list of categories obtained
      catList: [],
      //boolean when ready
      goalByCatReady: false,
      //new data structure obtained from the new endpoint
      goalByCat: {},
      //a count of the inputs recieved
      countInput: 0,
      //boolean for whether or not submit button has been pressed
      submitClicked: false,
      //HOLD ALL USER INPUT
      holdAllInput: {}
    };
  },
  //the created method, uses user email to query if user has goal
  async created() {
    //if user has no goals, send to survey page
    await this.checkGoals();
    //gather appropriate information to display
    await this.getGoalbyCat();
  },

  methods: {
    //method that checks if the user has no goals, and if so sends to survey page
    checkGoals() {
      //if user has no goals, send to survey page
      let endpoint = `/api/goal/list/`;
      apiService(endpoint).then(data => {
        //if empty, move to survey page
        if (data.count === 0) {
          this.$router.push({
            name: "Survey"
          });
        }
      });
    },

    //method that obtains goals by every category
    async getGoalbyCat() {
      let endpoint = `/api/endpoints/ScoreToday/`;
      const method = "GET";

      await apiService(endpoint, method).then(data => {
        this.goalByCat = data;
        this.catList = Object.keys(this.goalByCat);
      });

      this.goalByCatReady = true;
    },

    //a method that toggles the submitClicked boolean, causing all the components to emit input which can then be verified and submited
    toggleClicked() {
      //if errors are currently displayed, get rid of them
      this.greaterThanMax = false;
      //set submit clicked to true to cause component to send in data
      this.submitClicked = true;
    },

    //a method to check input. Verfies that all goals have a non zero score, caps score at max amount
    checkInput(userInput) {
      //list of score keys
      var score_keys = Object.keys(userInput);
      //check if there is no input for a goal, or that the value inputted is greater than the max
      for (var i = 0; i < score_keys.length; i++) {
        //get the value
        var val = userInput[score_keys[i]][0];
        //get the max
        var max = userInput[score_keys[i]][1];
        //if val is greater than max, change val to max
        if (val > max) {
          userInput[score_keys[i]][0] = max;
          break;
        }
      }
      //if all goals are inputted, append userInput to overall input of scores and call method to submit
      this.countInput = this.countInput + 1;
      //this.holdAllInput.push(userInput)
      this.holdAllInput = { ...this.holdAllInput, ...userInput };
      this.submitScores();
      //toggle variable that check has been performed to false
      this.submitClicked = false;
    },

    //a method that checks that all goals_in_category components have submitted scores, and if so submits
    submitScores() {
      //empty list
      var list_ = [];
      //length of overall scores should be equal to the number of components, or categories created
      if (this.countInput === this.catList.length) {
        //iterate over scores to add to list to add
        var score_ids = Object.keys(this.holdAllInput);
        for (var i = 0; i < score_ids.length; i++) {
          var score_id = score_ids[i];
          var ind_score = this.holdAllInput[score_id][0];

          list_.push({ individual_score: ind_score, id: score_id });
        }

        let endpoint = `/api/score/update/`;
        let method = "PATCH";
        //wait for the post to process
        const waitAPI = async () => {
          await apiService(endpoint, method, list_);
        };
        waitAPI();
        //after all updates, refresh the page
        window.location.reload();
      }
    }
  }
};
</script>