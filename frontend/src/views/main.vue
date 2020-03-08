<template>
  <div class="main">
    <img alt="Vue logo" src="../assets/logo.png" />
    <h1>This is the Home Page</h1>
  </div>
</template>

<script>
// @ is an alias to /src
import { apiService } from "../common/api.service";
export default {
  name: "main",
  data() {
    return {
      userId: null
    };
  },
  //the created method, uses user email to query if user has goal
  created() {
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
  }
};
</script>
