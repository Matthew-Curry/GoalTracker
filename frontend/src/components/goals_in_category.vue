<template>
  <div>
    <h1>{{category}}:</h1>
    <div v-for="(goal_attr, index) in goal_list" :key="index" :index="index">
      <label for="1">{{goal_attr[0]}}:</label>
      <input
        id="1"
        :placeholder="goal_attr[1]"
        type="number"
        min="0"
        onkeypress="return event.charCode >= 48"
        v-on:input="placeInput(goal_attr[4], goal_attr[3], $event.target.value)"
      />
      {{goal_attr[2]}} (goal: {{goal_attr[3]}})
      <br />
      <br />
    </div>
  </div>
</template>

<script>
export default {
  name: "GoalsInCategory",
  props: {
    //the catgory to display
    category: {
      type: String,
      required: true
    },
    //list is in form goal, goal id, measure, unit
    goal_list: {
      type: Array,
      required: true
    },
    //a boolean for whether or not submit was clicked in main component
    submit_checked: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      //user input for scores
      userInput: {}
    };
  },

  //watch the submit_checked, if true emit the user input to the main component
  watch: {
    submit_checked: function() {
      if (this.submit_checked === true) {
        setTimeout(() => {
          this.$emit("submitToReview", this.userInput);
        }, Math.random() * 1000);
      }
    }
  },
  methods: {
    //method to store the user input in an object
    placeInput(score_id, max, value) {
      this.userInput[score_id] = [value, max];
    }
  }
};
</script>