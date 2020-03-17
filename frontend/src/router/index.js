import Vue from "vue";
import VueRouter from "vue-router";
import ScoreToday from "../views/ScoreToday.vue";
import Survey from "../views/Survey.vue";
import analytics from "../views/analytics.vue";
import calender from "../views/calender.vue";
import weekly from "../views/weekly.vue";

Vue.use(VueRouter);

const routes = [
  //path to main page, enter scores today
  {
    path: "/",
    name: "ScoreToday",
    component: ScoreToday
  },
  //path to calender page, see progress
  {
    path: "/calender",
    name: "calender",
    component: calender
  },
  //path to analytics page, see analysis of performance
  {
    path: "/analytics",
    name: "analytics",
    component: analytics
  },
  //path to weekly report, force routed after enter scores on 7th day
  {
    path: "/weekly",
    name: "weekly",
    component: weekly
  },
  //path to the survey, force routed if user has no goals
  {
    path: "/survey",
    name: "Survey",
    component: Survey
  },
];

const router = new VueRouter({
  mode: "history",
  //base: process.env.BASE_URL,
  routes
});

export default router;
