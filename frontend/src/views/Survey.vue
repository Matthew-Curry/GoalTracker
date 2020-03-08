<template >
  <div>
    <h1>Survey</h1>
    <div >
      <SelectCategories v-show = "select === true" @selectClicked = 'selectToAssign'>
          
      </SelectCategories>
    </div>

      <AssignPoints v-show = "assign === true" :prio_ = "prio" @submitPoints = 'assignToAdd'>
        
      </AssignPoints>
  
    <div>
      <AddGoals v-show = "add === true" :prio_ = "prio" @addedGoals = "getGoals">
        
      </AddGoals>
    </div>
  </div>
</template>

<script>
//import the used components
import SelectCategories from '../components/select_categories.vue';
import AssignPoints from '../components/assign_points.vue';
import AddGoals from '../components/add_goals.vue';
import {apiService} from "@/common/api.service.js"

export default {
  name: "Survey",
  components: {
    SelectCategories,
    AssignPoints,
    AddGoals
  },
  data(){
    return{
      select :true,
      assign : false,
      add : false,
      //for now an empty array to hold the array passed from select cateogories
      prio: [],
      //an array to hold the points assigned
      userInput: [],
      //the list of the user's goals
      user_goals: [],
      //the current user's id
      requestUserId: ''
    }
  },
  methods:{
    //methods to change booleans to transition to displaying component to assing points
    selectToAssign(value){
      //get the prio array from select categories
      this.prio = value
      //change the booleans to effect conditional rendering
      this.select = false
      this.assign = true
    },
    //method to transtion from assign to add component displays
    assignToAdd(value){
      //get the user point values
      this.userInput = value
      //change the booleans to effect conditional rendering
      this.assign = false
      this.add = true
    },
    //method to get the Goals from "add_goals" and then set the weight property and convert all "on" to a boolean value of true
    getGoals(goal_list){
      //iterate over the goal list, add the weight of the goal, and also make all "on" = true for day categories
      for(var i = 0; i<goal_list.length; i++){
        //a list of all of this goal's keys
        var keys = Object.keys(goal_list[i])
        //make all "on" = true for days, else false
        for(var j = 0; j<keys.length; j++){
          if(goal_list[i][keys[j]] === 'on'){
            goal_list[i][keys[j]] = true
          }else if(goal_list[i][keys[j]] === ''){
            goal_list[i][keys[j]] = false
          }
        }
        //get the index of the prio array that matches the goal's category
        var weight_index = '';
          for(var z = 0; z < this.prio.length; z++){
            //if the values are equal, store the index
            if(this.prio[z] === goal_list[z]["category"]){
              weight_index = z
            }
            //use the weight index to get the weight for the goal
            var w = this.userInput[weight_index]
            //assign the weight to the goal
            goal_list[i]["weight"] = w;
          }

        }
      //assign the goals to the global var
      this.user_goals = goal_list
      //to hide the assign prop
      this.add = false;
      //a method to post the now properly formatted goals
      this.postGoals()
    },
    
    //a method to post the goals after they have been properly formated
    postGoals(){
      //the endpoint and method to use with the API
      let endpoint = '/api/goal/create/';
      let method = 'POST';
      //iterate over the goals and post
      for(var i = 0; i < this.user_goals.length; i++){
        console.log(this.user_goals[i])
        apiService(endpoint, method, this.user_goals[i])
    }
  }
  }
};
</script> 
