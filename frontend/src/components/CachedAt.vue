<script setup lang="ts">
import { useLiveClock } from "@/composables/useLiveClock";
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

defineProps<{ cachedAt: string }>();

// tick triggers re-render so .fromNow() stays fresh
const { tick } = useLiveClock();
</script>

<template>
  <p class="text-muted text-sm mt-sm" :data-tick="tick">
    Cached at {{ getLocalDatetime(cachedAt) }} ({{ getHumanizedRelativeTime(cachedAt) }})
  </p>
</template>
