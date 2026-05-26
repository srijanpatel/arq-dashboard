<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ success: boolean; status: string }>();

const className = computed(() => {
  if (props.status === "complete") {
    return props.success ? "is-success" : "is-danger";
  }
  return "";
});
</script>

<template>
  <span class="tag is-medium is-light" :class="className">{{ success }}</span>
</template>
