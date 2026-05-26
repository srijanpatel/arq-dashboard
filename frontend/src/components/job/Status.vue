<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ status: string }>();

const tagClass = computed(() => {
  const map: Record<string, string> = {
    deferred: "tag-info",
    queued: "tag-neutral",
    in_progress: "tag-accent",
    complete: "tag-success",
    not_found: "tag-warning",
  };
  return map[props.status] || "tag-neutral";
});
</script>

<template>
  <span class="tag" :class="tagClass">{{ status }}</span>
</template>
