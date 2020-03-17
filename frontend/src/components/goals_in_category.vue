<template>
<div>
    <h1>{{category}}:</h1>
    <div v-if = "doneFill">
    <div v-for = "(goal_attr, index) in goal_list" :key = "index" :index = "index">
        <!--<div v-if = "this.current_scores[goal_attr[0]][1] != 0">-->
        <!--<div v-if = "goalToCurrentScore[goal_attr[0]][0] === 0">-->
        <label for = 1>{{goal_attr[0]}}:</label>
        <input id = 1 :placeholder = "[[ goalToCurrentScore[goal_attr[0]][0] ]]" type = "number" min = "0" onkeypress="return event.charCode >= 48" v-on:input = "placeInput(goal_attr[1], goal_attr[2], $event.target.value)"> {{goal_attr[3]}} (goal: {{goal_attr[2]}})
        <br>
        <br>
        </div>
        <!--<div v-else>
            <p>{{goal_attr[0]}}: {{goalToCurrentScore[goal_attr[0]][0]}} {{goalToCurrentScore[goal_attr[0]][1]}} </p>
        </div> -->
    </div>
    <!--</div>-->
</div>
</template>

<script>
//on created, iterate through goals

//object where keys are goals

//use key from goal list to get meausrement form goal to score

//can get unit from goal object itself



export default {
    name: "GoalsInCategory",
    props:{
        //the catgory to display
        category:{
            type: String,
            required: true
        },
        //a lists of lists, where each list represents a goal to show for the category.
        //list is in form goal, goal id, measure, unit
        goal_list: {
            type: Array,
            required: true
        },
        //mapping of goals to tuple lists of score ids and individual scores. Will be filtered for current category
        current_scores:{
            type: Object,
            required:true
        },
        //a boolean for whether or not submit was clicked in main component
        submit_checked:{
            type: Boolean,
            required: true
        }
    },
    data(){
        return{
            //user input for scores
            userInput: {},
            //some booleans
            doneFill: false,
            noScore: false,
            //object that maps goals to measure and untit
            goalToCurrentScore: {}
        }
    },
    //in the created method, build object for goals mapped to current score and unit
    created(){
        //iterate over goals to build the object
        for(var i = 0; i< this.goal_list.length; i++){
            //get the goal name
            var goal = this.goal_list[i][0]
            //get the unit of measure
            var unit = this.goal_list[i][3]
            //use the key to get the current score from current_scores
            var key = this.goal_list[i][1]
            var score = this.current_scores[key][1]
            //now have all pieces, place in object
            this.goalToCurrentScore[goal] = [score, unit]
        }
        //the object is filled, can render page
        this.doneFill = true
    }, 
    //watch the submit_checked, if true emit the user input to the main component
    watch:{
        submit_checked: function(){

            if(this.submit_checked === true){
                //send in the number of goals so it can check if no goals were set
                var numGoals = Object.keys(this.userInput).length
                setTimeout(()=>{
                    this.$emit('submitToReview', this.userInput, numGoals)}, Math.random() *1000)
                
            }
        }
    },
    methods:{
        //method to store the user input in an object
        placeInput(goal_id,max,value){
            this.userInput[goal_id] = [value, max]
        }
    }
}
</script>