<script setup lang="ts">
import { computed } from "vue";

import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

const props = defineProps<{
  enqueueTime?: string | null;
  startTime?: string | null;
  finishTime?: string | null;
}>();

function durationBetween(a: string, b: string): string {
  const ms = new Date(b).getTime() - new Date(a).getTime();
  if (ms < 1000) return `${ms}ms`;
  const s = ms / 1000;
  if (s < 60) return `${s.toFixed(1)}s`;
  const m = s / 60;
  return `${m.toFixed(1)}m`;
}

const waitTime = computed(() => {
  if (props.enqueueTime && props.startTime) return durationBetween(props.enqueueTime, props.startTime);
  return null;
});

const runTime = computed(() => {
  if (props.startTime && props.finishTime) return durationBetween(props.startTime, props.finishTime);
  return null;
});

const steps = computed(() => [
  { label: "Enqueued", time: props.enqueueTime, active: !!props.enqueueTime },
  { label: "Started", time: props.startTime, active: !!props.startTime },
  { label: "Finished", time: props.finishTime, active: !!props.finishTime },
]);
</script>

<template>
  <div class="timeline">
    <div class="timeline-track">
      <template v-for="(step, i) in steps" :key="step.label">
        <div class="timeline-step" :class="{ 'timeline-step-active': step.active }">
          <div class="timeline-dot"></div>
          <div class="timeline-label">{{ step.label }}</div>
          <div v-if="step.time" class="timeline-time" :title="getLocalDatetime(step.time)">
            {{ getHumanizedRelativeTime(step.time) }}
          </div>
          <div v-else class="timeline-time text-muted">—</div>
        </div>
        <div v-if="i < steps.length - 1" class="timeline-connector" :class="{ 'timeline-connector-active': steps[i + 1].active }">
          <span v-if="i === 0 && waitTime" class="timeline-duration">{{ waitTime }} wait</span>
          <span v-if="i === 1 && runTime" class="timeline-duration">{{ runTime }} runtime</span>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.timeline {
  padding: var(--space-lg) 0;
}

.timeline-track {
  display: flex;
  align-items: flex-start;
}

.timeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-border);
  border: 2px solid var(--color-surface);
  box-shadow: 0 0 0 2px var(--color-border);
  transition: all var(--transition-fast);
}

.timeline-step-active .timeline-dot {
  background: var(--color-accent);
  box-shadow: 0 0 0 2px var(--color-accent);
}

.timeline-label {
  margin-top: var(--space-sm);
  font-family: var(--font-ui);
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.timeline-time {
  margin-top: var(--space-xs);
  font-size: 0.8rem;
  color: var(--color-text-secondary);
}

.timeline-connector {
  flex: 1;
  height: 2px;
  background: var(--color-border);
  margin-top: 5px;
  position: relative;
  min-width: 60px;
}

.timeline-connector-active {
  background: var(--color-accent);
}

.timeline-duration {
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-ui);
  font-size: 0.7rem;
  color: var(--color-accent);
  white-space: nowrap;
}
</style>
