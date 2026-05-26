<script setup lang="ts"></script>

<template>
  <nav role="navigation" aria-label="main navigation" class="navbar is-fixed-top">
    <div class="navbar-brand">
      <a class="navbar-item"><h1 class="title">ARQ Dashboard</h1></a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start"></div>
      <div class="navbar-end">
        <router-link class="navbar-item" :to="{ name: 'stats' }">Stats</router-link>
        <router-link class="navbar-item" :to="{ name: 'jobs' }">Jobs</router-link>
        <router-link class="navbar-item" :to="{ name: 'setting' }">Setting</router-link>
        <a class="navbar-item" href="/redoc" target="_blank">API</a>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  border-bottom: 1px solid lightgray;
}
</style>
