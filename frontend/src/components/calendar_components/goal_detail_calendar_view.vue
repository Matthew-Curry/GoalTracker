<template>
  <div>
    <modal height="auto" name="pop">
      <template v-if = "isReady">
        <h1>Individual Scores:</h1>
        <div v-for= "(value, key) in ind_goals" :key= "key">
          <h1>{{key}}: {{value}}</h1>
        </div>
        <button @click= "tearDown">close</button>
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
      isReady: false,
    };
  },
  //when created, use the id to access indivdual scores for that day
  async created() {
    //builds mapping of goal ids to individual score
    await this.loadDetailViewInfo();
    //iterates over mapping of goal its to individual score and makes into mapping of goals to scores
    await this.mapGoalsToScores();
    //once info is gathered, can display
    await this.displayModal()
  },

  methods: {
    //a method to retrieve indidivual goals for the passing in id
    async loadDetailViewInfo() {
      //the endpoint and method for the request
      var endpoint = `/api/score/list/?id=` + this.id;
      const method = "GET";
      //get the info
      const whileLoop = async () => {
        while (endpoint != null) {
          //build mapping from goal ids to individual scores
          await apiService(endpoint, method).then(data => {
            var results = data["results"];
            for (var i = 0; i < results.length; i++) {
              //id and score
              var goal_id = results[i]["goal"];
              var ind_score = results[i]["individual_score"];
              //append to ind_goals
              this.ind_goals[goal_id] = ind_score;
            }
            //move to next
            endpoint = data["next"];
          });
        }
      };
      return whileLoop();
    },
    //changes mapping of goal ids to scores to mapping of goals to score
    async mapGoalsToScores() {
      var endpoint = "";
      const method = "GET";
      var goal_ids = Object.keys(this.ind_goals);
      //iterate over keys of ind_goal object and access its data
      const forLoop = async () => {
        for (var i = 0; i < goal_ids.length; i++) {
            endpoint = `/api/goal/` + goal_ids[i] + `/update/`;
          await apiService(endpoint, method).then(data => {
              //get goal name, assign to entries in the id, then delete
              var goal_name = data['goal']
              this.ind_goals[goal_name] = this.ind_goals[goal_ids[i]]
              delete this.ind_goals[goal_ids[i]]
            })
          };
        }
      return forLoop()
    },
    //displays the modal container when the information after it has been gathered
    async displayModal(){
        this.isReady = true
        this.$modal.show('pop')
        },
    //emit a teadown event so the parent component removes pop up
    tearDown(){
      this.$emit('tearDown')
    }
    }
    };
</script>