<script setup lang="ts">
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

defineProps<{ dt?: string }>();
</script>

<template>
  <div v-if="!dt">
    <p>-</p>
  </div>
  <div v-else>
    <p>{{ getLocalDatetime(dt) }}</p>
    <p>({{ getHumanizedRelativeTime(dt) }})</p>
  </div>
</template>
