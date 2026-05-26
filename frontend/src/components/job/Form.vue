<script setup lang="ts">
import "@vuepic/vue-datepicker/dist/main.css";

import Datepicker from "@vuepic/vue-datepicker";
import { useRouteQuery } from "@vueuse/router";
import { onMounted, ref } from "vue";

import type { FunctionName, QueueName, SearchParams } from "@/types";

const props = defineProps<{
  page: number;
  functionNames: FunctionName[];
  queueNames: QueueName[];
}>();

const success = ref<boolean | undefined>(undefined);
const startTime = ref<string | undefined>(undefined);
const finishTime = ref<string | undefined>(undefined);
const functionName = ref<string | undefined>(undefined);
const status = ref<string | undefined>(undefined);

const functionQuery = useRouteQuery("function");
const statusQuery = useRouteQuery("status");

const statuses = ["deferred", "queued", "in_progress", "complete", "not_found"];

function normalizeQueryValue(value: string | undefined): string | undefined {
  if (value === undefined || value === "") return undefined;
  return value;
}

function getSearchParams(): SearchParams {
  return {
    page: props.page,
    success: success.value,
    status: normalizeQueryValue(status.value),
    startTime: normalizeQueryValue(startTime.value),
    finishTime: normalizeQueryValue(finishTime.value),
    functionName: normalizeQueryValue(functionName.value),
  };
}

onMounted(() => {
  if (functionQuery.value) functionName.value = functionQuery.value.toString();
  if (statusQuery.value) status.value = statusQuery.value.toString();
});

defineExpose({ getSearchParams });
</script>

<template>
  <div class="form-row">
    <div class="form-group">
      <label class="form-label">Function</label>
      <select v-model="functionName" class="form-select">
        <option value="">All functions</option>
        <option v-for="f in functionNames" :key="f.name" :value="f.name">{{ f.name }}</option>
      </select>
    </div>
    <div class="form-group">
      <label class="form-label">Status</label>
      <select v-model="status" class="form-select">
        <option value="">All statuses</option>
        <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>
  </div>

  <div class="form-row mt-md">
    <div class="form-group">
      <label class="form-label">Start time</label>
      <Datepicker v-model="startTime" />
    </div>
    <div class="form-group">
      <label class="form-label">Finish time</label>
      <Datepicker v-model="finishTime" />
    </div>
  </div>

  <div class="form-row mt-md">
    <div class="form-group">
      <label class="form-label">Success</label>
      <div class="form-radio-group">
        <label class="form-radio">
          <input type="radio" v-model="success" :value="true" /> True
        </label>
        <label class="form-radio">
          <input type="radio" v-model="success" :value="false" /> False
        </label>
        <label class="form-radio">
          <input type="radio" v-model="success" :value="undefined" /> Both
        </label>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Override vue-datepicker to match theme */
:deep(.dp__theme_light),
:deep(.dp__theme_dark) {
  --dp-background-color: var(--color-bg);
  --dp-text-color: var(--color-text);
  --dp-hover-color: var(--color-surface-hover);
  --dp-hover-text-color: var(--color-text);
  --dp-primary-color: var(--color-accent);
  --dp-primary-text-color: #fff;
  --dp-secondary-color: var(--color-text-dim);
  --dp-border-color: var(--color-border);
  --dp-menu-border-color: var(--color-border);
  --dp-border-color-hover: var(--color-accent);
  --dp-disabled-color: var(--color-text-dim);
  --dp-icon-color: var(--color-text-muted);
}
</style>
