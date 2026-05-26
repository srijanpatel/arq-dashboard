<script setup lang="ts">
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

defineProps<{ cachedAt: string }>();
</script>

<template>
  <p class="text-muted text-sm mt-sm">
    Cached at {{ getLocalDatetime(cachedAt) }} ({{ getHumanizedRelativeTime(cachedAt) }})
  </p>
</template>
