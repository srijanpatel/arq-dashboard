<script setup lang="ts">
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

defineProps<{ dt?: string }>();
</script>

<template>
  <span v-if="!dt" class="text-muted">—</span>
  <span v-else :title="getLocalDatetime(dt)">
    {{ getHumanizedRelativeTime(dt) }}
  </span>
</template>
