<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router";

defineProps<{
  label: string;
  value: number;
  color?: string;
  to?: RouteLocationRaw;
}>();
</script>

<template>
  <router-link v-if="to" :to="to" class="stat-card card card-hover" :style="color ? `--stat-color: ${color}` : ''">
    <div class="stat-value">{{ value.toLocaleString() }}</div>
    <div class="stat-label">{{ label }}</div>
  </router-link>
  <div v-else class="stat-card card" :style="color ? `--stat-color: ${color}` : ''">
    <div class="stat-value">{{ value.toLocaleString() }}</div>
    <div class="stat-label">{{ label }}</div>
  </div>
</template>

<style scoped>
.stat-card {
  text-decoration: none;
  color: inherit;
  border-left: 3px solid var(--stat-color, var(--color-border));
  text-align: center;
}

.stat-value {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  color: var(--color-text);
}

.stat-label {
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: var(--space-xs);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
</style>
