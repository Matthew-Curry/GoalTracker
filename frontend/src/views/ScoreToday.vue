<template>
  <div class="ScoreToday">
    <h1>Scores Today:</h1>
    <div v-if = "goalToScoreReady && goalToCatReady">
    <div v-for = "value in catList" :key = value>
    <GoalsInCategory :category = value :goal_list = catToGoal[value] :current_scores = goalToScore :submit_checked = submitClicked @submitToReview = "checkInput">
    
    </GoalsInCategory>
    </div>
    <button @click = "toggleClicked">Submit Scores</button>
    </div>
    <h1 v-if = "noInputError">There is no input for a goal</h1>
  </div> 
</template>

<script>
//show goals for the day, input field to tie to the score

//what information do i need to show from a goal?
//at top, total score

//category header
//all goals in that category
//input field/score


// @ is an alias to /src
import { apiService } from "../common/api.service";
//the component to show goals for a catagory
import GoalsInCategory from "../components/goals_in_category.vue"
export default {
  name: "ScoreToday",
  components: {GoalsInCategory},
  data() {
    return {
      //the id of the user
      userId: null,
      //mapping of goal keys to a list holding the score id then the score
      goalToScore: {},
      //a list of goal ids
      goalIdList: [],
      //categories mapped to goal info
      catToGoal: {},
      //list of categories obtained
      catList: [],
      //initial endpoint to get individual scores today
      score_endpoint: `/api/score/list/today/`,
      //intial endpoint to get goals for the day
      goal_endpoint: `/api/goal/list/today/`,
      //keeps track of whether or not goal 
      goalToScoreReady: false,
      //keeps track of whether or not goal to category mapping has been recieved from the API
      goalToCatReady: false,
      //boolean for whether or not submit button has been pressed
      submitClicked: false,
      //a boolean for whether or not to display an error for no input for a goal
      noInputError: false,
      //HOLD ALL USER INPUT
      holdAllInput: []


  }
  },
  //the created method, uses user email to query if user has goal
  async created(){
    //if user has no goals, send to survey page
    await this.checkGoals()
    //display goals and input fields for that day
    await this.buildGoalToScore()
    //build mapping of categories to goals, only call when length of goal id list is not 0
    await this.buildCatToGoal()
  //after created (data is gathered) can use mounted hook to 
  },
  methods:{
    //method that checks if the user has no goals, and if so sends to survey page
    checkGoals(){
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

    //a method that fills the object mapping goal keys to a list that holds the score id and the score currently
    buildGoalToScore(){
      //get method
      let method = 'GET';
      //loop in async function for use of await
      const whileLoop = async() =>{
      while(this.score_endpoint !=null){
        //process the key value pairs
        await apiService(this.score_endpoint, method).then(data =>{
            var results = data['results']
            //iterate over results array
            for(var i = 0; i < results.length; i++){
              var goalKey = results[i]['goal']
              //the components of the list
              var scoreKey = results[i]['id']
              var ind_score = results[i]['individual_score']
              this.goalToScore[goalKey] = [scoreKey, ind_score]
              this.goalIdList.push(goalKey)
            }
            //move to next
            this.score_endpoint = data['next'];
      })
        }
        this.goalToScoreReady = true
      }
      whileLoop()
      },
    
      //uses endpoint that has all goals today to build map of catagories to goal info
      buildCatToGoal(){
        //get method
        let method = 'GET';
        //loop in async function for use of await
        const whileLoop = async() =>{
        while(this.goal_endpoint !=null){
          //process the key value pairs
          await apiService(this.goal_endpoint, method).then(data =>{
              var results = data['results']
              //iterate over results array
              for(var i = 0; i < results.length; i++){
                var catKey = results[i]['category']
                //append to list of categories, if not present
                if(this.catList.indexOf(catKey) === -1){
                this.catList.push(catKey)
                }
                var goal = results[i]["goal"]
                var id = results[i]["id"]
                var measure = results[i]["measure"]
                var unit = results[i]['unit']
                //if catkey does not exists, append list with this instance of features
                if (Object.keys(this.catToGoal).indexOf(catKey) === -1){
                  this.catToGoal[catKey] = [[goal, id, measure, unit]]
                }//otherwise, push to the existsing list
                else{
                  this.catToGoal[catKey].push([goal, id, measure, unit])
                }
                
              }
            //move to next
            this.goal_endpoint = data['next'];
          })
        }
        this.goalToCatReady = true
      }
      whileLoop()
    },
      //a method that toggles the submitClicked boolean, causing all the components to emit input which can then be verified and submited
      toggleClicked(){
        //if errors are currently displayed, get rid of them
        this.greaterThanMax = false
        this.noInputError = false
        //set submit clicked to true to cause component to send in data
        this.submitClicked = true
      },
      //a method to check input. Verfies that all goals have a non zero score, caps score at max amount
      checkInput(userInput, numGoals){
        //list of goal keys to iterate over
        var goal_ids = Object.keys(userInput)
        //show error if no goals
        if(numGoals ===0){
            this.noInputError = true
          }//else go through goals
        else{
        //check if there is no input for a goal, or that the value inputted is greater than the max
        for(var i =0; i < goal_ids.length; i++){
          //get the value
          var val = userInput[goal_ids[i]][0]
          //if value is 0, raise error and break
          if(val ===0){
            this.noInputError = true
            break
          }
          //get the max
          var max = userInput[goal_ids[i]][1]
          //if val is greater than max, change val to max
          if(val > max){
            userInput[goal_ids[i]][0] = max
            break
          }
        }
        //if all goals are inputted, append userInput to overall input of scores and call method to submit
        if(this.noInputError ===false){
          this.holdAllInput.push(userInput)
          this.submitScores()}
        //otherwise reset submit clicked so user can try again
        else{
          //once input is checked, toggle variable that check has been performed to false
          this.submitClicked = false
        }
      }
      },
      //this.goalToScore[goalKey] = [scoreKey, ind_score]

      //a method that checks that all goals_in_category components have submitted scores, and if so submits
      submitScores(){
        //length of overall scores should be equal to the number of components, or categories created
        if(this.holdAllInput.length === this.catList.length){
          //console.log('you would submit here with holdAllInput object, should be on console once')
          //iterate over the the inputs from each goal category
          for(var i = 0; i < this.holdAllInput.length; i++){
            //get the input from that category
            var cat_input = this.holdAllInput[i]
            //the ids
            var goal_ids = Object.keys(cat_input)
            //iterate over goals, use goalToScore to map to score id
            for(var j = 0; j<goal_ids.length; j++){
              //the score to put
              var ind_score = cat_input[goal_ids[j]][0]
              ind_score = parseInt(ind_score)
              //get the score id
              var score_id = this.goalToScore[goal_ids[j]][0]
              //use the score id to build the right endpoint
              let endpoint = `/api/score/` + parseInt(score_id) + `/update/`
              //the method
              let method = "PUT"
              //connect to the endpoint and update the goal
              apiService(endpoint, method, {'individual_score': ind_score })
            }
          }
          //after all updates, refresh the page
          window.location.reload()
        }
      }
    }
  };
</script>