<script setup lang="ts">
import "vue-json-pretty/lib/styles.css";

import VueJsonPretty from "vue-json-pretty";

import CachedAt from "@/components/CachedAt.vue";
import type { CachedJob } from "@/types";

defineProps<{ job: CachedJob }>();
</script>

<template>
  <h2 class="is-size-2 mb-4">{{ job.jobId }}</h2>
  <div class="wrapper">
    <VueJsonPretty :data="(job as any)" />
  </div>
  <CachedAt :cached-at="job.cachedAt" />
</template>

<style scoped>
.wrapper {
  background-color: rgb(246, 248, 250);
  padding: 10px;
}
</style>
