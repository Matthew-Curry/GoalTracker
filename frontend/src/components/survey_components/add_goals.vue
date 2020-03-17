<template>
<div>
    <div>
        <h1 style = "font-size:25px">Add goals for each category:</h1>
        <h1 v-show = 'error1 === true'>Error, enter all fields for a new goal</h1>
        <h1 v-show = 'error2 === true'>Error, make sure you have one goal per category</h1>
    </div>
    <div v-for= "(value, index) in prio_" :key = "value">
        <button @click = 'setBoolean(index)'>Add Goal for {{value}}</button>
        <div v-show = 'booleanList[index]'>
            <label for = 1>Goal:</label>
            <input type = "text" id = 1 v-on:input = "goal = $event.target.value"/>
            <label for = 2>Measure:</label>
            <input type = "number" id = 2 v-on:input = "measure = $event.target.value" onkeypress="return event.charCode >= 48"/>
            <label for = 3>Unit:</label>
            <input type = "text" id = 3 v-on:input = "unit = $event.target.value"/>
            <!--Different Days -->
            <br>
            <input type="checkbox" id = 4 v-on:input = "mon = $event.target.value">Monday<br />
            <input type="checkbox" id = 5 v-on:input = "tues = $event.target.value">Tuesday<br/>
            <input type="checkbox" id = 6 v-on:input = "wen = $event.target.value">Wednesday<br/>
            <input type="checkbox" id = 7 v-on:input = "thurs = $event.target.value">Thursday<br/>
            <input type="checkbox" id = 8 v-on:input = "fri = $event.target.value">Friday<br/>
            <input type="checkbox" id = 9 v-on:input = "sat = $event.target.value">Saturday<br/>
            <input type="checkbox" id = 10 v-on:input = "sun = $event.target.value">Sunday<br/>

            <button @click = 'setGoalObj(value)'>Click to add Goal</button>
        </div>
    </div>
    <button @click = "checkSubmit">Final Submit Button</button>
    </div>
</template>

<script>

export default {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  name: "AddGoals",
    props:{
        prio_: {
            type: Array,
            required: true
        }
    },
    data(){
        return{
        //holds the number of index to make true
        set_true: 'not a number',
        //variables used to hold the goals as they are set
        goal: '',
        measure:'',
        unit: '',
        //the day variables
        mon: '',
        tues: '',
        wen: '',
        thurs: '',
        fri: '',
        sat: '',
        sun: '',
        //a list of goal objects to pass back to survey component
        goal_list: [],
        //variable to hold whether or not there was an error in entering goals
        error1: false,
        //variable to hold whether or not there was not a goal entered for every category
        error2: false
        }
    },
    //list of booleans for showing the different inputs for goals
    computed: {
        booleanList: function() {
            var booleanList = []
            for(var i = 0; i < this.prio_.length; i++){
                booleanList.push(false)
            }
            //if set true is a number then set the index
            if(Number.isInteger(this.set_true)){
                booleanList[this.set_true] = true
            }

            return booleanList;
        }
    },
    methods: {
        //a method that sets the index to make true
        setBoolean(index){
            //the boolean at that index is now true
            this.set_true = index;
        },
        //method to set the goal object
        setGoalObj(cat){
            //check to make sure all fields have been entered, and that the goal array is not already the full length
            var prop = true;
            if(this.goal === ''){
                prop = false
            }else if(this.measure === ''){
                prop = false
            }else if(this.unit === ''){
                prop = false
            }//at least one day should be entered
            else if(this.mon === ''
            &&this.tues === ''
            &&this.wen === ''
            && this.thurs === ''
            && this.fri === '' 
            && this.sat === ''
            && this.sun === ''){
                prop = false
            }
            //continue if the values have been entered correctly
            if(prop){
            //there should be no error
            this.error1 = false;
            //the goal object
            var goal_obj = {
                "goal":this.goal,
                "measure": this.measure,
                "unit": this.unit,
                "category": cat,
                "mon": this.mon,
                "tues": this.tues,
                "wen": this.wen,
                "thurs": this.thurs,
                "fri": this.fri,
                "sat": this.sat,
                "sun": this.sun
            }
            //
            //append to the goal list
            this.goal_list.push(goal_obj)
            //a method to clear the form presented to the user
            this.clearForm()
            }//otherwise display error message
            else{
                this.error1 = true;
            }
        },
        //method to check if all categories were given goals
        checkSubmit(){
            //reset the global boolean
            this.error2 = false
            //iterate over prio, check if a category is not used. if so, throw error
            for(var i =0; i<this.prio_.length; i++){
                var cat = this.prio_[i];
                //for this category, assume is not used
                var this_used = false
                //iterate over goals, check that it is there
                goal_iter:
                for(var j=0; j<this.goal_list.length; j++){
                    //get the category of the goal
                    var cat_goal = this.goal_list[j]["category"]
                    //check if the category of the goal is the same as cat. if so, used is true, break this loop
                    if(cat_goal ===cat){
                        this_used = true;
                        break goal_iter;
                    }
                }
                //throw error if a category not used
                if(this_used ===false){
                    this.error2 = true
                    break
                }

                    
                }
                //if there is no error set, call a method to emit the goal data to the main survey component
                this.sendGoals()
            },
            //method to send the goals to the main survey function
            sendGoals(){
                this.$emit('addedGoals', this.goal_list)
            },

            //a method to clear the form presented to the user
            clearForm(){
                var uncheck=document.getElementsByTagName('input');
                for(var i=0;i<uncheck.length;i++){
                    if(uncheck[i].type=='checkbox'){
                        uncheck[i].checked=false;
                    }//if number or text set blank
                    else{
                        uncheck[i].value = '' 
                    }   
                }
            }

        }
    }
</script>