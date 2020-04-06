<template>
  <div>
    <h1 v-show="errorMessage === true">Points assigned must total 100!</h1>
    <h1 style="font-size: 27px">Points Left:</h1>
    <p style="font-size: 22px">{{points_left}}</p>
    <h1
      style="font-size: 25px"
    >Distribute 100 points to the priorities based on how important to you they are:</h1>
    <div v-for="(value, index) in prio_" :key="value">
      {{value}}
      <input
        type="number"
        min="0"
        onkeypress="return event.charCode >= 48"
        v-model="userInput[index]"
      />
    </div>
    <button @click="checkSubmit">Submit</button>
  </div>
</template>

<script>
export default {
  name: "AssignPoints",
  props: {
    prio_: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      //an array to hold the different values entered by the user
      userInput: [],
      //a boolean to display an error message
      errorMessage: false
    };
  },
  methods: {
    //a method that checks if submission is valid, then calls the emit to advance to the next page
    checkSubmit() {
      //convert all user inputs to strings
      this.convertToInt();
      //check that all numbers are positive and add up to 100
      var check = true;
      var sum = 0;
      //iterate over the array
      for (let i = 0; i < this.userInput.length; i++) {
        //the item
        var item = this.userInput[i];
        //add to overall sum
        sum = sum + item;
        //is it an integer less than 100?
        if (Number.isInteger(item) === false || item > 100) {
          check = false;
          break;
        }
      }
      //if sum is greater than 100 check false
      if (sum != 100) {
        check = false;
      }
      //if passes check call method to emit
      if (check === true) {
        this.nextPage();
      }
      //if check fails, call method to display error message and reset inputs
      else {
        this.resetInputs();
      }
    },
    //method to convert all entries in an array to numbers
    convertToInt() {
      for (var i = 0; i < this.userInput.length; i++) {
        this.userInput[i] = parseInt(this.userInput[i], 10);
      }
    },
    //method to go to the next page
    nextPage() {
      //what does overall survey page need to have?
      this.$emit("submitPoints", this.userInput);
    },

    //method to reset inputs if they don't fit needed criteria
    resetInputs() {
      this.errorMessage = true;
    }
  },
  //the points left is a computed property
  computed: {
    points_left: function() {
      //iterate over the user input and subtract from 100
      var points_left = 100;
      for (var i = 0; i < this.userInput.length; i++) {
        points_left = points_left - this.userInput[i];
      }
      //return the points left
      return points_left;
    }
  }
};
</script>
<style>
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>