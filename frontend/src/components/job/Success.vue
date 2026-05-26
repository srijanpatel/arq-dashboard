<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ success: boolean; status: string }>();

const tagClass = computed(() => {
  if (props.status === "complete") {
    return props.success ? "tag-success" : "tag-danger";
  }
  return "tag-neutral";
});
</script>

<template>
  <span class="tag" :class="tagClass">{{ success }}</span>
</template>
