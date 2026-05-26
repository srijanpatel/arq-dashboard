<script setup lang="ts">
import Navbar from "@/components/Navbar.vue";
</script>

<template>
  <Navbar />
  <main class="section">
    <div class="container">
      <router-view />
    </div>
  </main>
</template>
