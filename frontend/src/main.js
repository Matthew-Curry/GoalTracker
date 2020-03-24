import Vue from "vue";
import App from "./App.vue";
import router from "./router";
//import modal from 'vue-js-modal'
import VModal from 'vue-js-modal'

Vue.config.productionTip = false;
//Vue.use(VModal, {dialog: true, dynamic:true})
Vue.use(VModal)

new Vue({
  router,
  //vuetify,
  render: h => h(App)
}).$mount("#app");
