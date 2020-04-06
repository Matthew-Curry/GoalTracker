<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light my-navbar">
    <div class="container">
      <router-link :to="{name: 'ScoreToday'}" class="navbar-brand">Score Today</router-link>

      <router-link :to="{name: 'analytics'}" class="navbar-brand">Analytics</router-link>

      <router-link :to="{name: 'calender'}" class="navbar-brand">Calender</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavbarComponent"
};
</script>

<style>
.my-navbar {
  border-bottom: 1px solid #ddd;
}

.navbar-brand {
  font-weight: bold;
  font-size: 130%;
}

.navbar-brand:hover {
  color: #dc3545 !important;
}
</style>