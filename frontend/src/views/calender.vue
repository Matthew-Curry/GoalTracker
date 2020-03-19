<template>
    <div v-if = "isReady">
        <h1>Record of Scores-Click to see more detail!</h1>
        <Fullcalendar :plugins = "calendarPlugins" :events = "EVENTS" @datesRender = 'loadScores' />
    </div>
</template>

<script>
//calender styling
require('@fullcalendar/core/main.min.css')

//calendar imports
import Fullcalendar from '@fullcalendar/vue'
import DayGridPlugin from '@fullcalendar/daygrid'
import TimeGridPlugin from '@fullcalendar/timegrid'
import InteractionPlugin from '@fullcalendar/interaction'
import ListPlugin from '@fullcalendar/list'

//api service
import { apiService } from "../common/api.service";
export default{
    name: "calender",
    components: {Fullcalendar},
    data(){
        return{
            //the plugins needed for the full calender to be rendered
            calendarPlugins: [
                DayGridPlugin,
                TimeGridPlugin,
                InteractionPlugin,
                ListPlugin
            ],
            //the list of events built from the total scores for the current month
            EVENTS: [],
            //list of months with already rendered goals
            months: [],
            //boolean for whether API data has been gathered
            isReady: true

        }
    },
    methods:{
        loadScores(arg){
            //the month and year argument to supply to the endpoint
            var month = arg['view']['title']
            month = month.split(" ")
            //if you already rendered goals for this month, do not connect to the api
            if(this.months.indexOf(month[0]) === -1){
                //build the url, mark month to prevent another rerender, get total scores
                let endpoint = `/api/totalScore/list/?month=` + month[0]+ '+' +month[1]
                this.months.push(month[0])
                this.getTotalScores(endpoint)
            }
        },

        getTotalScores(endpoint){
            //getting data
            const method = 'GET'
            //get all total scores for this month. Loop is async so as to wait for API service
            const whileLoop = async() =>{
            while(endpoint !=null){
            //process the key value pairs
            await apiService(endpoint, method).then(data =>{
              var results = data['results']
              for(var i = 0; i < results.length; i++){
                var id = results[i]['id']
                //the components of the list
                var total_score = results[i]['total_score']
                var date = results[i]['date']
                //the event object for this score
                var event_obj = {
                    'id': id,
                    'allDay': true,
                    'start': date,
                    'title': total_score
                }
                //append to the list of events
                this.EVENTS.push(event_obj)
              }
            //move to next
            endpoint = data['next'];
          })
        }


        }
        whileLoop()
        }
    }
}
</script>