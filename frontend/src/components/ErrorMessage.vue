<script setup lang="ts">
import "vue-json-pretty/lib/styles.css";

import VueJsonPretty from "vue-json-pretty";

defineProps<{
  error: { response?: { data?: unknown } } | unknown;
}>();
</script>

<template>
  <div class="notification notification-danger mb-md">
    <p><strong>Something went wrong</strong></p>
  </div>
  <div
    v-if="error && typeof error === 'object' && 'response' in error && (error as any).response?.data"
    class="code-block"
  >
    <VueJsonPretty :data="(error as any).response.data" />
  </div>
  <p v-else class="text-muted">{{ error }}</p>
</template>
