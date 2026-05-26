<script setup lang="ts">
import { useTitle } from "@vueuse/core";
import { onMounted } from "vue";

import Stats from "@/components/stats/StatsWrapper.vue";

onMounted(() => useTitle("Stats - ARQ Dashboard"));
</script>

<template>
  <Stats />
</template>
