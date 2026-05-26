<script setup lang="ts">
import Navbar from "@/components/Navbar.vue";
</script>

<template>
  <Navbar />
  <section class="section is-medium">
    <div class="container">
      <router-view />
    </div>
  </section>
</template>
