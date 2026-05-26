<script setup lang="ts">
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

defineProps<{ cachedAt: string }>();
</script>

<template>
  <p class="has-text-grey">
    Cached at: {{ getLocalDatetime(cachedAt) }} ({{ getHumanizedRelativeTime(cachedAt) }})
  </p>
</template>
