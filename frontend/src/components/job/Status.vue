<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ status: string }>();

const statusToClass = new Map<string, string>([
  ["deferred", "is-info"],
  ["queued", ""],
  ["in_progress", "is-link"],
  ["complete", "is-success"],
  ["not_found", "is-warning"],
]);

const className = computed(() => statusToClass.get(props.status) || "");
</script>

<template>
  <span class="tag is-medium" :class="className">{{ status }}</span>
</template>
