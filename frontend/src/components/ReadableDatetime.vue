<script setup lang="ts">
import { useLiveClock } from "@/composables/useLiveClock";
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

defineProps<{ dt?: string }>();

const { tick } = useLiveClock();
</script>

<template>
  <span v-if="!dt" class="text-muted">—</span>
  <span v-else :title="getLocalDatetime(dt)" :data-tick="tick">
    {{ getHumanizedRelativeTime(dt) }}
  </span>
</template>
