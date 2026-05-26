<script setup lang="ts">
import "vue-json-pretty/lib/styles.css";

import VueJsonPretty from "vue-json-pretty";

defineProps<{
  error: { response?: { data?: unknown } } | unknown;
}>();
</script>

<template>
  <div class="notification is-danger is-light">
    <p>Something went wrong...</p>
  </div>
  <div
    v-if="error && typeof error === 'object' && 'response' in error && (error as any).response?.data"
    class="wrapper"
  >
    <VueJsonPretty :data="(error as any).response.data" />
  </div>
  <p v-else>{{ error }}</p>
</template>

<style scoped>
.wrapper {
  background-color: rgb(246, 248, 250);
  padding: 10px;
}
</style>
