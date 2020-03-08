import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/main.vue";
import Survey from "../views/Survey.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "main",
    component: Home
  },
  {
    path: "/survey",
    name: "Survey",
    component: Survey
  }
];

const router = new VueRouter({
  mode: "history",
  //base: process.env.BASE_URL,
  routes
});

export default router;
