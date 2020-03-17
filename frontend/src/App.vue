<template>
  <div id="app">
    <NavbarComponent v-show = "$route.path != '/survey'"></NavbarComponent>
    <router-view />
  </div>
</template>

<script>
import {apiService} from "@/common/api.service.js"
import NavbarComponent from "./components/Navbar.vue"
export default {
  name: "App",
  components: {NavbarComponent},
  methods:{
  async setUserInfo(){
      const data = await apiService("/api/accounts/");
      const requestUserId = data["id"];
      window.localStorage.setItem("requestUserId", requestUserId);
  }
  },
  created(){
    this.setUserInfo();
  }
};
</script>
