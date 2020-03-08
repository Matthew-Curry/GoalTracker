<template>
  <div id="app">
      <router-view />
  </div>
</template>

<script>
import {apiService} from "@/common/api.service.js"
export default {
  name: "App",

  components: {
  },
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
